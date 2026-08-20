"""Génère les abstractions Pd communes Proto 06 (pd/lib/*_06.pd).

Isolation stricte du proto 05 (figé): tous les fichiers écrits portent le
suffixe _06. Idempotent: régénère les mêmes fichiers à chaque exécution.
"""
import math
import os
import shutil

from .pdbuild import P
from . import presets06 as PR

LIBDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "pd", "lib"))


def _w(p, fname):
    p.write(os.path.join(LIBDIR, fname))
    print(f"OK lib: {fname}")


# ---------------------------------------------------------------------------
def gen_fsm_memory_06(fname="fsm_memory_06.pd", fsm_n=None, max_layers=3,
                      cycle1=None):
    """FSM: cycle 1 fixe puis cycles libres, reset 7 min.

    cycle1: liste [(etat, dur_ms), ...] — défaut PR.CYCLE1 (4/6HP legacy).
            8HP artiste: PR.CYCLE1_8HP = CORTEX→HIPPO→RECON.

    Inlets:  0=FSM_AUTO (0/1), 1=FORCE etat (déjà gaté par le parent, Q21),
             2=bang session (démarre/redémarre le cycle 1 — lié à AUDIO_ON
             dans le parent: le visiteur entend le cycle depuis le début)
    Outlets: 0=etat, 1=bang presets (chaque transition, re-clic inclus),
             2=n couches, 3..(2+max_layers)=slots durée lecteurs,
             last=bang lecteurs (uniquement si l'état CHANGE — Q27)
    """
    fsm_n = PR.fsm_n_padded(fsm_n or PR.FSM_N, max_layers)
    cycle1 = cycle1 if cycle1 is not None else PR.CYCLE1
    n_c1 = len(cycle1)
    first_dur = cycle1[0][1]
    out_names = (["o_state", "o_bpre", "o_n"]
                 + [f"o_d{i}" for i in range(max_layers)]
                 + ["o_bply"])
    out_y = 820 + max_layers * 35 + 40
    p = P(max(860, 40 + len(out_names) * 110), out_y + 60)
    p.obj("in_auto", 40, 20, "inlet")
    p.obj("in_force", 200, 20, "inlet")
    p.obj("in_sess", 340, 20, "inlet")
    for i, nm in enumerate(out_names):
        p.obj(nm, 40 + i * 110, out_y, "outlet")

    # --- AUTO on/off + timer principal
    p.obj("a_t", 40, 60, "t f f f f")
    p.obj("sel_a1", 40, 100, "sel 1")
    p.obj("sel_a0", 110, 100, "sel 0")
    p.obj("f_durlast", 40, 140, f"f {first_dur}")
    p.msg("m_stop", 110, 140, "stop")
    p.obj("dur_t", 320, 100, "t b f f")
    p.obj("delay_main", 320, 150, f"delay {first_dur}")
    p.obj("spig_adv", 320, 190, "spigot")
    p.con("in_auto", 0, "a_t", 0)
    p.con("a_t", 3, "spig_adv", 1)      # fires first: gate advance
    p.con("a_t", 1, "sel_a1", 0)
    p.con("a_t", 0, "sel_a0", 0)
    p.con("sel_a1", 0, "f_durlast", 0)  # AUTO on -> relance timer (durée courante)
    p.con("f_durlast", 0, "dur_t", 0)
    p.con("sel_a0", 0, "m_stop", 0)     # AUTO off -> stop timer
    p.con("m_stop", 0, "delay_main", 0)
    p.con("dur_t", 2, "f_durlast", 1)
    p.con("dur_t", 1, "delay_main", 1)
    p.con("dur_t", 0, "delay_main", 0)
    p.con("delay_main", 0, "spig_adv", 0)

    # --- FORCE: stop+reset timer (Q26) puis goto
    p.obj("frc_t", 200, 60, "t f b")
    p.con("in_force", 0, "frc_t", 0)
    p.con("frc_t", 1, "m_stop", 0)

    # --- session: demarrage sur bang inlet 2 (pas au loadbang) + reset 7 min
    p.obj("lb_t", 620, 100, "t b b")
    p.obj("delay_reset", 620, 140, f"delay {PR.RESET_MS}")
    p.obj("drt", 620, 180, "t b b")
    p.obj("spig_rst", 620, 220, "spigot")
    p.con("in_sess", 0, "lb_t", 0)
    p.con("lb_t", 1, "delay_reset", 0)
    p.con("delay_reset", 0, "drt", 0)
    p.con("drt", 1, "delay_reset", 0)   # se relance toujours
    p.con("drt", 0, "spig_rst", 0)
    p.con("a_t", 2, "spig_rst", 1)

    # --- start cycle 1: c1=1, step=0, avance immédiate
    p.obj("start_t", 460, 260, "t b b b")
    p.msg("m_st0", 560, 300, "0")
    p.msg("m_c11", 620, 300, "1")
    p.con("lb_t", 0, "start_t", 0)
    p.con("spig_rst", 0, "start_t", 0)
    p.con("start_t", 2, "m_st0", 0)
    p.con("start_t", 1, "m_c11", 0)

    # --- avance: cycle1 (ordre fixe) ou libre (retour CORTEX 1/N)
    p.obj("f_c1", 60, 260, "f 1")
    p.obj("selc1", 60, 300, "sel 1 0")
    p.con("spig_adv", 0, "f_c1", 0)
    p.con("start_t", 0, "f_c1", 0)
    p.con("m_c11", 0, "f_c1", 1)
    p.con("f_c1", 0, "selc1", 0)

    # cycle 1
    p.obj("f_step", 60, 340, "f 0")
    p.obj("stp_t", 60, 380, "t f f")
    p.obj("plus1", 170, 380, "+ 1")
    sel_args = " ".join(str(i) for i in range(n_c1))
    p.obj("sel_step", 60, 420, f"sel {sel_args}")
    p.con("selc1", 0, "f_step", 0)
    p.con("m_st0", 0, "f_step", 1)
    p.con("f_step", 0, "stp_t", 0)
    p.con("stp_t", 1, "plus1", 0)
    p.con("plus1", 0, "f_step", 1)
    p.con("stp_t", 0, "sel_step", 0)
    p.msg("m_c1clr", 400, 500, "0")
    p.msg("m_cnt0", 450, 500, "0")
    for k, (st, dur) in enumerate(cycle1):
        x = 40 + k * 130
        if k == n_c1 - 1:
            p.obj(f"c1t{k}", x, 460, "t b b b b")
        else:
            p.obj(f"c1t{k}", x, 460, "t b b")
        p.msg(f"c1d{k}", x, 500, str(dur))
        p.msg(f"c1s{k}", x, 540, str(st))
        p.con("sel_step", k, f"c1t{k}", 0)
        if k == n_c1 - 1:
            p.con(f"c1t{k}", 3, f"c1d{k}", 0)
            p.con(f"c1t{k}", 2, "m_c1clr", 0)   # fin cycle 1
            p.con(f"c1t{k}", 1, "m_cnt0", 0)
            p.con(f"c1t{k}", 0, f"c1s{k}", 0)
        else:
            p.con(f"c1t{k}", 1, f"c1d{k}", 0)
            p.con(f"c1t{k}", 0, f"c1s{k}", 0)
        p.con(f"c1d{k}", 0, "dur_t", 0)
    p.con("m_c1clr", 0, "f_c1", 1)

    # cycles libres
    p.obj("free_t", 180, 300, "t b b")
    p.obj("rnd_dur", 290, 340, f"random {PR.FREE_DUR_RAND}")
    p.obj("pl15", 290, 380, f"+ {PR.FREE_DUR_BASE}")
    p.obj("f_cnt", 180, 340, "f 0")
    p.obj("cp1", 180, 380, "+ 1")
    p.obj("cnt_t", 180, 420, "t f f")
    p.obj("mod5", 180, 460, f"% {PR.FREE_CORTEX_EVERY}")
    p.obj("sel5", 180, 500, "sel 0")
    p.msg("m_cx", 180, 540, "0")
    # état suivant toujours DIFFÉRENT du courant (cur+1+random(3) mod 4):
    # chaque transition libre change d'état -> relance lecteurs -> nouveaux
    # samples à chaque passage (retour Loumana 10 juil.)
    p.obj("tb5", 250, 540, "t b b")
    p.obj("f_cur", 360, 540, "f 0")
    p.obj("rnd4", 250, 580, "random 3")
    p.obj("nx_p1", 250, 615, "+ 1")
    p.obj("nx_add", 250, 650, "+")
    p.obj("nx_mod", 250, 685, "% 4")
    p.con("tb5", 1, "f_cur", 0)
    p.con("f_cur", 0, "nx_add", 1)
    p.con("rnd4", 0, "nx_p1", 0)
    p.con("nx_p1", 0, "nx_add", 0)
    p.con("nx_add", 0, "nx_mod", 0)
    p.con("selc1", 1, "free_t", 0)
    p.con("free_t", 1, "rnd_dur", 0)
    p.con("rnd_dur", 0, "pl15", 0)
    p.con("pl15", 0, "dur_t", 0)
    p.con("free_t", 0, "f_cnt", 0)
    p.con("m_cnt0", 0, "f_cnt", 1)
    p.con("f_cnt", 0, "cp1", 0)
    p.con("cp1", 0, "cnt_t", 0)
    p.con("cnt_t", 1, "f_cnt", 1)
    p.con("cnt_t", 0, "mod5", 0)
    p.con("mod5", 0, "sel5", 0)
    p.con("sel5", 0, "m_cx", 0)
    p.con("sel5", 1, "tb5", 0)
    p.con("tb5", 0, "rnd4", 0)

    # --- goto(state): ordre déterministe (droite -> gauche)
    #     1 détection de changement  2 msgs n/durées (froid pour le parent)
    #     3 sortie etat (chaud)      4 bang presets  5 bang lecteurs
    p.obj("goto_t", 40, 620, "t b b f f f")
    for src in ["frc_t", "m_cx", "nx_mod"]:
        p.con(src, 0, "goto_t", 0)
    for k in range(n_c1):
        p.con(f"c1s{k}", 0, "goto_t", 0)
    p.obj("cd_t", 460, 660, "t f f b")
    p.obj("f_last", 560, 700, "f -1")
    p.obj("neq", 460, 740, "!=")
    p.obj("spig_pl", 460, 780, "spigot")
    p.con("goto_t", 4, "cd_t", 0)
    p.con("cd_t", 2, "f_last", 0)       # ancien état -> comparateur
    p.con("f_last", 0, "neq", 1)
    p.con("cd_t", 1, "neq", 0)
    p.con("neq", 0, "spig_pl", 1)
    p.con("cd_t", 0, "f_last", 1)       # mémorise le nouvel état
    p.con("cd_t", 0, "f_cur", 1)        # même mémoire pour le tirage libre
    p.obj("sel_nd", 140, 740, "sel 0 1 2 3")
    p.con("goto_t", 3, "sel_nd", 0)
    p.con("goto_t", 2, "o_state", 0)
    p.con("goto_t", 1, "o_bpre", 0)
    for s in range(4):
        tup = fsm_n[s]
        n = tup[0]
        slots = tup[1:]
        x = 140 + s * 170
        p.msg(f"nd_n{s}", x, 790, str(n))
        p.con("sel_nd", s, f"nd_n{s}", 0)
        p.con(f"nd_n{s}", 0, "o_n", 0)
        for li, slot in enumerate(slots):
            p.msg(f"nd_{li}{s}", x, 820 + li * 30, str(slot))
            p.con("sel_nd", s, f"nd_{li}{s}", 0)
            p.con(f"nd_{li}{s}", 0, f"o_d{li}", 0)
    p.con("goto_t", 0, "spig_pl", 0)
    p.con("spig_pl", 0, "o_bply", 0)

    _w(p, fname)


