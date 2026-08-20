"""Génère les abstractions Pd Proto 07 (pd/lib/*_07*.pd).

N'écrit QUE des fichiers *_07. Réutilise le DSP 06 (fx_router_06,
spatial_router_06, decode_8hp_06, visu_cerveau_06, install_mode_06).
"""
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "scripts"))
from shared.pdbuild import P
from . import presets07 as PR
from . import sons_audit07 as audit

LIBDIR = os.path.join(_REPO, "pd", "lib")


def _w(p, fname):
    p.write(os.path.join(LIBDIR, fname))
    print(f"OK lib: {fname}")


def gen_fsm_memory_07(fname="fsm_memory_07_8hp.pd", fsm_n=None, max_layers=None,
                      cycle1=None):
    """FSM 07: cycle 1 Cortex 40s → Hippo 50s → Recon 120s.

    Extra vs 06: hold Cortex (s6_cortex_hold), pique Boucle 15% en cycle libre.
    """
    max_layers = max_layers or PR.MAX_LAYERS_8HP
    fsm_n = PR.fsm_n_padded(fsm_n or PR.FSM_N_8HP, max_layers)
    cycle1 = cycle1 if cycle1 is not None else PR.CYCLE1_8HP
    n_c1 = len(cycle1)
    first_dur = cycle1[0][1]
    out_names = (["o_state", "o_bpre", "o_n"]
                 + [f"o_d{i}" for i in range(max_layers)]
                 + ["o_bply"])
    out_y = 820 + max_layers * 35 + 40
    p = P(max(980, 40 + len(out_names) * 110), out_y + 60)
    p.obj("in_auto", 40, 20, "inlet")
    p.obj("in_force", 200, 20, "inlet")
    p.obj("in_sess", 340, 20, "inlet")
    for i, nm in enumerate(out_names):
        p.obj(nm, 40 + i * 110, out_y, "outlet")

    p.obj("a_t", 40, 60, "t f f f f")
    p.obj("sel_a1", 40, 100, "sel 1")
    p.obj("sel_a0", 110, 100, "sel 0")
    p.obj("f_durlast", 40, 140, f"f {first_dur}")
    p.msg("m_stop", 110, 140, "stop")
    p.obj("dur_t", 320, 100, "t b f f")
    p.obj("delay_main", 320, 150, f"delay {first_dur}")
    p.obj("spig_adv", 320, 190, "spigot")
    p.con("in_auto", 0, "a_t", 0)
    p.con("a_t", 3, "spig_adv", 1)
    p.con("a_t", 1, "sel_a1", 0)
    p.con("a_t", 0, "sel_a0", 0)
    p.con("sel_a1", 0, "f_durlast", 0)
    p.con("f_durlast", 0, "dur_t", 0)
    p.con("sel_a0", 0, "m_stop", 0)
    p.con("m_stop", 0, "delay_main", 0)
    p.con("dur_t", 2, "f_durlast", 1)
    p.con("dur_t", 1, "delay_main", 1)
    p.con("dur_t", 0, "delay_main", 0)
    p.con("delay_main", 0, "spig_adv", 0)

    p.obj("frc_t", 200, 60, "t f b")
    p.con("in_force", 0, "frc_t", 0)
    p.con("frc_t", 1, "m_stop", 0)

    p.obj("lb_t", 620, 100, "t b b")
    p.obj("delay_reset", 620, 140, f"delay {PR.RESET_MS}")
    p.obj("drt", 620, 180, "t b b")
    p.obj("spig_rst", 620, 220, "spigot")
    p.con("in_sess", 0, "lb_t", 0)
    p.con("lb_t", 1, "delay_reset", 0)
    p.con("delay_reset", 0, "drt", 0)
    p.con("drt", 1, "delay_reset", 0)
    p.con("drt", 0, "spig_rst", 0)
    p.con("a_t", 2, "spig_rst", 1)

    p.obj("start_t", 460, 260, "t b b b")
    p.msg("m_st0", 560, 300, "0")
    p.msg("m_c11", 620, 300, "1")
    p.con("lb_t", 0, "start_t", 0)
    p.con("spig_rst", 0, "start_t", 0)
    p.con("start_t", 2, "m_st0", 0)
    p.con("start_t", 1, "m_c11", 0)

    p.obj("f_c1", 60, 260, "f 1")
    p.obj("selc1", 60, 300, "sel 1 0")
    p.con("spig_adv", 0, "f_c1", 0)
    p.con("start_t", 0, "f_c1", 0)
    p.con("m_c11", 0, "f_c1", 1)
    p.con("f_c1", 0, "selc1", 0)

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
            p.con(f"c1t{k}", 2, "m_c1clr", 0)
            p.con(f"c1t{k}", 1, "m_cnt0", 0)
            p.con(f"c1t{k}", 0, f"c1s{k}", 0)
        else:
            p.con(f"c1t{k}", 1, f"c1d{k}", 0)
            p.con(f"c1t{k}", 0, f"c1s{k}", 0)
        p.con(f"c1d{k}", 0, "dur_t", 0)
    p.con("m_c1clr", 0, "f_c1", 1)

    p.obj("free_t", 180, 300, "t b b")
    p.obj("rnd_dur", 290, 340, f"random {PR.FREE_DUR_RAND}")
    p.obj("pl15", 290, 380, f"+ {PR.FREE_DUR_BASE}")
    p.obj("f_cnt", 180, 340, "f 0")
    p.obj("cp1", 180, 380, "+ 1")
    p.obj("cnt_t", 180, 420, "t f f")
    p.obj("mod5", 180, 460, f"% {PR.FREE_CORTEX_EVERY}")
    p.obj("sel5", 180, 500, "sel 0")
    p.msg("m_cx", 180, 540, "0")
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
    p.con("cd_t", 2, "f_last", 0)
    p.con("f_last", 0, "neq", 1)
    p.con("cd_t", 1, "neq", 0)
    p.con("neq", 0, "spig_pl", 1)
    p.con("cd_t", 0, "f_last", 1)
    p.con("cd_t", 0, "f_cur", 1)
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
    p.con("goto_t", 0, "o_bply", 0)

    # présence: hold Cortex = stop timer ; relâche = relance durée courante
    p.obj("r_hold", 800, 40, "r s6_cortex_hold")
    p.obj("ht", 800, 70, "t f f")
    p.obj("hs1", 800, 100, "sel 1")
    p.obj("hs0", 880, 100, "sel 0")
    p.con("r_hold", 0, "ht", 0)
    p.con("ht", 0, "hs1", 0)
    p.con("ht", 1, "hs0", 0)
    p.con("hs1", 0, "m_stop", 0)
    p.con("hs0", 0, "f_durlast", 0)

    p.text(800, 140, "07 hold Cortex + Boucle 15pct cycles libres")
    _w(p, fname)