# ---------------------------------------------------------------------------
def gen_fsm_presets_06(fname="fsm_presets_06.pd", presets=None):
    """Tirage variante (3 par état, Q23) + application banque SPAT/FX.

    Inlets: 0=bang (transition), 1=etat (froid).
    Outlet: 0=variante_id (etat*3+variante, 0..11 — Q25).
    r s6_preset_refresh: ré-applique la dernière banque (fin de sweep HIPPO).
    """
    presets = presets or PR.PRESETS
    p = P(1200, 700)
    p.obj("in_b", 40, 20, "inlet")
    p.obj("in_s", 140, 20, "inlet")
    p.obj("o_var", 40, 660, "outlet")
    p.obj("mul3p", 140, 60, "* 3")
    p.obj("rnd3", 40, 60, "random 3")
    p.obj("padd", 40, 100, "+")
    p.obj("pt", 40, 140, "t f f f")
    p.obj("f_last", 200, 140, "f 0")
    p.obj("sel_b", 40, 180, "sel 0 1 2 3 4 5 6 7 8 9 10 11")
    p.obj("r_ref", 300, 20, "r s6_preset_refresh")
    p.con("in_s", 0, "mul3p", 0)
    p.con("mul3p", 0, "padd", 1)
    p.con("in_b", 0, "rnd3", 0)
    p.con("rnd3", 0, "padd", 0)
    p.con("padd", 0, "pt", 0)
    p.con("pt", 1, "o_var", 0)
    p.con("pt", 2, "f_last", 1)
    p.con("pt", 0, "sel_b", 0)
    p.con("r_ref", 0, "f_last", 0)
    p.con("f_last", 0, "sel_b", 0)
    p.text(300, 40, "banques presets: etat*3+variante -> multi-send s6_*;")
    for s in range(4):
        for v in range(3):
            bid = s * 3 + v
            body = "\\; " + PR.bank_msg_body(presets[s][v])
            p.msg(f"bank{bid}", 300, 60 + bid * 44, body)
            p.con("sel_b", bid, f"bank{bid}", 0)
    _w(p, fname)


def gen_hippo_motion_06():
    """Dramaturgie spatiale HIPPO 8HP — actif seulement en état HIPPOCAMPE.

    - Phase normale: presets (souvent mode 4 = circulation 3–4 baffles).
    - De temps à autre: nudge mode4 sur couche 1–2.
    - Parfois: SWEEP solo — 1 sample, mode 3 rapide HP1→HP8, autres couches
      coupées (s6_hippo_solo 1) ; à la fin → solo 0 + refresh presets.
    """
    p = P(900, 520)
    p.text(20, 10, "hippo_motion_06 — sweep 1..8 + circulation locale;")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel_h", 40, 70, "sel 1")
    p.obj("gate", 40, 100, "spigot")
    p.obj("met", 40, 140, "metro 5500")
    p.obj("f_on", 200, 70, "f 0")
    p.obj("eq_on", 200, 100, "== 1")
    p.con("r_et", 0, "sel_h", 0)
    # entrée HIPPO: metro on ; sortie: metro off + solo 0
    p.msg("m_on", 140, 100, "1")
    p.msg("m_off", 140, 130, "0")
    p.msg("m_solo0", 140, 160, "0")
    p.obj("s_solo", 280, 160, "s s6_hippo_solo")
    p.con("sel_h", 0, "m_on", 0)
    p.con("m_on", 0, "f_on", 1)
    p.con("m_on", 0, "met", 0)
    p.con("sel_h", 1, "m_off", 0)
    p.con("m_off", 0, "f_on", 1)
    p.con("m_off", 0, "met", 0)
    p.con("sel_h", 1, "m_solo0", 0)
    p.con("m_solo0", 0, "s_solo", 0)
    p.con("f_on", 0, "eq_on", 0)
    p.con("eq_on", 0, "gate", 1)
    p.con("met", 0, "gate", 0)

    # tirage événement: 0-1 local nudge, 2 sweep, 3-4 idle
    p.obj("rnd", 40, 180, "random 5")
    p.obj("sel_ev", 40, 210, "sel 0 1 2 3 4")
    p.con("gate", 0, "rnd", 0)
    p.con("rnd", 0, "sel_ev", 0)

    # --- nudge locale (mode 4) sur L1 / L2
    p.msg("n_l1m", 300, 210, "4")
    p.msg("n_l1s", 300, 240, "480")
    p.msg("n_l1x", 300, 270, "35")
    p.obj("s_l1m", 400, 210, "s s6_l1_mode")
    p.obj("s_l1s", 400, 240, "s s6_l1_step")
    p.obj("s_l1x", 400, 270, "s s6_l1_xfade")
    p.msg("n_l2m", 300, 310, "4")
    p.msg("n_l2s", 300, 340, "560")
    p.obj("s_l2m", 400, 310, "s s6_l2_mode")
    p.obj("s_l2s", 400, 340, "s s6_l2_step")
    for ev in (0, 1):
        p.con("sel_ev", ev, "n_l1m", 0)
        p.con("sel_ev", ev, "n_l1s", 0)
        p.con("sel_ev", ev, "n_l1x", 0)
        p.con("sel_ev", ev, "n_l2m", 0)
        p.con("sel_ev", ev, "n_l2s", 0)
    p.con("n_l1m", 0, "s_l1m", 0)
    p.con("n_l1s", 0, "s_l1s", 0)
    p.con("n_l1x", 0, "s_l1x", 0)
    p.con("n_l2m", 0, "s_l2m", 0)
    p.con("n_l2s", 0, "s_l2s", 0)

    # --- SWEEP solo 1→8 rapide puis restore
    # 8 HP * 170 ms ≈ 1360 + marge
    p.msg("sw_solo1", 40, 280, "1")
    p.msg("sw_m3", 40, 310, "3")
    p.msg("sw_st", 40, 340, "170")
    p.msg("sw_xf", 40, 370, "18")
    p.obj("s_swm", 160, 310, "s s6_l1_mode")
    p.obj("s_sws", 160, 340, "s s6_l1_step")
    p.obj("s_swx", 160, 370, "s s6_l1_xfade")
    p.obj("del_sw", 40, 410, "delay 1550")
    p.msg("sw_solo0", 40, 450, "0")
    p.obj("s_ref", 160, 450, "s s6_preset_refresh")
    p.obj("tb_sw", 40, 250, "t b b b b b")
    p.con("sel_ev", 2, "tb_sw", 0)
    p.con("tb_sw", 0, "sw_solo1", 0)
    p.con("sw_solo1", 0, "s_solo", 0)
    p.con("tb_sw", 1, "sw_m3", 0)
    p.con("sw_m3", 0, "s_swm", 0)
    p.con("tb_sw", 2, "sw_st", 0)
    p.con("sw_st", 0, "s_sws", 0)
    p.con("tb_sw", 3, "sw_xf", 0)
    p.con("sw_xf", 0, "s_swx", 0)
    p.con("tb_sw", 4, "del_sw", 0)
    p.con("del_sw", 0, "sw_solo0", 0)
    p.con("sw_solo0", 0, "s_solo", 0)
    p.con("del_sw", 0, "s_ref", 0)

    p.text(500, 100, "events: 0-1 mode4 local \\; 2 sweep solo 1-8 \\; 3-4 idle;")
    _w(p, "hippo_motion_06.pd")