def gen_fsm_presets_07(fname="fsm_presets_07_8hp.pd", presets=None):
    presets = presets or PR.PRESETS_8HP
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
    p.obj("lb_s", 40, 20, "loadbang")
    p.obj("fid", 40, 40, "f \\$0")
    p.msg("sd0", 40, 50, "seed \\$1")
    p.obj("tb_rnd", 20, 50, "t b")
    p.con("lb_s", 0, "fid", 0)
    p.con("fid", 0, "sd0", 0)
    p.con("sd0", 0, "rnd3", 0)
    p.con("in_s", 0, "mul3p", 0)
    p.con("mul3p", 0, "padd", 1)
    p.con("in_b", 0, "tb_rnd", 0)
    p.con("tb_rnd", 0, "rnd3", 0)
    p.con("rnd3", 0, "padd", 0)
    p.con("padd", 0, "pt", 0)
    p.con("pt", 1, "o_var", 0)
    p.con("pt", 2, "f_last", 1)
    p.con("pt", 0, "sel_b", 0)
    p.con("r_ref", 0, "f_last", 0)
    p.con("f_last", 0, "sel_b", 0)
    p.text(300, 40, "banques 07: etat*3+variante -> s6_*")
    p.obj("pipefx", 40, 220, "pipe 500")
    p.obj("sel_bfx", 40, 250, "sel 0 1 2 3 4 5 6 7 8 9 10 11")
    p.con("pt", 0, "pipefx", 0)
    p.con("pipefx", 0, "sel_bfx", 0)
    for s in range(4):
        for v in range(3):
            bid = s * 3 + v
            body = "\\; " + PR.bank_msg_body(presets[s][v], PR.LAYER_FIELDS_NOW)
            p.msg(f"bank{bid}", 300, 60 + bid * 44, body)
            p.con("sel_b", bid, f"bank{bid}", 0)
            tail = "\\; " + PR.bank_msg_body(presets[s][v], PR.LAYER_FIELDS_TAIL)
            p.msg(f"bankfx{bid}", 700, 60 + bid * 44, tail)
            p.con("sel_bfx", bid, f"bankfx{bid}", 0)
    _w(p, fname)