# ---------------------------------------------------------------------------
def gen_spatial_router_06():
    """Routeur spatial par couche. Args: $1=couche, $2=azimut ancre,
    $3=HP ancre (1-based), $4=nb HP directs (4/5/8), $5=$4-1 (tirage saut).

    Inlet~: audio (post-FX). Outlets~: W X Y (bus ambi) + HP1..HP8 (bus
    directs — HP inutilisés restent à 0). Reçoit s6_l$1_mode/rot/sens/step/xfade.
    Modes: 0=dry DIRECT sur HP $3, 1=rotation ambi, 2=saut HP,
    3=séquence HP (tous), 4=circulation locale 3–4 baffles voisins.
    """
    p = P(1400, 1100)
    p.obj("in_a", 40, 20, "inlet~")
    outs = ["o_w", "o_x", "o_y"] + [f"o_h{k}" for k in range(1, 9)]
    for i, nm in enumerate(outs):
        p.obj(nm, 20 + i * 100, 1060, "outlet~")

    p.obj("r_mode", 300, 20, "r s6_l\\$1_mode")
    p.obj("mode_t", 300, 60, "t f f f f f f")
    p.con("r_mode", 0, "mode_t", 0)

    # --- mode 1: bus ambi + rotation
    p.obj("eq1a", 40, 110, "== 1")
    p.obj("pk_a", 40, 150, "pack 0 30")
    p.obj("ln_a", 40, 190, "line~")
    p.obj("g_a", 40, 240, "*~")
    p.con("mode_t", 4, "eq1a", 0)
    p.con("eq1a", 0, "pk_a", 0)
    p.con("pk_a", 0, "ln_a", 0)
    p.con("ln_a", 0, "g_a", 1)
    p.con("in_a", 0, "g_a", 0)

    p.obj("eq1", 280, 110, "== 1")
    p.obj("spig_rot", 280, 300, "spigot")
    p.con("mode_t", 2, "eq1", 0)
    p.con("eq1", 0, "spig_rot", 1)

    p.obj("r_rot", 420, 110, "r s6_l\\$1_rot")
    p.obj("rot_t", 420, 150, "t f f")
    p.obj("r_sens", 560, 110, "r s6_l\\$1_sens")
    p.obj("sensm2", 560, 150, "* -2")
    p.obj("sensp1", 560, 190, "+ 1")
    p.obj("senst", 560, 230, "t b f f")
    p.obj("rot_f", 470, 230, "f")
    p.obj("rot_mul", 420, 270, "* 1")
    p.obj("phasor", 420, 310, "phasor~ 0.05")
    p.obj("mul360", 420, 350, "*~ 360")
    p.obj("snap", 420, 390, "snapshot~")
    p.obj("met40", 540, 350, "metro 40")
    p.con("r_rot", 0, "rot_t", 0)
    p.con("rot_t", 1, "rot_f", 1)
    p.con("rot_t", 0, "rot_mul", 0)
    p.con("r_sens", 0, "sensm2", 0)
    p.con("sensm2", 0, "sensp1", 0)
    p.con("sensp1", 0, "senst", 0)
    p.con("senst", 1, "rot_mul", 1)
    p.con("senst", 0, "rot_f", 0)
    p.con("rot_f", 0, "rot_mul", 0)
    p.con("rot_mul", 0, "phasor", 0)
    p.con("phasor", 0, "mul360", 0)
    p.con("mul360", 0, "snap", 0)
    p.con("met40", 0, "snap", 0)
    p.con("snap", 0, "spig_rot", 0)
    p.obj("add_anchor", 280, 340, "+ \\$2")
    p.con("spig_rot", 0, "add_anchor", 0)

    p.obj("enc", 160, 420, "encode_2d")
    p.obj("f_anchor", 160, 190, "f \\$2")
    p.con("f_anchor", 0, "enc", 0)
    p.con("add_anchor", 0, "enc", 0)
    p.con("g_a", 0, "enc", 1)
    p.con("enc", 0, "o_w", 0)
    p.con("enc", 1, "o_x", 0)
    p.con("enc", 2, "o_y", 0)

    # --- mode 0: dry DIRECT sur HP ancre $3
    p.obj("eq0", 40, 300, "== 0")
    p.obj("pk_d0", 40, 340, "pack 0 30")
    p.obj("ln_d0", 40, 370, "line~")
    p.obj("g_d0", 40, 400, "*~")
    p.con("mode_t", 3, "eq0", 0)
    p.con("eq0", 0, "pk_d0", 0)
    p.con("pk_d0", 0, "ln_d0", 0)
    p.con("ln_d0", 0, "g_d0", 1)
    p.con("in_a", 0, "g_d0", 0)
    p.obj("eq0sel", 140, 300, "sel 1")
    p.obj("d0_get", 140, 340, "f \\$3")
    p.obj("d0_m1", 140, 370, "- 1")
    p.obj("d0_idx", 140, 400, "f 0")
    p.con("eq0", 0, "eq0sel", 0)
    p.con("eq0sel", 0, "d0_get", 0)
    p.con("d0_get", 0, "d0_m1", 0)
    p.con("d0_m1", 0, "d0_idx", 0)

    # --- params saut/séquence
    p.obj("r_step", 700, 110, "r s6_l\\$1_step")
    p.obj("step_t", 700, 150, "t f f")
    p.obj("r_xf", 850, 110, "r s6_l\\$1_xfade")
    p.con("r_step", 0, "step_t", 0)

    # --- init ancre + metro
    p.obj("lb_m", 540, 270, "loadbang")
    p.obj("ilb_t", 540, 305, "t b b b")
    p.msg("m_one", 640, 305, "1")
    p.obj("f_init", 700, 300, "f \\$3")
    p.obj("im1", 700, 340, "- 1")
    p.obj("init_t", 700, 380, "t f f f f")
    p.con("lb_m", 0, "ilb_t", 0)
    p.con("ilb_t", 2, "m_one", 0)
    p.con("m_one", 0, "met40", 0)
    p.con("ilb_t", 1, "f_init", 0)
    p.con("f_init", 0, "im1", 0)
    p.con("im1", 0, "init_t", 0)
    p.con("ilb_t", 0, "d0_get", 0)

    # --- mode 2: saut
    p.obj("eq2", 460, 470, "== 2")
    p.obj("j_t", 460, 505, "t f f")
    p.obj("pk_j", 560, 540, "pack 0 30")
    p.obj("ln_j", 560, 575, "line~")
    p.obj("g_j", 460, 620, "*~")
    p.obj("met_j", 460, 540, "metro 800")
    p.obj("jm_t", 380, 575, "t b b")
    p.obj("jf_prev", 300, 615, "f 0")
    p.obj("rnd3j", 380, 615, "random \\$5")
    p.obj("jp1", 380, 650, "+ 1")
    p.obj("jadd", 340, 685, "+")
    p.obj("jmod", 340, 715, "% \\$4")
    p.obj("jt", 340, 745, "t f f")
    p.con("mode_t", 1, "eq2", 0)
    p.con("eq2", 0, "j_t", 0)
    p.con("j_t", 1, "pk_j", 0)
    p.con("pk_j", 0, "ln_j", 0)
    p.con("ln_j", 0, "g_j", 1)
    p.con("j_t", 0, "met_j", 0)
    p.con("step_t", 1, "met_j", 1)
    p.con("met_j", 0, "jm_t", 0)
    p.con("jm_t", 1, "jf_prev", 0)
    p.con("jf_prev", 0, "jadd", 1)
    p.con("jm_t", 0, "rnd3j", 0)
    p.con("rnd3j", 0, "jp1", 0)
    p.con("jp1", 0, "jadd", 0)
    p.con("jadd", 0, "jmod", 0)
    p.con("jmod", 0, "jt", 0)
    p.con("jt", 1, "jf_prev", 1)
    p.con("init_t", 3, "jf_prev", 1)
    p.con("init_t", 2, "jt", 0)
    p.con("in_a", 0, "g_j", 0)

    # --- mode 3: séquence
    p.obj("eq3", 700, 470, "== 3")
    p.obj("s_t", 700, 505, "t f f")
    p.obj("pk_s", 800, 540, "pack 0 30")
    p.obj("ln_s", 800, 575, "line~")
    p.obj("g_s", 700, 620, "*~")
    p.obj("met_s", 700, 540, "metro 800")
    p.obj("sf", 640, 580, "f 0")
    p.obj("sadd", 640, 615, "+ 1")
    p.obj("sp4", 640, 650, "+ \\$4")
    p.obj("smod", 640, 685, "% \\$4")
    p.obj("st_s", 640, 715, "t f f")
    p.con("mode_t", 0, "eq3", 0)
    p.con("eq3", 0, "s_t", 0)
    p.con("s_t", 1, "pk_s", 0)
    p.con("pk_s", 0, "ln_s", 0)
    p.con("ln_s", 0, "g_s", 1)
    p.con("s_t", 0, "met_s", 0)
    p.con("step_t", 0, "met_s", 1)
    p.con("met_s", 0, "sf", 0)
    p.con("sf", 0, "sadd", 0)
    p.con("senst", 2, "sadd", 1)
    p.con("sadd", 0, "sp4", 0)
    p.con("sp4", 0, "smod", 0)
    p.con("smod", 0, "st_s", 0)
    p.con("st_s", 1, "sf", 1)
    p.con("init_t", 1, "sf", 1)
    p.con("init_t", 0, "st_s", 0)
    p.con("in_a", 0, "g_s", 0)

    # --- mode 4: circulation locale sur 3–4 baffles voisins
    p.obj("eq4", 900, 470, "== 4")
    p.obj("l4_t", 900, 505, "t f f f")
    p.obj("pk_l", 1000, 540, "pack 0 30")
    p.obj("ln_l", 1000, 575, "line~")
    p.obj("g_l", 900, 620, "*~")
    p.obj("met_l", 900, 540, "metro 500")
    p.obj("f_win", 820, 540, "f 4")
    p.obj("f_start", 820, 575, "f 0")
    p.obj("f_pos", 820, 610, "f 0")
    p.obj("rnd_win", 740, 540, "random 2")
    p.obj("win3", 740, 575, "+ 3")
    p.obj("rnd_st", 740, 610, "random \\$4")
    p.obj("lt_init", 740, 645, "t b b b")
    p.obj("lp1", 820, 680, "+ 1")
    p.obj("lmodw", 820, 715, "%")
    p.obj("ladd", 880, 750, "+")
    p.obj("lmodn", 880, 785, "% \\$4")
    p.obj("loc_t", 880, 820, "t f f")
    p.obj("lz", 960, 680, "sel 0")
    p.obj("ltb", 960, 715, "t b b")
    p.con("mode_t", 5, "eq4", 0)
    p.con("eq4", 0, "l4_t", 0)
    p.con("l4_t", 1, "pk_l", 0)
    p.con("pk_l", 0, "ln_l", 0)
    p.con("ln_l", 0, "g_l", 1)
    p.con("l4_t", 0, "met_l", 0)
    p.con("step_t", 0, "met_l", 1)
    p.con("l4_t", 2, "lt_init", 0)
    p.con("lt_init", 0, "rnd_win", 0)
    p.con("rnd_win", 0, "win3", 0)
    p.con("win3", 0, "f_win", 1)
    p.con("lt_init", 1, "rnd_st", 0)
    p.con("rnd_st", 0, "f_start", 1)
    p.con("lt_init", 2, "m_l0", 0)
    p.msg("m_l0", 700, 680, "0")
    p.con("m_l0", 0, "f_pos", 1)
    p.con("in_a", 0, "g_l", 0)
    # metro: pos+1 % win ; si wrap → nouveau start ; hp = (start+pos)%N
    p.obj("ltm", 780, 680, "t b f")
    p.con("met_l", 0, "f_pos", 0)
    p.con("f_pos", 0, "lp1", 0)
    p.con("lp1", 0, "ltm", 0)
    p.con("ltm", 0, "f_win", 0)
    p.con("f_win", 0, "lmodw", 1)
    p.con("ltm", 1, "lmodw", 0)
    p.obj("ltp", 820, 745, "t f f f")
    p.con("lmodw", 0, "ltp", 0)
    p.con("ltp", 2, "f_pos", 1)
    p.con("ltp", 1, "lz", 0)
    p.con("lz", 0, "ltb", 0)
    p.con("ltb", 0, "rnd_st", 0)
    p.con("ltb", 1, "f_start", 0)
    p.obj("lta", 850, 780, "t b f")
    p.con("ltp", 0, "lta", 0)
    p.con("lta", 0, "f_start", 0)
    p.con("f_start", 0, "ladd", 1)
    p.con("lta", 1, "ladd", 0)
    p.con("ladd", 0, "lmodn", 0)
    p.con("lmodn", 0, "loc_t", 0)
    # première position à l'entrée du mode
    p.obj("lfirst", 700, 750, "t b b")
    p.con("lt_init", 2, "lfirst", 0)
    p.con("lfirst", 0, "f_start", 0)
    p.con("f_start", 0, "loc_t", 0)

    # somme audio seq (mode3) + locale (mode4) vers les mêmes gates HP
    p.obj("g_seqsum", 700, 655, "+~")
    p.con("g_s", 0, "g_seqsum", 0)
    p.con("g_l", 0, "g_seqsum", 1)

    # gates par HP: dry(mode0) + saut + séquence/locale
    for k in range(8):
        x = 20 + (k % 4) * 160
        y0 = 560 + (k // 4) * 180
        p.obj(f"deq{k}", x, y0, f"== {k}")
        p.obj(f"dpk{k}", x, y0 + 25, "pack 0 20")
        p.obj(f"dln{k}", x, y0 + 50, "line~")
        p.obj(f"dg{k}", x, y0 + 75, "*~")
        p.con("d0_idx", 0, f"deq{k}", 0)
        p.con(f"deq{k}", 0, f"dpk{k}", 0)
        p.con(f"dpk{k}", 0, f"dln{k}", 0)
        p.con(f"dln{k}", 0, f"dg{k}", 1)
        p.con("g_d0", 0, f"dg{k}", 0)
        p.con(f"dg{k}", 0, f"o_h{k + 1}", 0)
        p.obj(f"jeq{k}", x + 70, y0, f"== {k}")
        p.obj(f"jpk{k}", x + 70, y0 + 25, "pack 0 20")
        p.obj(f"jln{k}", x + 70, y0 + 50, "line~")
        p.obj(f"jg{k}", x + 70, y0 + 75, "*~")
        p.con("jt", 0, f"jeq{k}", 0)
        p.con(f"jeq{k}", 0, f"jpk{k}", 0)
        p.con("r_xf", 0, f"jpk{k}", 1)
        p.con(f"jpk{k}", 0, f"jln{k}", 0)
        p.con(f"jln{k}", 0, f"jg{k}", 1)
        p.con("g_j", 0, f"jg{k}", 0)
        p.con(f"jg{k}", 0, f"o_h{k + 1}", 0)
        p.obj(f"seq{k}", x + 35, y0 + 105, f"== {k}")
        p.obj(f"spk{k}", x + 35, y0 + 130, "pack 0 20")
        p.obj(f"sln{k}", x + 35, y0 + 155, "line~")
        p.obj(f"sg{k}", x + 35, y0 + 175, "*~")
        p.con("st_s", 0, f"seq{k}", 0)
        p.con("loc_t", 0, f"seq{k}", 0)
        p.con(f"seq{k}", 0, f"spk{k}", 0)
        p.con("r_xf", 0, f"spk{k}", 1)
        p.con(f"spk{k}", 0, f"sln{k}", 0)
        p.con(f"sln{k}", 0, f"sg{k}", 1)
        p.con("g_seqsum", 0, f"sg{k}", 0)
        p.con(f"sg{k}", 0, f"o_h{k + 1}", 0)

    _w(p, "spatial_router_06.pd")


def gen_fx_distort_06():
    """Saturation soft-clip par couche (J6/J7).

    Inlets: 0=in~  1=sat 0..1 (drive + wet)
    sat=0 → bypass pur. Compensation gain ×1.5 (J7).
    """
    p = P(520, 420)
    p.obj("in_a", 40, 20, "inlet~")
    p.obj("in_sat", 200, 20, "inlet")
    p.obj("o", 40, 380, "outlet~")
    # sat → line~ (wet) + drive = 1+sat*4 + gain_comp = 1/(1+sat*1.5)
    p.obj("clip_sat", 200, 60, "clip 0 1")
    p.obj("pk_w", 200, 90, "pack 0 30")
    p.obj("ln_w", 200, 120, "line~")
    p.obj("drv", 320, 60, "* 4")
    p.obj("drv1", 320, 90, "+ 1")
    p.obj("pk_d", 320, 120, "pack 0 30")
    p.obj("ln_d", 320, 150, "line~")
    p.obj("comp_m", 420, 60, "* 1.5")
    p.obj("comp_a", 420, 90, "+ 1")
    p.obj("t_comp", 420, 120, "t b f")
    p.msg("m_one", 500, 120, "1")
    p.obj("div_c", 420, 150, "/")
    p.obj("pk_c", 420, 180, "pack 0 30")
    p.obj("ln_c", 420, 210, "line~")
    p.con("in_sat", 0, "clip_sat", 0)
    p.con("clip_sat", 0, "pk_w", 0)
    p.con("pk_w", 0, "ln_w", 0)
    p.con("clip_sat", 0, "drv", 0)
    p.con("drv", 0, "drv1", 0)
    p.con("drv1", 0, "pk_d", 0)
    p.con("pk_d", 0, "ln_d", 0)
    p.con("clip_sat", 0, "comp_m", 0)
    p.con("comp_m", 0, "comp_a", 0)
    p.con("comp_a", 0, "t_comp", 0)
    p.con("t_comp", 1, "div_c", 1)
    p.con("t_comp", 0, "m_one", 0)
    p.con("m_one", 0, "div_c", 0)
    p.con("div_c", 0, "pk_c", 0)
    p.con("pk_c", 0, "ln_c", 0)
    # distort path: in * drive → clip → * gain_comp → * wet
    p.obj("mul_d", 40, 100, "*~")
    p.obj("clp", 40, 140, "clip~ -0.85 0.85")
    p.obj("mul_c", 40, 180, "*~")
    p.obj("mul_w", 40, 220, "*~")
    p.con("in_a", 0, "mul_d", 0)
    p.con("ln_d", 0, "mul_d", 1)
    p.con("mul_d", 0, "clp", 0)
    p.con("clp", 0, "mul_c", 0)
    p.con("ln_c", 0, "mul_c", 1)
    p.con("mul_c", 0, "mul_w", 0)
    p.con("ln_w", 0, "mul_w", 1)
    # dry = in * (1 - wet)
    p.obj("one", 160, 180, "sig~ 1")
    p.obj("sub_w", 160, 220, "-~")
    p.obj("mul_dry", 160, 260, "*~")
    p.con("one", 0, "sub_w", 0)
    p.con("ln_w", 0, "sub_w", 1)
    p.con("in_a", 0, "mul_dry", 0)
    p.con("sub_w", 0, "mul_dry", 1)
    p.obj("sum", 40, 300, "+~")
    p.con("mul_dry", 0, "sum", 0)
    p.con("mul_w", 0, "sum", 1)
    p.con("sum", 0, "o", 0)
    p.text(20, 350, "sat=0 bypass \\; drive=1+sat*4 \\; gain=1/(1+sat*1.5);")
    _w(p, "fx_distort_06.pd")


def gen_fx_filter_06():
    """HPF + LPF + LFO léger sur LPF (J4).

    Inlets: 0=in~  1=hpf Hz  2=lpf Hz  3=flfo 0..1 (profondeur mod LPF)
    Défaut transparent: hpf=20, lpf=20000, flfo=0.
    """
    p = P(620, 400)
    p.obj("in_a", 40, 20, "inlet~")
    p.obj("in_hpf", 160, 20, "inlet")
    p.obj("in_lpf", 300, 20, "inlet")
    p.obj("in_flfo", 440, 20, "inlet")
    p.obj("o", 40, 360, "outlet~")
    # HPF
    p.obj("chpf", 160, 60, "clip 20 1200")
    p.obj("pk_h", 160, 90, "pack 0 40")
    p.obj("ln_h", 160, 120, "line")
    p.obj("hip", 40, 160, "hip~ 20")
    p.con("in_hpf", 0, "chpf", 0)
    p.con("chpf", 0, "pk_h", 0)
    p.con("pk_h", 0, "ln_h", 0)
    p.con("ln_h", 0, "hip", 1)
    p.con("in_a", 0, "hip", 0)
    # LFO → add to LPF (depth = flfo * 800 Hz)
    p.obj("cfl", 440, 60, "clip 0 1")
    p.obj("pk_f", 440, 90, "pack 0 40")
    p.obj("ln_f", 440, 120, "line~")
    p.obj("osc", 440, 160, "osc~ 0.12")
    p.obj("mdepth", 440, 200, "*~ 800")
    p.obj("mlfo", 440, 240, "*~")
    p.con("in_flfo", 0, "cfl", 0)
    p.con("cfl", 0, "pk_f", 0)
    p.con("pk_f", 0, "ln_f", 0)
    p.con("osc", 0, "mdepth", 0)
    p.con("mdepth", 0, "mlfo", 0)
    p.con("ln_f", 0, "mlfo", 1)
    # LPF cutoff = lpf + lfo_mod, clipped
    p.obj("clpf", 300, 60, "clip 400 20000")
    p.obj("pk_l", 300, 90, "pack 0 40")
    p.obj("ln_l", 300, 120, "line~")
    p.obj("add_m", 300, 200, "+~")
    p.obj("clip_f", 300, 240, "clip~ 400 20000")
    p.obj("lop", 40, 240, "lop~ 20000")
    p.obj("sn", 300, 280, "snapshot~")
    p.obj("metro", 300, 310, "metro 40")
    p.obj("lb", 380, 310, "loadbang")
    p.con("in_lpf", 0, "clpf", 0)
    p.con("clpf", 0, "pk_l", 0)
    p.con("pk_l", 0, "ln_l", 0)
    p.con("ln_l", 0, "add_m", 0)
    p.con("mlfo", 0, "add_m", 1)
    p.con("add_m", 0, "clip_f", 0)
    p.con("clip_f", 0, "sn", 0)
    p.con("lb", 0, "metro", 0)
    p.con("metro", 0, "sn", 0)
    p.con("sn", 0, "lop", 1)
    p.con("hip", 0, "lop", 0)
    p.con("lop", 0, "o", 0)
    p.text(20, 340, "HPF 20-1200 \\; LPF 400-20k + LFO*flfo*800Hz;");
    _w(p, "fx_filter_06.pd")


def gen_fx_router_06():
    """Chaîne FX par couche ($1=couche): sat → filtre → ECHO + CONTRASTE.

    Reçoit s6_l$1_wet/del/fb/lfo/on/sat/hpf/lpf/flfo et s6_contraste_f (Q24).
    Ordre J8: saturation → filtre → (ECHO déjà en place).
    """
    p = P(900, 520)
    p.obj("in_a", 40, 20, "inlet~")
    p.obj("o", 40, 480, "outlet~")
    p.obj("dist", 40, 200, "fx_distort_06")
    p.obj("filt", 40, 280, "fx_filter_06")
    p.obj("fx", 40, 360, "fx_fluid")
    p.con("in_a", 0, "dist", 0)
    p.con("dist", 0, "filt", 0)
    p.con("filt", 0, "fx", 0)
    p.con("fx", 0, "o", 0)

    # --- ECHO params + CONTRASTE
    p.obj("r_wet", 160, 40, "r s6_l\\$1_wet")
    p.obj("fw", 160, 80, "f")
    p.obj("mw", 160, 120, "* 1")
    p.obj("r_del", 300, 40, "r s6_l\\$1_del")
    p.obj("r_fb", 420, 40, "r s6_l\\$1_fb")
    p.obj("ffb", 420, 80, "f")
    p.obj("mfb", 420, 120, "* 1")
    p.obj("r_lfo", 540, 40, "r s6_l\\$1_lfo")
    p.obj("flf", 540, 80, "f")
    p.obj("mlf", 540, 120, "* 1")
    p.obj("r_on", 660, 40, "r s6_l\\$1_on")
    p.con("r_wet", 0, "fw", 0)
    p.con("fw", 0, "mw", 0)
    p.con("mw", 0, "fx", 1)
    p.con("r_del", 0, "fx", 2)
    p.con("r_fb", 0, "ffb", 0)
    p.con("ffb", 0, "mfb", 0)
    p.con("mfb", 0, "fx", 3)
    p.con("r_lfo", 0, "flf", 0)
    p.con("flf", 0, "mlf", 0)
    p.con("mlf", 0, "fx", 4)
    p.con("r_on", 0, "fx", 5)

    # --- sat (aussi sous CONTRASTE)
    p.obj("r_sat", 780, 40, "r s6_l\\$1_sat")
    p.obj("fs", 780, 80, "f")
    p.obj("ms", 780, 120, "* 1")
    p.con("r_sat", 0, "fs", 0)
    p.con("fs", 0, "ms", 0)
    p.con("ms", 0, "dist", 1)

    # --- filtre (hpf/lpf/flfo — flfo sous contraste léger)
    p.obj("r_hpf", 160, 200, "r s6_l\\$1_hpf")
    p.obj("r_lpf", 300, 200, "r s6_l\\$1_lpf")
    p.obj("r_flfo", 440, 200, "r s6_l\\$1_flfo")
    p.obj("ffo", 440, 240, "f")
    p.obj("mfo", 440, 280, "* 1")
    p.con("r_hpf", 0, "filt", 1)
    p.con("r_lpf", 0, "filt", 2)
    p.con("r_flfo", 0, "ffo", 0)
    p.con("ffo", 0, "mfo", 0)
    p.con("mfo", 0, "filt", 3)

    # CONTRASTE: facteur sur wet/fb/lfo/sat/flfo
    p.obj("r_con", 160, 320, "r s6_contraste_f")
    p.obj("ct", 160, 360, "t b b b b b f f f f f")
    p.con("r_con", 0, "ct", 0)
    p.con("ct", 9, "mw", 1)
    p.con("ct", 8, "mfb", 1)
    p.con("ct", 7, "mlf", 1)
    p.con("ct", 6, "ms", 1)
    p.con("ct", 5, "mfo", 1)
    p.con("ct", 4, "fw", 0)
    p.con("ct", 3, "ffb", 0)
    p.con("ct", 2, "flf", 0)
    p.con("ct", 1, "fs", 0)
    p.con("ct", 0, "ffo", 0)
    _w(p, "fx_router_06.pd")


# ---------------------------------------------------------------------------
def gen_install_mode_06():
    """INSTALL_MODE (L4): ON=1 masque moteur+debug, OFF=0 affiche tout.

    Sort la valeur `vis` (inverse du toggle); le patch parent la route vers
    ses messages `; pd-<subpatch> vis $1` (noms propres à chaque variante).
    """
    p = P(460, 200)
    p.obj("in_m", 40, 20, "inlet")
    p.obj("eq0", 40, 80, "== 0")
    p.obj("o_vis", 40, 150, "outlet")
    p.con("in_m", 0, "eq0", 0)
    p.con("eq0", 0, "o_vis", 0)
    p.text(140, 20, "INSTALL_MODE ON=1 -> vis 0 (masque) \\; OFF=0 -> vis 1;")
    _w(p, "install_mode_06.pd")


# ---------------------------------------------------------------------------
def gen_decode_4hp_06():
    """Copie isolée du decode 4HP proto 05 (référence figée)."""
    src = os.path.join(LIBDIR, "decode_4hp.pd")
    dst = os.path.join(LIBDIR, "decode_4hp_06.pd")
    shutil.copyfile(src, dst)
    print("OK lib: decode_4hp_06.pd (copie decode_4hp)")


def gen_decode_6hp_06():
    """Decode 5 canaux, géométrie 6HP actée (§3.6).

    Rectangle: 4 coins (canaux 1 2 4 5) + paire médiane du grand côté
    partagée sur le canal 6 (azimut 0 = face). Sortie carte 3 non utilisée.
    """
    az = PR.DECODE_6HP_AZ  # ordre canaux carte 1 2 4 5 6
    rows = []
    for a in az:
        r = math.radians(a)
        rows.append(f"1 {math.cos(r):.4f} {math.sin(r):.4f}")
    mtx = "matrix 5 3 " + " ".join(rows)
    p = P(640, 340)
    p.obj("in_w", 40, 40, "inlet~")
    p.obj("in_x", 40, 70, "inlet~")
    p.obj("in_y", 40, 100, "inlet~")
    p.obj("mtx", 200, 140, "mtx_*~ 5 3 100")
    for i in range(5):
        p.obj(f"o{i}", 40 + i * 110, 280, "outlet~")
        p.con("mtx", i, f"o{i}", 0)
    p.obj("lb", 40, 150, "loadbang")
    p.obj("dl", 40, 180, "delay 200")
    p.msg("m_mtx", 40, 220, mtx)
    p.con("lb", 0, "dl", 0)
    p.con("dl", 0, "m_mtx", 0)
    p.con("m_mtx", 0, "mtx", 0)
    p.con("in_w", 0, "mtx", 1)
    p.con("in_x", 0, "mtx", 2)
    p.con("in_y", 0, "mtx", 3)
    p.text(20, 10, "decode 6HP ordre 1 / 2D — rectangle + paire mediane grand cote;")
    p.text(20, 26, f"azimuts canaux 1 2 4 5 6: {' '.join(str(a) for a in az)} deg;")
    _w(p, "decode_6hp_06.pd")


def gen_decode_8hp_06():
    """Decode 8 canaux — octogone régulier, sorties carte 1..8."""
    az = PR.DECODE_8HP_AZ
    rows = []
    for a in az:
        r = math.radians(a)
        rows.append(f"1 {math.cos(r):.4f} {math.sin(r):.4f}")
    mtx = "matrix 8 3 " + " ".join(rows)
    p = P(900, 360)
    p.obj("in_w", 40, 40, "inlet~")
    p.obj("in_x", 40, 70, "inlet~")
    p.obj("in_y", 40, 100, "inlet~")
    p.obj("mtx", 200, 140, "mtx_*~ 8 3 100")
    for i in range(8):
        p.obj(f"o{i}", 20 + i * 105, 300, "outlet~")
        p.con("mtx", i, f"o{i}", 0)
    p.obj("lb", 40, 150, "loadbang")
    p.obj("dl", 40, 180, "delay 200")
    p.msg("m_mtx", 40, 220, mtx)
    p.con("lb", 0, "dl", 0)
    p.con("dl", 0, "m_mtx", 0)
    p.con("m_mtx", 0, "mtx", 0)
    p.con("in_w", 0, "mtx", 1)
    p.con("in_x", 0, "mtx", 2)
    p.con("in_y", 0, "mtx", 3)
    p.text(20, 10, "decode 8HP ordre 1 / 2D — octogone regulier;")
    p.text(20, 26, f"azimuts 1..8: {' '.join(str(a) for a in az)} deg;")
    _w(p, "decode_8hp_06.pd")


def gen_player_state_06():
    """Lecteur SONS/ proto 06 — généré depuis un scan de SONS/ (plus de liste
    codée en dur comme dans player_state 05).

    - Audit RMS: écarte les segments silencieux ou à trou >= 5 s (Q7);
    - slot vide -> repli sur les autres durées du même état;
    - arg $1 = loop (1: fin de fichier -> nouveau tirage même slot — Q7;
      0: one-shot pour les couches superposition);
    - `del 80` avant start (coupure <= 100 ms, Q7);
    - slot en entrée froide: le fichier ne change qu'au bang lecteur, gaté
      par changement d'état réel dans fsm_memory_06 (Q18/Q27);
    - outlet 1 = symbole nom de fichier (basename) pour le panneau VISU.
    - slots 0..11 = etat×3+durée (COURT/MOYEN/LONG) ;
    - slots 20..29 = pools exclusifs CORTEX 8HP (CORTEX_LAYER_MAP → B1..B8).
    """
    root = os.path.abspath(os.path.join(LIBDIR, "..", ".."))
    from .sons_audit import usable_files, usable_cortex_layer_pools
    u = usable_files(root)
    all_state = {si: sum((u[(si, di)] for di in range(3)), []) for si in range(4)}
    everything = sum(all_state.values(), [])
    if not everything:
        raise SystemExit("SONS/: aucun segment utilisable")

    n_cx = PR.MAX_LAYERS_8HP
    cx_pools = usable_cortex_layer_pools(root, n_layers=n_cx, n_baffles=8)
    # repli si B1..B8 absents: découpe MOYEN sans chevauchement
    moyen = u[(0, 1)] or all_state[0] or everything
    for li in range(n_cx):
        if not cx_pools[li]:
            if li < len(moyen):
                cx_pools[li] = [moyen[li]]
            else:
                cx_pools[li] = [moyen[li % len(moyen)]]

    # (slot_id, files) — outlets select dans cet ordre
    slot_specs = []
    for si in range(4):
        for di in range(3):
            slot_specs.append((si * 3 + di, u[(si, di)] or all_state[si] or everything))
    for li in range(n_cx):
        slot_specs.append((20 + li, cx_pools[li]))

    sel_args = " ".join(str(s) for s, _ in slot_specs)
    p = P(1100, max(900, 200 + len(slot_specs) * 55 + 80))
    p.text(20, 6, "player_state_06 - scan SONS/ + audit RMS + pools CORTEX B1..B8;")
    p.text(20, 22, "in0 bang=lecture \\, in1 slot froid \\, out0 audio \\, out1 nom sample;")
    p.text(20, 38, "slots 0..11 etat/duree \\; 20..29 CORTEX exclusifs \\; s6_play_reps = lectures avant swap;")
    p.obj("in_b", 40, 50, "inlet")
    p.obj("in_slot", 140, 50, "inlet")
    p.obj("out", 40, 860, "outlet~")
    p.obj("out_name", 200, 860, "outlet")
    p.obj("readsf", 640, 300, "readsf~")
    p.obj("gain", 640, 340, "*~ 0.9")
    p.con("readsf", 0, "gain", 0)
    p.con("gain", 0, "out", 0)
    p.obj("delay0", 40, 90, "delay 0")
    p.obj("tb", 40, 120, "t b")
    p.obj("f_slot", 140, 120, "f")
    p.obj("sel_slot", 40, 160, f"select {sel_args}")
    p.obj("del_start", 640, 180, "del 80")
    p.msg("m_start", 640, 220, "start")
    p.obj("spig_loop", 760, 90, "spigot \\$1")
    p.msg("m_clear", 760, 130, "symbol none")
    p.con("in_b", 0, "delay0", 0)
    p.con("delay0", 0, "tb", 0)
    p.con("tb", 0, "f_slot", 0)
    p.obj("t_slot", 200, 90, "t f b")
    p.con("in_slot", 0, "t_slot", 0)
    p.con("t_slot", 0, "f_slot", 1)
    p.con("f_slot", 0, "sel_slot", 0)
    p.con("del_start", 0, "m_start", 0)
    p.con("m_start", 0, "readsf", 0)
    p.con("readsf", 1, "spig_loop", 0)
    p.con("spig_loop", 0, "delay0", 0)
    # play_reps: nb lectures d'un même fichier avant nouveau tirage (HIPPO=3)
    p.obj("r_reps", 760, 20, "r s6_play_reps")
    p.obj("f_reps", 760, 50, "f 1")
    p.obj("lb_reps", 860, 180, "loadbang")
    p.msg("m_reps1", 860, 210, "1")
    p.con("lb_reps", 0, "m_reps1", 0)
    p.con("m_reps1", 0, "f_reps", 1)
    p.con("r_reps", 0, "f_reps", 1)
    # one-shot: clear displayed name at EOF (gate = not loop)
    p.obj("lb_loop", 860, 20, "loadbang")
    p.obj("f_loop", 860, 50, "f \\$1")
    p.obj("eq_loop0", 860, 90, "== 0")
    p.obj("spig_clr", 860, 130, "spigot")
    p.con("lb_loop", 0, "f_loop", 0)
    p.con("f_loop", 0, "eq_loop0", 0)
    p.con("eq_loop0", 0, "spig_clr", 1)
    p.con("readsf", 1, "spig_clr", 0)
    p.con("spig_clr", 0, "m_clear", 0)
    p.con("m_clear", 0, "out_name", 0)

    for oi, (s, files) in enumerate(slot_specs):
        n = len(files)
        y = 200 + oi * 55
        p.obj(f"sel{s}", 240, y, "select " + " ".join(str(j) for j in range(n)))
        p.con("sel_slot", oi, "del_start", 0)
        if n >= 2:
            # Compteur play_reps: 1..(reps-1) rejoue le même idx ;
            # cnt==1 ou cnt>reps → nouveau tirage (sans répétition immédiate).
            p.obj(f"tt{s}", 20, y, "t b b")
            p.obj(f"fc{s}", 20, y + 18, "f 0")
            p.obj(f"p1{s}", 20, y + 36, "+ 1")
            p.obj(f"tc{s}", 70, y + 18, "t f f")
            p.obj(f"tb{s}", 70, y + 36, "t b f")
            p.obj(f"gt{s}", 130, y + 18, ">")
            p.obj(f"sgt{s}", 130, y + 36, "sel 1")
            p.obj(f"eq1{s}", 180, y + 18, "== 1")
            p.obj(f"se1{s}", 180, y + 36, "sel 1")
            p.obj(f"fi{s}", 150, y, "f 0")
            p.obj(f"m1{s}", 100, y, "1")
            p.obj(f"tr{s}", 60, y, "t b b")
            p.obj(f"fp{s}", 100, y + 55, "f 0")
            p.obj(f"rnd{s}", 60, y + 55, f"random {n - 1}")
            p.obj(f"a1{s}", 60, y + 72, "+ 1")
            p.obj(f"ad{s}", 110, y + 72, "+")
            p.obj(f"md{s}", 110, y + 55, f"% {n}")
            p.obj(f"tf{s}", 160, y + 72, "t f f")
            p.con("sel_slot", oi, f"tt{s}", 0)
            p.con(f"tt{s}", 0, f"fc{s}", 0)
            p.con(f"fc{s}", 0, f"p1{s}", 0)
            p.con(f"p1{s}", 0, f"tc{s}", 0)
            p.con(f"tc{s}", 1, f"fc{s}", 1)
            p.con(f"tc{s}", 0, f"tb{s}", 0)
            p.con(f"tb{s}", 0, "f_reps", 0)
            p.con("f_reps", 0, f"gt{s}", 1)
            p.con(f"tb{s}", 1, f"gt{s}", 0)
            p.con(f"gt{s}", 0, f"sgt{s}", 0)
            # cnt > reps → reset à 1 + nouveau tirage
            p.con(f"sgt{s}", 1, f"m1{s}", 0)
            p.con(f"m1{s}", 0, f"fc{s}", 1)
            p.con(f"sgt{s}", 1, f"tr{s}", 0)
            # cnt <= reps → si ==1 nouveau, sinon reuse idx
            p.con(f"sgt{s}", 0, f"eq1{s}", 0)
            p.con(f"eq1{s}", 0, f"se1{s}", 0)
            p.con(f"se1{s}", 1, f"tr{s}", 0)
            p.con(f"se1{s}", 0, f"fi{s}", 0)
            p.con(f"fi{s}", 0, f"sel{s}", 0)
            # tirage sans répétition immédiate
            p.con(f"tr{s}", 1, f"fp{s}", 0)
            p.con(f"fp{s}", 0, f"ad{s}", 1)
            p.con(f"tr{s}", 0, f"rnd{s}", 0)
            p.con(f"rnd{s}", 0, f"a1{s}", 0)
            p.con(f"a1{s}", 0, f"ad{s}", 0)
            p.con(f"ad{s}", 0, f"md{s}", 0)
            p.con(f"md{s}", 0, f"tf{s}", 0)
            p.con(f"tf{s}", 1, f"fp{s}", 1)
            p.con(f"tf{s}", 1, f"fi{s}", 1)
            p.con(f"tf{s}", 0, f"sel{s}", 0)
            # reset compteur si changement de slot
            p.msg(f"z{s}", 200, y + 55, "0")
            p.con("t_slot", 1, f"z{s}", 0)
            p.con(f"z{s}", 0, f"fc{s}", 1)
        else:
            p.obj(f"rnd{s}", 140, y, f"random {n}")
            p.con("sel_slot", oi, f"rnd{s}", 0)
            p.con(f"rnd{s}", 0, f"sel{s}", 0)
        for j, rel in enumerate(files):
            base = os.path.basename(rel).replace(" ", "\\ ")
            p.msg(f"op{s}_{j}", 420, y + j, f"open {rel}")
            p.msg(f"nm{s}_{j}", 620, y + j, f"symbol {base}")
            p.con(f"sel{s}", j, f"op{s}_{j}", 0)
            p.con(f"sel{s}", j, f"nm{s}_{j}", 0)
            p.con(f"op{s}_{j}", 0, "readsf", 0)
            p.con(f"nm{s}_{j}", 0, "out_name", 0)
    _w(p, "player_state_06.pd")


def gen_visu_cerveau_06():
    """Historique cerveau: inlet=etat (0..3)."""
    p = P(1200, 760)
    p.obj("in_st", 40, 20, "inlet")
    p.text(200, 20, "visu_cerveau_06 — etat courant + historique 8 lignes;")

    p.obj("trg", 40, 60, "t f b")
    p.con("in_st", 0, "trg", 0)

    p.obj("tmr", 900, 60, "timer")
    p.obj("met", 1020, 60, "metro 200")
    p.obj("lb", 1020, 20, "loadbang")
    p.msg("m_on", 1020, 40, "1")
    p.obj("div_s", 1020, 100, "/ 1000")
    p.obj("s_dur", 1020, 140, "s s6_etat_dur")
    p.con("lb", 0, "m_on", 0)
    p.con("m_on", 0, "met", 0)
    p.con("met", 0, "tmr", 1)
    p.con("tmr", 0, "div_s", 0)
    p.con("div_s", 0, "s_dur", 0)

    for i in range(8):
        x = 40 + i * 120
        p.obj(f"hn{i}", x, 400, "symbol")
        p.obj(f"hd{i}", x, 440, "f 0")
        p.obj(f"tn{i}", x, 480, "t a a")
        p.obj(f"td{i}", x, 520, "t f f")
        p.obj(f"s_hn{i}", x, 560, f"s s6_hist_nom{i}")
        p.obj(f"s_hd{i}", x, 600, f"s s6_hist_dur{i}")
        p.con(f"hn{i}", 0, f"tn{i}", 0)
        p.con(f"hd{i}", 0, f"td{i}", 0)
        p.con(f"tn{i}", 0, f"s_hn{i}", 0)
        p.con(f"td{i}", 0, f"s_hd{i}", 0)

    for i in range(7):
        p.con(f"tn{i}", 1, f"hn{i + 1}", 1)
        p.con(f"td{i}", 1, f"hd{i + 1}", 1)

    p.obj("sym_prev", 40, 200, "symbol")
    p.obj("f_ready", 200, 100, "f 0")
    p.obj("spig_push", 200, 140, "spigot")
    p.obj("push_t", 200, 180, "t b b b b b b b b b b")
    p.con("trg", 1, "f_ready", 0)
    p.con("f_ready", 0, "spig_push", 0)
    p.con("spig_push", 0, "push_t", 0)

    p.obj("ask_dur", 420, 180, "t b")
    p.obj("div_h", 420, 220, "/ 1000")
    p.obj("f_pdur", 420, 260, "f")
    p.con("push_t", 9, "ask_dur", 0)
    p.con("ask_dur", 0, "tmr", 1)
    p.con("tmr", 0, "div_h", 0)
    p.con("div_h", 0, "f_pdur", 1)

    for k in range(7):
        src = 6 - k
        p.con("push_t", 8 - k, f"hn{src}", 0)
        p.con("push_t", 8 - k, f"hd{src}", 0)

    p.con("push_t", 1, "sym_prev", 0)
    p.con("sym_prev", 0, "hn0", 1)
    p.con("push_t", 1, "f_pdur", 0)
    p.con("f_pdur", 0, "hd0", 1)

    p.obj("emit_t", 40, 640, "t b b b b b b b b")
    p.con("push_t", 0, "emit_t", 0)
    for i in range(8):
        p.con("emit_t", i, f"hn{i}", 0)
        p.con("emit_t", i, f"hd{i}", 0)

    # maj etat courant: bang reset timer, float -> sel noms
    p.obj("aft", 700, 200, "t f b")
    p.con("trg", 0, "aft", 0)
    p.con("aft", 1, "tmr", 0)           # bang = reset timer
    p.msg("m_ready1", 700, 240, "1")
    p.con("aft", 1, "m_ready1", 0)
    p.con("m_ready1", 0, "f_ready", 1)

    p.obj("sel_nm", 700, 280, "sel 0 1 2 3")
    p.obj("s_nom", 700, 420, "s s6_etat_nom")
    p.con("aft", 0, "sel_nm", 0)         # float = nouvel etat
    for i, nm in enumerate(PR.ETAT_NOMS):
        p.msg(f"nm{i}", 700, 320 + i * 22, f"symbol {nm}")
        p.con("sel_nm", i, f"nm{i}", 0)
        p.con(f"nm{i}", 0, "s_nom", 0)
        p.con(f"nm{i}", 0, "sym_prev", 0)

    p.obj("lb2", 40, 700, "loadbang")
    p.msg("m_none", 140, 700, "symbol none")
    p.msg("m_z", 280, 700, "0")
    p.con("lb2", 0, "m_none", 0)
    p.con("lb2", 0, "m_z", 0)
    for i in range(8):
        p.con("m_none", 0, f"hn{i}", 1)
        p.con("m_none", 0, f"s_hn{i}", 0)
        p.con("m_z", 0, f"hd{i}", 1)
        p.con("m_z", 0, f"s_hd{i}", 0)

    _w(p, "visu_cerveau_06.pd")


def ensure():
    gen_fsm_memory_06()
    gen_fsm_presets_06()
    # Variante 8HP: cycle artiste CORTEX→HIPPO→RECON, jusqu'à 6 couches
    gen_fsm_memory_06("fsm_memory_06_8hp.pd",
                      fsm_n=PR.FSM_N_8HP, max_layers=PR.MAX_LAYERS_8HP,
                      cycle1=PR.CYCLE1_8HP)
    gen_fsm_presets_06("fsm_presets_06_8hp.pd", presets=PR.PRESETS_8HP)
    gen_hippo_motion_06()
    gen_spatial_router_06()
    gen_fx_distort_06()
    gen_fx_filter_06()
    gen_fx_router_06()
    gen_install_mode_06()
    gen_decode_4hp_06()
    gen_decode_6hp_06()
    gen_decode_8hp_06()
    gen_player_state_06()
    gen_visu_cerveau_06()