def gen_hippo_motion_07():
    """Circulation 0.8-2.2 s: local / saut. xfade court."""
    p = P(980, 640)
    p.text(20, 10, "hippo_motion_07 circulation rapide local saut")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel_h", 40, 70, "sel 1")
    p.msg("m_stop", 140, 100, "stop")
    p.obj("d_ent", 40, 100, "delay 80")
    p.obj("met", 40, 140, "metro 3500")
    p.con("r_et", 0, "sel_h", 0)
    p.con("sel_h", 0, "d_ent", 0)
    p.con("d_ent", 0, "met", 0)
    p.con("sel_h", 1, "m_stop", 0)
    p.con("m_stop", 0, "met", 0)

    p.obj("ent", 40, 180, "t b b b b b")
    p.con("d_ent", 0, "ent", 0)
    steps = [1100, 1600, 2200, 1400]
    modes = [4, 2, 4, 2]
    senss = [0, 1, 1, 0]
    for i in range(1, 5):
        y = 160 + i * 28
        p.msg(f"mm{i}", 200, y, str(modes[i - 1]))
        p.msg(f"mst{i}", 320, y, str(steps[i - 1]))
        p.msg(f"mxf{i}", 440, y, "35")
        p.msg(f"msn{i}", 560, y, str(senss[i - 1]))
        p.obj(f"sm{i}", 640, y, f"s s6_l{i}_mode")
        p.obj(f"ss{i}", 720, y, f"s s6_l{i}_step")
        p.obj(f"sx{i}", 800, y, f"s s6_l{i}_xfade")
        p.obj(f"sn{i}", 880, y, f"s s6_l{i}_sens")
        p.con(f"mm{i}", 0, f"sm{i}", 0)
        p.con(f"mst{i}", 0, f"ss{i}", 0)
        p.con(f"mxf{i}", 0, f"sx{i}", 0)
        p.con(f"msn{i}", 0, f"sn{i}", 0)
        p.con("ent", i - 1, f"mm{i}", 0)
        p.con("ent", i - 1, f"mst{i}", 0)
        p.con("ent", i - 1, f"mxf{i}", 0)
        p.con("ent", i - 1, f"msn{i}", 0)

    p.msg("mm9", 200, 310, "4")
    p.msg("mst9", 320, 310, "1500")
    p.msg("mxf9", 440, 310, "35")
    p.obj("sm9", 640, 310, "s s6_l9_mode")
    p.obj("ss9", 720, 310, "s s6_l9_step")
    p.obj("sx9", 800, 310, "s s6_l9_xfade")
    p.con("mm9", 0, "sm9", 0)
    p.con("mst9", 0, "ss9", 0)
    p.con("mxf9", 0, "sx9", 0)
    p.con("ent", 4, "mm9", 0)
    p.con("ent", 4, "mst9", 0)
    p.con("ent", 4, "mxf9", 0)
    p.msg("m0_l9", 220, 100, "0")
    p.con("sel_h", 1, "m0_l9", 0)
    p.con("m0_l9", 0, "sm9", 0)

    # tick: d'abord nouvelle vitesse + mode, ensuite une seule couche, puis intervalle
    p.obj("tb_m", 40, 360, "t b b b")
    p.con("met", 0, "tb_m", 0)
    p.obj("rst", 200, 360, "random 1400")
    p.obj("pst", 200, 390, "+ 800")
    p.con("tb_m", 0, "rst", 0)
    p.con("rst", 0, "pst", 0)
    p.obj("rmd", 360, 360, "random 5")
    p.obj("smd", 360, 390, "sel 0 1 2 3 4")
    p.msg("md4a", 500, 360, "4")
    p.msg("md4b", 500, 385, "4")
    p.msg("md2a", 500, 410, "2")
    p.msg("md2b", 500, 435, "2")
    p.msg("md0", 500, 460, "4")
    p.con("tb_m", 0, "rmd", 0)
    p.con("rmd", 0, "smd", 0)
    p.con("smd", 0, "md4a", 0)
    p.con("smd", 1, "md4b", 0)
    p.con("smd", 2, "md2a", 0)
    p.con("smd", 3, "md2b", 0)
    p.con("smd", 4, "md0", 0)
    p.obj("rl", 40, 400, "random 4")
    p.obj("pl", 40, 430, "+ 1")
    p.obj("sell", 40, 460, "sel 1 2 3 4")
    p.con("tb_m", 1, "rl", 0)
    p.con("rl", 0, "pl", 0)
    p.con("pl", 0, "sell", 0)
    for i in range(1, 5):
        p.obj(f"fs{i}", 200, 430 + i * 24, "f 1400")
        p.obj(f"fm{i}", 360, 490 + i * 24, "f 4")
        p.con("pst", 0, f"fs{i}", 1)
        p.con("md4a", 0, f"fm{i}", 1)
        p.con("md4b", 0, f"fm{i}", 1)
        p.con("md2a", 0, f"fm{i}", 1)
        p.con("md2b", 0, f"fm{i}", 1)
        p.con("md0", 0, f"fm{i}", 1)
        p.con("sell", i - 1, f"fs{i}", 0)
        p.con("sell", i - 1, f"fm{i}", 0)
        p.con(f"fs{i}", 0, f"ss{i}", 0)
        p.con(f"fm{i}", 0, f"sm{i}", 0)
    p.obj("rsn", 40, 500, "random 2")
    p.con("tb_m", 1, "rsn", 0)
    p.con("rsn", 0, "sn1", 0)
    p.obj("rit", 40, 540, "random 2500")
    p.obj("pit", 40, 570, "+ 2000")
    p.con("tb_m", 2, "rit", 0)
    p.con("rit", 0, "pit", 0)
    p.con("pit", 0, "met", 1)
    p.text(20, 610, "0.8-2.2s entre baffles - metro suivant 2-4.5s")
    _w(p, "hippo_motion_07.pd")


def gen_amb_route_07():
    """Route le lit d'ambiance vers 1 HP (1–8), fixe pendant le tour."""
    p = P(900, 520)
    p.text(20, 10, "amb_route_07 1 HP dedie index s6_amb_hp")
    p.obj("in_a", 40, 40, "inlet~")
    p.obj("r_hp", 200, 40, "r s6_amb_hp")
    p.obj("hp_t", 200, 70, "t f b")
    p.obj("sel", 200, 110, "sel 1 2 3 4 5 6 7 8")
    p.con("r_hp", 0, "hp_t", 0)
    p.con("hp_t", 1, "z", 0)
    p.msg("z", 40, 110, "0")
    p.con("hp_t", 0, "sel", 0)
    for k in range(8):
        x = 40 + k * 100
        p.msg(f"m1_{k}", 320, 110 + k * 28, "1")
        p.obj(f"pk{k}", x, 200, "pack 0 3")
        p.obj(f"ln{k}", x, 230, "line~")
        p.obj(f"g{k}", x, 270, "*~")
        p.obj(f"o{k}", x, 480, "outlet~")
        p.con("z", 0, f"pk{k}", 0)
        p.con("sel", k, f"m1_{k}", 0)
        p.con(f"m1_{k}", 0, f"pk{k}", 0)
        p.con(f"pk{k}", 0, f"ln{k}", 0)
        p.con(f"ln{k}", 0, f"g{k}", 1)
        p.con("in_a", 0, f"g{k}", 0)
        p.con(f"g{k}", 0, f"o{k}", 0)
    p.obj("lb", 520, 40, "loadbang")
    p.msg("d5", 520, 70, "5")
    p.obj("s_init", 520, 100, "s s6_amb_hp")
    p.con("lb", 0, "d5", 0)
    p.con("d5", 0, "s_init", 0)
    _w(p, "amb_route_07.pd")


def gen_cortex_ctrl_07():
    """Cortex: 6 frag + 5 nappes. LPF 1500 qui bouge 500-2000. Hippo: LPF L9."""
    p = P(920, 560)
    p.text(20, 8, "cortex_ctrl_07 LPF 500-2000 sur L1-L6")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 0 1")
    p.con("r_et", 0, "sel", 0)

    p.obj("tb", 40, 110, "t b b")
    p.con("sel", 0, "tb", 0)
    p.msg("n6", 40, 150, "6")
    p.obj("s_n", 40, 190, "s s6_cortex_n")
    p.con("tb", 0, "n6", 0)
    p.con("n6", 0, "s_n", 0)
    p.obj("lb_n", 40, 230, "loadbang")
    p.con("lb_n", 0, "n6", 0)

    p.obj("dcx", 200, 110, "delay 60")
    p.msg("dry", 200, 150,
          "\\; s6_l9_lpf 18000 \\; s6_l9_wet 0 \\; s6_l9_on 0 \\; s6_l9_sat 0 \\; s6_l9_hpf 30 \\; s6_l9_fb 0 \\; s6_l9_flfo 0 \\; s6_l9_del 40 \\; s6_l9_mode 0")
    p.con("tb", 1, "dcx", 0)
    p.con("dcx", 0, "dry", 0)

    p.obj("dhp", 200, 230, "delay 60")
    p.msg("hplpf", 200, 270,
          "\\; s6_l9_lpf 5000 \\; s6_l9_wet 0 \\; s6_l9_on 0 \\; s6_l9_sat 0 \\; s6_l9_hpf 40 \\; s6_l9_fb 0 \\; s6_l9_flfo 0")
    p.con("sel", 1, "dhp", 0)
    p.con("dhp", 0, "hplpf", 0)

    p.obj("selcx", 40, 280, "sel 0")
    p.con("r_et", 0, "selcx", 0)
    p.msg("go", 40, 310, "bang")
    p.msg("stp", 120, 310, "stop")
    p.obj("mf", 40, 340, "metro 50")
    p.con("selcx", 0, "go", 0)
    p.con("selcx", 1, "stp", 0)
    p.con("go", 0, "mf", 0)
    p.con("stp", 0, "mf", 0)
    for i in range(6):
        x = 40 + i * 140
        hz = 0.07 + i * 0.02
        p.obj(f"osc{i}", x, 380, f"osc~ {hz:.3f}")
        p.obj(f"amp{i}", x, 410, "*~ 750")
        p.obj(f"off{i}", x, 440, "+~ 1250")
        p.obj(f"sn{i}", x, 470, "snapshot~")
        p.obj(f"cl{i}", x, 490, "clip 500 2000")
        p.obj(f"sl{i}", x, 510, f"s s6_l{i + 1}_lpf")
        p.con(f"osc{i}", 0, f"amp{i}", 0)
        p.con(f"amp{i}", 0, f"off{i}", 0)
        p.con(f"off{i}", 0, f"sn{i}", 0)
        p.con("mf", 0, f"sn{i}", 0)
        p.con(f"sn{i}", 0, f"cl{i}", 0)
        p.con(f"cl{i}", 0, f"sl{i}", 0)
    _w(p, "cortex_ctrl_07.pd")


def gen_presence_07():
    """Piezo/micro + rms_sim. Jamais vers les HP. Hold Cortex si énergie basse."""
    p = P(720, 480)
    p.text(20, 8, "presence_07 INPUT_ON + SIM - adc jamais vers dac")
    p.obj("r_on", 40, 40, "r s6_input_on")
    p.obj("r_sim", 160, 40, "r s6_rms_sim")
    p.obj("r_et", 280, 40, "r s6_etat")
    p.obj("f_on", 40, 70, "f 0")
    p.obj("f_sim", 160, 70, "f 0")
    p.obj("f_et", 280, 70, "f 0")
    p.con("r_on", 0, "f_on", 1)
    p.con("r_sim", 0, "f_sim", 1)
    p.con("r_et", 0, "f_et", 1)

    p.obj("adc", 40, 110, "adc~")
    p.obj("mix", 40, 150, "+~")
    p.obj("env", 40, 190, "env~ 2048")
    p.obj("sc", 40, 230, "/ 100")
    p.con("adc", 0, "mix", 0)
    p.con("adc", 1, "mix", 1)
    p.con("mix", 0, "env", 0)
    p.con("env", 0, "sc", 0)

    p.obj("met", 200, 110, "metro 250")
    p.obj("sel_sim", 200, 140, "sel 1")
    p.msg("sim_stop", 280, 140, "stop")
    p.obj("sp_sim", 200, 180, "spigot")
    p.obj("rnd", 200, 220, "random 100")
    p.obj("div", 200, 250, "/ 100")
    p.con("r_sim", 0, "sel_sim", 0)
    p.con("sel_sim", 0, "met", 0)
    p.con("sel_sim", 1, "sim_stop", 0)
    p.con("sim_stop", 0, "met", 0)
    p.obj("eqs", 320, 180, "== 1")
    p.con("r_sim", 0, "eqs", 0)
    p.con("eqs", 0, "sp_sim", 1)
    p.con("met", 0, "sp_sim", 0)
    p.obj("tb_sim", 200, 205, "t b")
    p.con("sp_sim", 0, "tb_sim", 0)
    p.con("tb_sim", 0, "rnd", 0)
    p.con("rnd", 0, "div", 0)

    p.obj("eq_on", 40, 270, "== 1")
    p.obj("sp_adc", 40, 300, "spigot")
    p.con("r_on", 0, "eq_on", 0)
    p.con("eq_on", 0, "sp_adc", 1)
    p.con("sc", 0, "sp_adc", 0)

    p.obj("en", 120, 330, "t f f")
    p.con("sp_adc", 0, "en", 0)
    p.con("div", 0, "en", 0)

    p.obj("s_rms", 120, 360, "s s6_presence_rms")
    p.con("en", 1, "s_rms", 0)

    # si Cortex et énergie < 0.12 → hold ; si > 0.45 → relâche (favorise sortie)
    p.obj("eq_cx", 280, 110, "== 0")
    p.obj("sp_cx", 280, 140, "spigot")
    p.con("r_et", 0, "eq_cx", 0)
    p.con("eq_cx", 0, "sp_cx", 1)
    p.con("en", 0, "sp_cx", 0)
    p.obj("lt", 280, 180, "< 0.12")
    p.obj("gt", 400, 180, "> 0.45")
    p.obj("selt", 280, 220, "sel 1")
    p.obj("selg", 400, 220, "sel 1")
    p.msg("h1", 280, 260, "1")
    p.msg("h0", 400, 260, "0")
    p.obj("s_h", 280, 300, "s s6_cortex_hold")
    p.con("sp_cx", 0, "lt", 0)
    p.con("sp_cx", 0, "gt", 0)
    p.con("lt", 0, "selt", 0)
    p.con("gt", 0, "selg", 0)
    p.con("selt", 0, "h1", 0)
    p.con("selg", 0, "h0", 0)
    p.con("h1", 0, "s_h", 0)
    p.con("h0", 0, "s_h", 0)
    # hors Cortex: jamais hold
    p.obj("sel_n", 520, 110, "sel 0")
    p.con("r_et", 0, "sel_n", 0)
    p.con("sel_n", 1, "h0", 0)
    p.text(20, 400, "pas de cable adc vers dac (anti larsen)")
    _w(p, "presence_07.pd")


def gen_recon_pulse_07():
    """En Reconstruction: bang périodique couche 2 = interruptions COURT."""
    p = P(480, 260)
    p.text(20, 8, "recon_pulse_07 interrupts 1-5 s sur couche 2")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 2")
    p.msg("off", 140, 100, "stop")
    p.obj("met", 40, 140, "metro 4500")
    p.obj("s_b", 40, 180, "s s6_recon_bang")
    p.con("r_et", 0, "sel", 0)
    p.con("sel", 0, "met", 0)
    p.con("sel", 1, "off", 0)
    p.con("off", 0, "met", 0)
    p.con("met", 0, "s_b", 0)
    _w(p, "recon_pulse_07.pd")


def gen_hippo_assoc_07():
    """A déclenche B: bangs décalés couches 3–4. Crochet tags vide."""
    p = P(560, 300)
    p.text(20, 8, "hippo_assoc_07 A vers B hasard - crochet tags vide")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 1")
    p.obj("tb", 40, 100, "t b b")
    p.obj("d3", 40, 140, "delay 2200")
    p.obj("d4", 160, 140, "delay 4100")
    p.obj("s3", 40, 180, "s s6_hippo_b3")
    p.obj("s4", 160, 180, "s s6_hippo_b4")
    p.obj("s_tag", 300, 140, "s s6_tag_hook")
    p.msg("none", 300, 100, "symbol none")
    p.con("r_et", 0, "sel", 0)
    p.con("sel", 0, "tb", 0)
    p.con("tb", 0, "d3", 0)
    p.con("tb", 1, "d4", 0)
    p.con("d3", 0, "s3", 0)
    p.con("d4", 0, "s4", 0)
    p.con("sel", 0, "none", 0)
    p.con("none", 0, "s_tag", 0)
    p.text(20, 220, "v1 random Q07-12 - tags plus tard Q07-16")
    _w(p, "hippo_assoc_07.pd")


def gen_boucle_inject_07():
    """15% à une transition: réinjection one-shot après 8–90 s, autre HP."""
    p = P(560, 320)
    p.text(20, 8, "boucle_inject_07 15pct delai 8-90s one-shot")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("chg", 40, 70, "change")
    p.obj("tb", 40, 100, "t b")
    p.obj("rnd", 40, 130, "random 100")
    p.obj("lt", 40, 160, f"< {PR.BOUCLE_PROBA}")
    p.obj("sel", 40, 190, "sel 1")
    p.obj("rd", 40, 220, "random 82000")
    p.obj("pd", 40, 250, "+ 8000")
    p.obj("dt", 180, 220, "t b f")
    p.obj("del", 180, 250, "delay 8000")
    p.obj("s_b", 180, 280, "s s6_boucle_bang")
    p.con("r_et", 0, "chg", 0)
    p.con("chg", 0, "tb", 0)
    p.con("tb", 0, "rnd", 0)
    p.con("rnd", 0, "lt", 0)
    p.con("lt", 0, "sel", 0)
    p.con("sel", 0, "rd", 0)
    p.con("rd", 0, "pd", 0)
    p.con("pd", 0, "dt", 0)
    p.con("dt", 1, "del", 1)
    p.con("dt", 0, "del", 0)
    p.con("del", 0, "s_b", 0)
    _w(p, "boucle_inject_07.pd")


def gen_player_state_07():
    """Lecteur SONS_V3 — listes [text], pas un open par fichier."""
    root = os.path.abspath(os.path.join(LIBDIR, "..", ".."))
    u = audit.usable_files(root)
    all_state = {si: sum((u[(si, di)] for di in range(3)), []) for si in range(4)}
    everything = sum(all_state.values(), [])
    if not everything:
        raise SystemExit("SONS_V3/: aucun segment utilisable")

    n_cx = 8
    cx_pools = audit.usable_cortex_layer_pools(root, n_layers=n_cx)
    moyen = u[(0, 1)] or all_state[0] or everything
    for li in range(n_cx):
        if not cx_pools[li]:
            cx_pools[li] = [moyen[li % len(moyen)]]

    amb_cx = audit.usable_ambiance(root, "CORTEX")
    if not amb_cx:
        raise SystemExit("SONS_V3/AMBIANCE: vide — pool d'ambiances partagé")
    amb_hp = audit.usable_ambiance(root, "HIPPOCAMPE") or amb_cx
    amb_pools = audit.usable_cortex_amb_pools(root, n=5)
    for i, pool in enumerate(amb_pools):
        if not pool:
            amb_pools[i] = amb_cx[i:] + amb_cx[:i]

    slot_specs = []
    for si in range(4):
        for di in range(3):
            files = u[(si, di)] or all_state[si] or everything
            slot_specs.append((si * 3 + di, files))
    for li in range(n_cx):
        slot_specs.append((20 + li, cx_pools[li]))
    slot_specs.append((30, amb_cx))
    slot_specs.append((31, amb_hp))
    for i, pool in enumerate(amb_pools):
        slot_specs.append((32 + i, pool))

    pl_dir = os.path.join(LIBDIR, "playlists07")
    if os.path.isdir(pl_dir):
        shutil.rmtree(pl_dir)
    os.makedirs(pl_dir)
    for s, files in slot_specs:
        with open(os.path.join(pl_dir, f"slot_{s}.txt"), "w", encoding="utf-8") as fh:
            for rel in files:
                fh.write(f"{rel} {os.path.basename(rel)};\n")

    sel_args = " ".join(str(s) for s, _ in slot_specs)
    nslots = len(slot_specs)
    p = P(980, 280 + nslots * 36)
    p.text(20, 6, "player_state_07 - SONS_V3 listes text (playlists07)")
    p.text(20, 22, "in0 bang \\, in1 slot froid \\, out0 audio \\, out1 nom")
    p.text(20, 38, "slots 0..11 etat/duree \\; 20..27 frag \\; 30-31 nappe \\; 32..36 Cortex 5 amb")
    p.obj("in_b", 40, 50, "inlet")
    p.obj("in_slot", 140, 50, "inlet")
    p.obj("out", 40, 240, "outlet~")
    p.obj("out_name", 200, 240, "outlet")
    p.obj("readsf", 700, 80, "readsf~")
    p.obj("gain", 700, 120, "*~ 0.9")
    p.con("readsf", 0, "gain", 0)
    p.con("gain", 0, "out", 0)
    p.obj("delay0", 40, 90, "delay 0")
    p.obj("tb", 40, 120, "t b")
    p.obj("f_slot", 140, 120, "f")
    p.obj("sel_slot", 40, 160, f"select {sel_args}")
    p.obj("del_start", 700, 160, "del 80")
    p.msg("m_start", 700, 200, "start")
    p.obj("t_open", 700, 140, "t a b")
    p.con("t_open", 0, "readsf", 0)
    p.con("t_open", 1, "del_start", 0)
    p.con("del_start", 0, "m_start", 0)
    p.con("m_start", 0, "readsf", 0)
    p.obj("spig_loop", 820, 40, "spigot \\$1")
    p.msg("m_clear", 820, 80, "symbol none")
    p.con("in_b", 0, "delay0", 0)
    p.con("delay0", 0, "tb", 0)
    p.con("tb", 0, "f_slot", 0)
    p.obj("t_slot", 200, 90, "t f b")
    p.con("in_slot", 0, "t_slot", 0)
    p.con("t_slot", 0, "f_slot", 1)
    p.con("f_slot", 0, "sel_slot", 0)
    p.con("readsf", 1, "spig_loop", 0)
    p.con("spig_loop", 0, "delay0", 0)
    p.obj("r_reps", 820, 120, "r s6_play_reps")
    p.obj("f_reps", 820, 150, "f 1")
    p.obj("lb_reps", 900, 180, "loadbang")
    p.msg("m_reps1", 900, 210, "1")
    p.con("lb_reps", 0, "m_reps1", 0)
    p.con("m_reps1", 0, "f_reps", 1)
    p.con("r_reps", 0, "f_reps", 1)
    p.obj("lb_loop", 820, 240, "loadbang")
    p.obj("f_loop", 820, 270, "f \\$1")
    p.obj("eq_loop0", 820, 300, "== 0")
    p.obj("spig_clr", 820, 330, "spigot")
    p.con("lb_loop", 0, "f_loop", 0)
    p.con("f_loop", 0, "eq_loop0", 0)
    p.con("eq_loop0", 0, "spig_clr", 1)
    p.con("readsf", 1, "spig_clr", 0)
    p.con("spig_clr", 0, "m_clear", 0)
    p.con("m_clear", 0, "out_name", 0)

    # graine unique par instance + bruit audio: pas la meme sequence a chaque lancement
    p.obj("nz", 40, 200, "noise~")
    p.obj("snap", 40, 230, "snapshot~")
    p.con("nz", 0, "snap", 0)
    p.obj("lb_id", 40, 260, "loadbang")
    p.obj("fid", 40, 290, "f \\$0")
    p.con("lb_id", 0, "fid", 0)
    p.obj("lb_pl", 40, 330, "loadbang")

    for oi, (s, files) in enumerate(slot_specs):
        n = len(files)
        y = 360 + oi * 36
        p.obj(f"td{s}", 400, y, f"text define \\$0-s{s}")
        p.msg(f"rd{s}", 220, y, f"read -c pd/lib/playlists07/slot_{s}.txt")
        p.con("lb_pl", 0, f"rd{s}", 0)
        p.con(f"rd{s}", 0, f"td{s}", 0)
        p.obj(f"tg{s}", 560, y, f"text get \\$0-s{s}")
        p.obj(f"ls{s}", 640, y, "list")
        p.obj(f"sp{s}", 700, y, "list split 1")
        p.obj(f"po{s}", 780, y, "list prepend open")
        p.obj(f"to{s}", 880, y, "list trim")
        p.obj(f"ps{s}", 780, y + 16, "list prepend symbol")
        p.obj(f"tn{s}", 880, y + 16, "list trim")
        p.con(f"tg{s}", 0, f"ls{s}", 0)
        p.con(f"ls{s}", 0, f"sp{s}", 0)
        p.con(f"sp{s}", 0, f"po{s}", 0)
        p.con(f"po{s}", 0, f"to{s}", 0)
        p.con(f"to{s}", 0, "t_open", 0)
        p.con(f"sp{s}", 1, f"ps{s}", 0)
        p.con(f"ps{s}", 0, f"tn{s}", 0)
        p.con(f"tn{s}", 0, "out_name", 0)
        if n >= 2:
            p.obj(f"ts{s}", 40, y, "t b b")
            p.obj(f"ml{s}", 100, y, "* 22000")
            p.obj(f"ab{s}", 160, y, "abs")
            p.obj(f"adid{s}", 220, y, "+")
            p.obj(f"adi{s}", 280, y, f"+ {s * 97 + 13}")
            p.obj(f"ii{s}", 340, y, "i")
            p.obj(f"rnd{s}", 40, y + 16, f"random {n - 1}")
            p.obj(f"a1{s}", 100, y + 16, "+ 1")
            p.obj(f"ad{s}", 160, y + 16, "+")
            p.obj(f"md{s}", 220, y + 16, f"% {n}")
            p.obj(f"tf{s}", 280, y + 16, "t f f")
            p.obj(f"fp{s}", 340, y + 16, "f 0")
            p.con("sel_slot", oi, f"ts{s}", 0)
            p.con(f"ts{s}", 0, "snap", 0)
            p.con("snap", 0, f"ml{s}", 0)
            p.con(f"ml{s}", 0, f"ab{s}", 0)
            p.con(f"ab{s}", 0, f"adid{s}", 0)
            p.con("fid", 0, f"adid{s}", 1)
            p.con(f"adid{s}", 0, f"adi{s}", 0)
            p.con(f"adi{s}", 0, f"ii{s}", 0)
            p.msg(f"sd{s}", 400, y + 16, "seed \\$1")
            p.con(f"ii{s}", 0, f"sd{s}", 0)
            p.con(f"sd{s}", 0, f"rnd{s}", 0)
            p.con(f"ts{s}", 1, f"rnd{s}", 0)
            p.con(f"rnd{s}", 0, f"a1{s}", 0)
            p.con(f"a1{s}", 0, f"ad{s}", 0)
            p.con(f"ad{s}", 0, f"md{s}", 0)
            p.con(f"md{s}", 0, f"tf{s}", 0)
            p.con(f"tf{s}", 1, f"fp{s}", 1)
            p.con(f"tf{s}", 1, f"ad{s}", 1)
            p.con(f"tf{s}", 0, f"tg{s}", 0)
        else:
            p.msg(f"z{s}", 40, y, "0")
            p.con("sel_slot", oi, f"z{s}", 0)
            p.con(f"z{s}", 0, f"tg{s}", 0)
    _w(p, "player_state_07.pd")


def gen_cortex_pulse_07():
    """En Cortex: bangs decales L1-L6 pour enchainer les petits fragments."""
    p = P(560, 300)
    p.text(20, 8, "cortex_pulse_07 enchainement L1-L6")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 0")
    p.msg("off", 140, 100, "stop")
    p.obj("met", 40, 140, "metro 10000")
    p.obj("tg", 40, 100, "t b b")
    p.con("r_et", 0, "sel", 0)
    p.con("sel", 0, "tg", 0)
    p.con("tg", 0, "met", 0)
    p.con("sel", 1, "off", 0)
    p.con("off", 0, "met", 0)
    p.obj("tb", 40, 180, "t b b b b b b")
    p.con("met", 0, "tb", 0)
    p.con("tg", 1, "tb", 0)
    for i in range(6):
        p.obj(f"d{i}", 20 + i * 80, 220, f"delay {80 + i * 160}")
        p.obj(f"o{i}", 20 + i * 80, 260, "outlet")
        p.con("tb", i, f"d{i}", 0)
        p.con(f"d{i}", 0, f"o{i}", 0)
    _w(p, "cortex_pulse_07.pd")


def gen_cortex_amb_pulse_07():
    """Bangs des 5 nappes Cortex (fichiers longs, decales)."""
    p = P(520, 300)
    p.text(20, 8, "cortex_amb_pulse_07 5 nappes")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 0")
    p.msg("off", 140, 100, "stop")
    p.obj("met", 40, 140, "metro 14000")
    p.obj("tg", 40, 100, "t b b")
    p.con("r_et", 0, "sel", 0)
    p.con("sel", 0, "tg", 0)
    p.con("tg", 0, "met", 0)
    p.con("sel", 1, "off", 0)
    p.con("off", 0, "met", 0)
    p.obj("tb", 40, 180, "t b b b b b")
    p.con("met", 0, "tb", 0)
    p.con("tg", 1, "tb", 0)
    for i in range(5):
        p.obj(f"d{i}", 20 + i * 90, 220, f"delay {120 + i * 220}")
        p.obj(f"o{i}", 20 + i * 90, 260, "outlet")
        p.con("tb", i, f"d{i}", 0)
        p.con(f"d{i}", 0, f"o{i}", 0)
    _w(p, "cortex_amb_pulse_07.pd")


def gen_cortex_amb_07():
    """5 nappes seches → HP4-8, chacune un fichier. HP1-3 silencieux ici."""
    p = P(720, 360)
    p.text(20, 8, "cortex_amb_07 HP4-8 nappes differentes")
    for i in range(5):
        p.obj(f"in{i}", 20 + i * 80, 40, "inlet~")
    for k in range(8):
        p.obj(f"out{k}", 20 + k * 80, 320, "outlet~")
    for i in range(5):
        x = 20 + i * 80
        hz = 0.03 + i * 0.011
        p.obj(f"lfo{i}", x, 80, f"osc~ {hz:.3f}")
        p.obj(f"lg{i}", x, 110, "*~ 0.10")
        p.obj(f"la{i}", x, 140, "+~ 0.78")
        p.obj(f"g{i}", x, 180, "*~")
        p.con(f"lfo{i}", 0, f"lg{i}", 0)
        p.con(f"lg{i}", 0, f"la{i}", 0)
        p.con(f"in{i}", 0, f"g{i}", 0)
        p.con(f"la{i}", 0, f"g{i}", 1)
        p.con(f"g{i}", 0, f"out{i + 3}", 0)
    _w(p, "cortex_amb_07.pd")


def gen_cortex_pair_07():
    """3 baffles x 2 couches (HP1-3). Pas de send delay/reverb."""
    p = P(980, 720)
    p.text(20, 8, "cortex_pair_07 HP1-3 paires \\; HP4-8 nappes ailleurs")
    for i in range(6):
        p.obj(f"in{i}", 20 + i * 70, 40, "inlet~")
    for k in range(8):
        p.obj(f"out{k}", 20 + k * 80, 680, "outlet~")

    for pr in range(3):
        a, b = pr * 2, pr * 2 + 1
        x = 20 + pr * 280
        p.obj(f"sum{pr}", x, 80, "+~")
        p.con(f"in{a}", 0, f"sum{pr}", 0)
        p.con(f"in{b}", 0, f"sum{pr}", 1)
        hz = 0.045 + pr * 0.018
        p.obj(f"lfo{pr}", x, 110, f"osc~ {hz:.3f}")
        p.obj(f"lfog{pr}", x, 140, "*~ 0.14")
        p.obj(f"lfoa{pr}", x, 170, "+~ 0.82")
        p.obj(f"att{pr}", x, 200, "*~")
        p.con(f"lfo{pr}", 0, f"lfog{pr}", 0)
        p.con(f"lfog{pr}", 0, f"lfoa{pr}", 0)
        p.con(f"sum{pr}", 0, f"att{pr}", 0)
        p.con(f"lfoa{pr}", 0, f"att{pr}", 1)

    p.obj("r_et", 780, 40, "r s6_etat")
    p.obj("sel", 780, 70, "sel 0")
    p.msg("go", 780, 100, "bang")
    p.msg("stp", 860, 100, "stop")
    p.con("r_et", 0, "sel", 0)
    p.con("sel", 0, "go", 0)
    p.con("sel", 1, "stp", 0)
    p.obj("met", 780, 140, "metro 2600")
    p.con("go", 0, "met", 0)
    p.con("stp", 0, "met", 0)
    p.obj("ch", 780, 170, "random 100")
    p.obj("lt", 780, 200, "< 62")
    p.obj("sm", 780, 230, "sel 1")
    p.con("met", 0, "ch", 0)
    p.con("ch", 0, "lt", 0)
    p.con("lt", 0, "sm", 0)
    p.obj("fo", 780, 260, "f 0")
    p.obj("p1", 780, 290, "+ 1")
    p.obj("md", 780, 320, "% 3")
    p.con("sm", 0, "fo", 0)
    p.con("fo", 0, "p1", 0)
    p.con("p1", 0, "md", 0)
    p.con("md", 0, "fo", 1)
    p.obj("rr", 860, 290, "random 3")
    p.obj("tbj", 860, 260, "t b")
    p.con("sm", 1, "tbj", 0)
    p.con("tbj", 0, "rr", 0)
    p.obj("off", 780, 360, "f")
    p.con("md", 0, "off", 0)
    p.con("rr", 0, "off", 0)
    p.obj("toff", 780, 390, "t f f f")
    p.con("off", 0, "toff", 0)
    p.obj("lb", 880, 140, "loadbang")
    p.msg("ini", 880, 170, "0")
    p.con("lb", 0, "ini", 0)
    p.con("ini", 0, "off", 0)
    p.con("ini", 0, "fo", 1)

    for pr in range(3):
        x = 20 + pr * 280
        p.obj(f"ad{pr}", x, 420, f"+ {pr}")
        p.obj(f"mod{pr}", x, 450, "% 3")
        p.obj(f"sh{pr}", x, 480, "sel 0 1 2")
        p.con("toff", pr, f"ad{pr}", 0)
        p.con(f"ad{pr}", 0, f"mod{pr}", 0)
        p.con(f"mod{pr}", 0, f"sh{pr}", 0)
        for h in range(3):
            p.msg(f"m1{pr}_{h}", x, 510 + h * 18, "1")
            p.msg(f"m0{pr}_{h}", x + 36, 510 + h * 18, "0")
            p.obj(f"pk{pr}_{h}", x + 72, 510 + h * 18, "pack 0 12")
            p.obj(f"ln{pr}_{h}", x + 140, 510 + h * 18, "line~")
            p.obj(f"g{pr}_{h}", x + 210, 510 + h * 18, "*~")
            p.con(f"sh{pr}", h, f"m1{pr}_{h}", 0)
            for hh in range(3):
                if hh != h:
                    p.con(f"sh{pr}", h, f"m0{pr}_{hh}", 0)
            p.con(f"m1{pr}_{h}", 0, f"pk{pr}_{h}", 0)
            p.con(f"m0{pr}_{h}", 0, f"pk{pr}_{h}", 0)
            p.con(f"pk{pr}_{h}", 0, f"ln{pr}_{h}", 0)
            p.con(f"ln{pr}_{h}", 0, f"g{pr}_{h}", 1)
            p.con(f"att{pr}", 0, f"g{pr}_{h}", 0)

    for h in range(3):
        p.obj(f"sA{h}", 20 + h * 180, 590, "+~")
        p.obj(f"sB{h}", 80 + h * 180, 620, "+~")
        p.con(f"g0_{h}", 0, f"sA{h}", 0)
        p.con(f"g1_{h}", 0, f"sA{h}", 1)
        p.con(f"sA{h}", 0, f"sB{h}", 0)
        p.con(f"g2_{h}", 0, f"sB{h}", 1)
        p.con(f"sB{h}", 0, f"out{h}", 0)
    _w(p, "cortex_pair_07.pd")


def ensure():
    gen_fsm_memory_07()
    gen_fsm_presets_07()
    gen_hippo_motion_07()
    gen_amb_route_07()
    gen_cortex_ctrl_07()
    gen_presence_07()
    gen_recon_pulse_07()
    gen_hippo_assoc_07()
    gen_boucle_inject_07()
    gen_player_state_07()
    gen_cortex_pulse_07()
    gen_cortex_amb_pulse_07()
    gen_cortex_amb_07()
    gen_cortex_pair_07()
