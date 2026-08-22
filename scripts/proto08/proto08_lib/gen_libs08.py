"""Génère les abstractions Pd Proto 08 (pd/lib/*_08*.pd).

N'écrit QUE des fichiers *_08. Réutilise le DSP 06 (fx_router_06,
spatial_router_06, decode_8hp_06, visu_cerveau_06, install_mode_06).
"""
import os
import shutil
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "scripts"))
from shared.pdbuild import P
from shared.gain_registre import gain_map_from_registre, linear_gain_for_rel, fmt_gain
from . import presets08 as PR
from . import sons_audit08 as audit
from . import hippo_recipes as HR
from . import hippo_events_loader as HEL
from . import recon_recipes as RR
from . import recon_events_loader as REL

LIBDIR = os.path.join(_REPO, "pd", "lib")


def _w(p, fname):
    p.write(os.path.join(LIBDIR, fname))
    print(f"OK lib: {fname}")


def gen_fsm_memory_08(fname="fsm_memory_08_8hp.pd", fsm_n=None, max_layers=None,
                      cycle1=None):
    """FSM 08: cycle 1 Cortex 40s → Hippo 50s → Recon 120s.

    Extra vs 06: pique Boucle 15% en cycle libre. Piezo → s6_force (Q14).
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

    p.text(800, 140, "08 Boucle 15pct cycles libres · piezo via s6_force")
    _w(p, fname)


def gen_fsm_presets_08(fname="fsm_presets_08_8hp.pd", presets=None):
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
    p.text(300, 40, "banques 08: etat*3+variante -> s6_*")
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


def _motion_layer_msgs(p, tag, layer, spec, y):
    """Crée msg+send pour une couche ; retourne liste noms msg pour trigger."""
    names = []
    for key, sfx in (("mode", "mode"), ("step", "step"), ("xfade", "xfade"),
                     ("sens", "sens"), ("rot", "rot")):
        if key not in spec:
            continue
        mn = f"{tag}m{layer}{key}"
        sn = f"{tag}s{layer}{key}"
        p.msg(mn, 200, y, str(spec[key]))
        p.obj(sn, 640, y, f"s s6_l{layer}_{sfx}")
        p.con(mn, 0, sn, 0)
        names.append(mn)
        y += 22
    return names, y


def gen_hippo_motion_08():
    """Bibliothèque 5 recettes spatiales V1 (Q26)."""
    p = P(1100, 820)
    p.text(20, 10, "hippo_motion_08 — 5 recettes Q26 · metro 2-4.5s")
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

    p.obj("ent", 40, 180, "t b b b b b b")
    p.con("d_ent", 0, "ent", 0)
    init_triggers: list[str] = []
    y = 160
    for layer in (1, 2, 3, 4):
        names, y = _motion_layer_msgs(p, "i", layer, HR.INIT_LAYERS[layer], y + layer * 2)
        init_triggers.extend(names)
    names13, _ = _motion_layer_msgs(p, "i", 13, HR.INIT_LAYERS[13], 300)
    init_triggers.extend(names13)
    for oi, mn in enumerate(init_triggers[:9]):
        p.con("ent", min(oi, 5), mn, 0)

    p.msg("m0_l13", 220, 100, "0")
    p.obj("sm13_off", 640, 100, "s s6_l13_mode")
    p.con("sel_h", 1, "m0_l13", 0)
    p.con("m0_l13", 0, "sm13_off", 0)

    p.obj("tb_tick", 40, 380, "t b b")
    p.con("met", 0, "tb_tick", 0)
    p.obj("rnd_r", 120, 380, "random 5")
    p.con("tb_tick", 0, "rnd_r", 0)
    p.obj("f_rec", 120, 410, "f 0")
    p.con("rnd_r", 0, "f_rec", 0)
    p.obj("r_rec", 40, 410, "r s6_hippo_motion")
    p.con("r_rec", 0, "f_rec", 0)
    p.obj("sel_r", 120, 440, "sel 0 1 2 3 4")
    p.con("f_rec", 0, "sel_r", 0)

    for rid, spec in enumerate(HR.RECIPES):
        yb = 480 + rid * 55
        p.obj(f"tr{rid}", 320, yb, "t b b b b b b b b b")
        p.con("sel_r", rid, f"tr{rid}", 0)
        msgs: list[str] = []
        yy = yb
        for layer in sorted(spec):
            nms, yy = _motion_layer_msgs(p, f"a{rid}", layer, spec[layer], yy)
            msgs.extend(nms)
        for oi, mn in enumerate(msgs[:9]):
            p.con(f"tr{rid}", oi, mn, 0)

    p.obj("rit", 40, 760, "random 2500")
    p.obj("pit", 40, 790, "+ 2000")
    p.con("tb_tick", 1, "rit", 0)
    p.con("rit", 0, "pit", 0)
    p.con("pit", 0, "met", 1)
    p.text(20, 800, "recettes Q26 · s6_hippo_motion force 0-4")
    _w(p, "hippo_motion_08.pd")


def gen_amb_route_08():
    """Route le lit d'ambiance vers 1 HP (1–8), fixe pendant le tour."""
    p = P(900, 520)
    p.text(20, 10, "amb_route_08 1 HP dedie index s6_amb_hp")
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
    _w(p, "amb_route_08.pd")


def gen_cortex_ctrl_08():
    """Cortex: 12 voix, balayage LPF underwater L1-L12, FX nappes L15-L16."""
    p = P(920, 580)
    p.text(20, 8, "cortex_ctrl_08 12 voix · LPF sweep · FX nappes HP5/HP7")

    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 0 1")
    p.con("r_et", 0, "sel", 0)

    p.obj("tb", 40, 110, "t b b b")
    p.con("sel", 0, "tb", 0)
    p.msg("n12", 40, 150, "12")
    p.obj("s_n", 40, 190, "s s6_cortex_n")
    p.con("tb", 0, "n12", 0)
    p.con("n12", 0, "s_n", 0)
    p.obj("lb_n", 40, 230, "loadbang")
    p.con("lb_n", 0, "n12", 0)

    p.obj("dcx", 200, 110, "delay 40")
    p.msg("dry", 200, 150,
          "\\; s6_l13_lpf 18000 \\; s6_l13_wet 0 \\; s6_l13_on 0 \\; s6_l13_sat 0 \\; s6_l13_hpf 30 \\; s6_l13_fb 0 \\; s6_l13_flfo 0 \\; s6_l13_del 40")
    p.con("tb", 1, "dcx", 0)
    p.con("dcx", 0, "dry", 0)

    p.obj("dhp", 200, 230, "delay 40")
    p.msg("hplpf", 200, 270,
          "\\; s6_l13_lpf 5000 \\; s6_l13_wet 0 \\; s6_l13_on 0 \\; s6_l13_sat 0 \\; s6_l13_hpf 40 \\; s6_l13_fb 0 \\; s6_l13_flfo 0")
    p.con("sel", 1, "dhp", 0)
    p.con("dhp", 0, "hplpf", 0)

    # FX nappes (fx_router 15 musicale · 16 texture)
    p.msg("fxmus", 360, 110, PR.amb_fx_msg(15, PR.AMB_MUSICALE_FX))
    p.msg("fxtex", 360, 150, PR.amb_fx_msg(16, PR.AMB_TEXTURE_FX))
    p.con("tb", 2, "fxmus", 0)
    p.con("tb", 2, "fxtex", 0)

    # Balayage LPF 500–2000 Hz (12 osc. non harmoniques) — effet underwater
    p.msg("m_go", 40, 310, "bang")
    p.msg("m_stop", 120, 310, "stop")
    p.obj("metro_l", 40, 340, "metro 50")
    p.con("sel", 0, "m_go", 0)
    p.con("sel", 1, "m_stop", 0)
    p.con("m_go", 0, "metro_l", 0)
    p.con("m_stop", 0, "metro_l", 0)

    for i in range(12):
        x = 40 + (i % 6) * 140
        y = 380 + (i // 6) * 130
        hz = 0.063 + i * 0.019
        if i % 2 == 0:
            # PREMIER_PLAN : 800–2000 Hz
            amp, base, lo, hi = 600, 1400, 800, 2000
        else:
            # ARRIERE_PLAN : 500–1000 Hz
            amp, base, lo, hi = 250, 750, 500, 1000
        p.obj(f"os{i}", x, y, f"osc~ {hz:.3f}")
        p.obj(f"sc{i}", x, y + 28, f"*~ {amp}")
        p.obj(f"of{i}", x, y + 56, f"+~ {base}")
        p.obj(f"sn{i}", x, y + 84, "snapshot~")
        p.obj(f"cl{i}", x, y + 112, f"clip {lo} {hi}")
        p.obj(f"sl{i}", x, y + 140, f"s s6_l{i + 1}_lpf")
        p.con(f"os{i}", 0, f"sc{i}", 0)
        p.con(f"sc{i}", 0, f"of{i}", 0)
        p.con(f"of{i}", 0, f"sn{i}", 0)
        p.con("metro_l", 0, f"sn{i}", 0)
        p.con(f"sn{i}", 0, f"cl{i}", 0)
        p.con(f"cl{i}", 0, f"sl{i}", 0)

    _w(p, "cortex_ctrl_08.pd")


def gen_presence_08():
    """Piezo/micro + rms_sim. Q14: déclenche transition + fondu nappes — pas de hold."""
    p = P(820, 520)
    p.text(20, 8, "presence_08 Q14 piezo → zone suivante + fade amb · pas s6_cortex_hold")
    p.obj("r_on", 40, 40, "r s6_input_on")
    p.obj("r_sim", 160, 40, "r s6_rms_sim")
    p.obj("r_et", 280, 40, "r s6_etat")
    p.obj("f_et", 280, 70, "f 0")
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

    # Piezo: seuil 0.35, front montant (change), cooldown 3 s
    p.obj("th_p", 120, 400, "> 0.35")
    p.obj("ch_p", 120, 430, "change")
    p.obj("eq1", 120, 460, "== 1")
    p.obj("sp_p", 120, 490, "spigot")
    p.obj("lk", 120, 490, "f 0")
    p.obj("cd", 200, 490, "delay 3000")
    p.con("en", 0, "th_p", 0)
    p.con("th_p", 0, "ch_p", 0)
    p.con("ch_p", 0, "eq1", 0)
    p.con("eq1", 0, "sp_p", 0)
    p.con("lk", 0, "sp_p", 1)
    p.obj("pt", 280, 460, "t b b b")
    p.con("sp_p", 0, "pt", 0)
    p.con("pt", 0, "lk", 0)
    p.msg("lk1", 280, 490, "1")
    p.con("lk1", 0, "lk", 0)
    p.con("lk1", 0, "cd", 0)
    p.con("cd", 0, "lk", 0)

    # Zone suivante: (etat + 1) % 4 → s6_force
    p.obj("p1", 400, 460, "+ 1")
    p.obj("m4", 400, 490, "% 4")
    p.obj("s_frc", 480, 490, "s s6_force")
    p.con("f_et", 0, "p1", 0)
    p.con("pt", 1, "p1", 0)
    p.con("p1", 0, "m4", 0)
    p.con("m4", 0, "s_frc", 0)

    p.obj("s_pf", 480, 430, "s s6_piezo_fade")
    p.con("pt", 2, "s_pf", 0)

    # INTERRUPTIBLE — un fondu commun pour tous les cuts
    p.obj("rf", 400, 520, "random 66")
    p.obj("af", 400, 545, "+ 35")
    p.con("pt", 0, "rf", 0)
    p.con("rf", 0, "af", 0)
    for layer in range(1, 5):
        p.obj(f"sc{layer}", 560, 520 + (layer - 1) * 28, f"s s6_hippo_cut{layer}")
        p.con("af", 0, f"sc{layer}", 0)
    for layer in range(1, 3):
        p.obj(f"sr{layer}", 560, 640 + (layer - 1) * 28, f"s s6_recon_cut{layer}")
        p.con("af", 0, f"sr{layer}", 0)

    p.text(20, 400, "pas de cable adc vers dac (anti larsen)")
    _w(p, "presence_08.pd")


def _spatial_msg(recipe_idx: int) -> str:
    spec = RR.SPATIAL_RECIPES[recipe_idx % len(RR.SPATIAL_RECIPES)]
    parts = []
    for layer, params in spec.items():
        for key, val in params.items():
            parts.append(f"s6_l{layer}_{key} {val}")
    return "\\; ".join(parts)


def gen_recon_formes_08():
    """Lit recon_formes/events.txt — moteur compositionnel Reconstruction [Q31]."""
    events = REL.load_events(LIBDIR)
    p = P(900, 120 + len(events) * 48)
    p.text(20, 8, "recon_formes_08 — gen_formes_recon.py · remplace recon_pulse")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 2")
    p.obj("tb0", 40, 100, "t b b")
    p.con("sel", 0, "tb0", 0)

    prev = "tb0"
    prev_t = 0
    y = 130
    ev_i = 0
    for ev in events:
        act = ev["action"]
        t_abs = max(0, int(ev["t"]))
        dly_ms = max(0, t_abs - prev_t)
        prev_t = t_abs
        p.obj(f"d{ev_i}", 40, y, f"delay {dly_ms}")
        p.con(prev, 0, f"d{ev_i}", 0)
        if act == "play":
            layer = int(ev.get("layer", 1))
            p.obj(f"s{ev_i}", 200, y, f"s s6_recon_b{layer}")
            p.con(f"d{ev_i}", 0, f"s{ev_i}", 0)
        elif act == "cut":
            layer = int(ev.get("layer", 2))
            fade = int(ev.get("fade_ms", 50))
            p.msg(f"fd{ev_i}", 200, y, str(fade))
            p.obj(f"s{ev_i}", 320, y, f"s s6_recon_cut{layer}")
            p.con(f"d{ev_i}", 0, f"fd{ev_i}", 0)
            p.con(f"fd{ev_i}", 0, f"s{ev_i}", 0)
        elif act == "spatial":
            recipe = int(ev.get("recipe", 0))
            body = _spatial_msg(recipe)
            p.msg(f"sp{ev_i}", 200, y, body)
            p.con(f"d{ev_i}", 0, f"sp{ev_i}", 0)
        elif act == "silence":
            # silence compositionnel — pas de bang lecteur
            pass
        prev = f"d{ev_i}"
        y += 44
        ev_i += 1

    p.msg("rst", 40, y + 20, "stop")
    p.con("sel", 1, "rst", 0)
    p.text(20, y + 50, f"{ev_i} events · état 2 · spatial Simon §14")
    _w(p, "recon_formes_08.pd")


def gen_hippo_assoc_08():
    """Lit events.txt — planifie play/cut/motion pour l'état Hippocampe."""
    events = HEL.load_events(LIBDIR)
    p = P(720, 120 + len(events) * 48)
    p.text(20, 8, "hippo_assoc_08 — séquences gen_assoc_hippo.py")
    p.obj("r_et", 40, 40, "r s6_etat")
    p.obj("sel", 40, 70, "sel 1")
    p.obj("tb0", 40, 100, "t b b")
    p.con("sel", 0, "tb0", 0)

    p.obj("s_tag", 520, 100, "s s6_tag_hook")
    p.msg("tag0", 520, 70, "symbol hippo_v1")
    p.con("tb0", 1, "tag0", 0)
    p.con("tag0", 0, "s_tag", 0)

    prev = "tb0"
    prev_t = 0
    y = 130
    ev_i = 0
    for ev in events:
        act = ev["action"]
        if act in ("silence", "noop"):
            continue
        t_abs = max(0, int(ev["t"]))
        dly_ms = max(0, t_abs - prev_t)
        prev_t = t_abs
        p.obj(f"d{ev_i}", 40, y, f"delay {dly_ms}")
        p.con(prev, 0, f"d{ev_i}", 0)
        if act == "play":
            layer = int(ev.get("layer", 3))
            p.obj(f"s{ev_i}", 200, y, f"s s6_hippo_b{layer}")
            p.con(f"d{ev_i}", 0, f"s{ev_i}", 0)
        elif act == "cut":
            layer = int(ev.get("layer", 3))
            fade = int(ev.get("fade_ms", 50))
            p.msg(f"fd{ev_i}", 200, y, str(fade))
            p.obj(f"s{ev_i}", 320, y, f"s s6_hippo_cut{layer}")
            p.con(f"d{ev_i}", 0, f"fd{ev_i}", 0)
            p.con(f"fd{ev_i}", 0, f"s{ev_i}", 0)
        elif act == "motion":
            recipe = int(ev.get("recipe", 0))
            p.msg(f"m{ev_i}", 200, y, str(recipe))
            p.obj(f"s{ev_i}", 320, y, "s s6_hippo_motion")
            p.con(f"d{ev_i}", 0, f"m{ev_i}", 0)
            p.con(f"m{ev_i}", 0, f"s{ev_i}", 0)
        prev = f"d{ev_i}"
        y += 44
        ev_i += 1

    p.msg("rst", 40, y + 20, "stop")
    p.con("sel", 1, "rst", 0)
    p.text(20, y + 50, f"{ev_i} events · deltas · L3/L4 courts")
    _w(p, "hippo_assoc_08.pd")


def gen_hippo_duck_08():
    """HA8 — duck ambiance (−4 à −10 dB) quand parole Hippo active."""
    p = P(640, 320)
    p.text(20, 8, "hippo_duck_08 HA8 gate parole L1-L4")
    for i in range(4):
        p.obj(f"in{i}", 40 + i * 100, 40, "inlet~")
    p.obj("out", 40, 260, "outlet~")
    p.obj("m01", 40, 100, "max~")
    p.obj("m23", 240, 100, "max~")
    p.obj("mall", 140, 140, "max~")
    p.obj("env", 140, 180, "env~ 512")
    p.obj("met", 300, 140, "metro 40")
    p.obj("snap", 140, 210, "snapshot~")
    p.obj("th", 300, 180, "> 0.012")
    p.obj("sel", 300, 210, "sel 1")
    p.msg("pk_d", 420, 200, "0.45 20")
    p.msg("pk_u", 420, 230, "1 200")
    p.obj("ln", 520, 210, "line~")
    p.con("in0", 0, "m01", 0)
    p.con("in1", 0, "m01", 1)
    p.con("in2", 0, "m23", 0)
    p.con("in3", 0, "m23", 1)
    p.con("m01", 0, "mall", 0)
    p.con("m23", 0, "mall", 1)
    p.con("mall", 0, "env", 0)
    p.con("met", 0, "snap", 0)
    p.con("env", 0, "snap", 0)
    p.con("snap", 0, "th", 0)
    p.con("th", 0, "sel", 0)
    p.con("sel", 0, "pk_d", 0)
    p.con("sel", 1, "pk_u", 0)
    p.con("pk_d", 0, "ln", 0)
    p.con("pk_u", 0, "ln", 0)
    p.con("ln", 0, "out", 0)
    p.text(20, 290, "duck ~-7dB · relache 200ms")
    _w(p, "hippo_duck_08.pd")


def gen_boucle_inject_08():
    """15% à une transition: réinjection one-shot après 8–90 s, autre HP."""
    p = P(560, 320)
    p.text(20, 8, "boucle_inject_08 15pct delai 8-90s one-shot")
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
    _w(p, "boucle_inject_08.pd")


def _hippo_interruptible_map(root: str) -> dict[str, int]:
    """id → 0/1 depuis feuille Hippocampe (mode_lecture)."""
    xlsx = os.path.join(root, "docs", "Matiere", "catalogue_fragments.xlsx")
    out: dict[str, int] = {}
    if not os.path.isfile(xlsx):
        return out
    try:
        import openpyxl
    except ImportError:
        return out
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    try:
        if "Hippocampe" not in wb.sheetnames:
            return out
        ws = wb["Hippocampe"]
        rows = list(ws.iter_rows(min_row=2, max_row=2, values_only=True))
        if not rows or not rows[0]:
            return out
        headers = [str(h or "").strip().lower() for h in rows[0]]
        try:
            mi = headers.index("mode lecture")
        except ValueError:
            return out
        for row in ws.iter_rows(min_row=3, values_only=True):
            if not row or not row[0]:
                continue
            sid = str(row[0]).strip()
            mode = str(row[mi] if mi < len(row) else "").upper()
            if "INTERRUPT" in mode:
                out[sid] = 1
    finally:
        wb.close()
    return out


def _interruptible_for(rel: str, hippo_map: dict[str, int], slot: int) -> int:
    stem = os.path.splitext(os.path.basename(rel))[0]
    if stem in hippo_map:
        return hippo_map[stem]
    if slot in (3, 4):
        return 0
    return 0


def gen_player_state_08():
    """Lecteur SONS_V3 — listes [text], pas un open par fichier."""
    root = os.path.abspath(os.path.join(LIBDIR, "..", ".."))
    u = audit.usable_files(root)
    all_state = {si: sum((u[(si, di)] for di in range(3)), []) for si in range(4)}
    everything = sum(all_state.values(), [])
    if not everything:
        raise SystemExit("SONS_V3/: aucun segment utilisable")

    n_cx = 12
    cx_pools = audit.usable_cortex_layer_pools(root, n_layers=n_cx)
    moyen = u[(0, 1)] or all_state[0] or everything
    for li in range(n_cx):
        if not cx_pools[li]:
            cx_pools[li] = [moyen[li % len(moyen)]]

    amb_cx = audit.usable_ambiance(root, "CORTEX")
    if not amb_cx:
        raise SystemExit("SONS_V3/AMBIANCE: vide — pool d'ambiances partagé")
    amb_hp = audit.usable_ambiance(root, "HIPPOCAMPE") or amb_cx
    amb_pools = audit.usable_cortex_amb_pools(root, n=2)
    for i, pool in enumerate(amb_pools):
        if not pool:
            raise SystemExit(f"pool ambiance slot {32 + i}: vide")

    gain_map = gain_map_from_registre(root)
    hippo_int = _hippo_interruptible_map(root)

    slot_specs = []
    for si in range(4):
        for di in range(3):
            files = u[(si, di)] or all_state[si] or everything
            slot_specs.append((si * 3 + di, files))
    for li in range(n_cx):
        slot_specs.append((20 + li, cx_pools[li]))
    slot_specs.append((40, amb_cx))
    slot_specs.append((41, amb_hp))
    for i, pool in enumerate(amb_pools):
        slot_specs.append((32 + i, pool))

    pl_dir = os.path.join(LIBDIR, "playlists08")
    if os.path.isdir(pl_dir):
        shutil.rmtree(pl_dir)
    os.makedirs(pl_dir)
    for s, files in slot_specs:
        with open(os.path.join(pl_dir, f"slot_{s}.txt"), "w", encoding="utf-8") as fh:
            for rel in files:
                g = fmt_gain(linear_gain_for_rel(rel, gain_map))
                fh.write(f"{rel} {os.path.basename(rel)} {g};\n")

    for s, files in slot_specs:
        with open(os.path.join(pl_dir, f"slot_{s}.txt"), "w", encoding="utf-8") as fh:
            for rel in files:
                g = fmt_gain(linear_gain_for_rel(rel, gain_map))
                intr = _interruptible_for(rel, hippo_int, s)
                fh.write(f"{rel} {os.path.basename(rel)} {g} {intr};\n")

    sel_args = " ".join(str(s) for s, _ in slot_specs)
    nslots = len(slot_specs)
    p = P(980, 320 + nslots * 36)
    p.text(20, 6, "player_state_08 - SONS_V3 listes text (playlists08)")
    p.text(20, 22, "in0 bang \\, in1 slot \\, in2 cut/fade ms \\, out0 audio \\, out1 nom")
    p.text(20, 38, "gain+interruptible · fade cut 35-100ms · arg1=loop")
    p.obj("in_b", 40, 50, "inlet")
    p.obj("in_slot", 140, 50, "inlet")
    p.obj("in_cut", 240, 50, "inlet")
    p.obj("out", 40, 240, "outlet~")
    p.obj("out_name", 200, 240, "outlet")
    p.obj("readsf", 700, 80, "readsf~")
    p.obj("f_gn", 700, 200, "f 1")
    p.obj("gmul", 700, 160, "*~")
    p.obj("gain", 700, 120, "*~ 0.9")
    p.con("readsf", 0, "gmul", 0)
    p.con("f_gn", 0, "gmul", 1)
    p.con("gmul", 0, "gain", 0)
    p.con("gain", 0, "out", 0)
    p.obj("f_int", 860, 160, "f 0")
    p.obj("sp_cut", 860, 190, "spigot")
    p.con("f_int", 0, "sp_cut", 1)
    p.obj("t_cut", 860, 220, "t f b")
    p.con("in_cut", 0, "t_cut", 0)
    p.con("t_cut", 0, "def_fd", 0)
    p.con("t_cut", 1, "sp_cut", 0)
    p.con("t_cut", 1, "t_stop", 0)
    p.obj("def_fd", 860, 250, "f 50")
    p.msg("m_stop", 980, 310, "stop")
    p.obj("d_rst", 980, 340, "delay 120")
    p.obj("t_stop", 900, 270, "t f b")
    p.obj("del_stop", 980, 295, "del 50")
    p.con("def_fd", 0, "t_stop", 0)
    p.con("t_stop", 0, "del_stop", 1)
    p.con("t_stop", 1, "del_stop", 0)
    p.con("del_stop", 0, "m_stop", 0)
    p.con("m_stop", 0, "readsf", 0)
    p.con("m_stop", 0, "d_rst", 0)
    p.msg("m_ref", 980, 370, "1")
    p.con("d_rst", 0, "m_ref", 0)
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
        p.msg(f"rd{s}", 220, y, f"read -c pd/lib/playlists08/slot_{s}.txt")
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
        p.obj(f"spl2_{s}", 780, y + 16, "list split 1")
        p.con(f"sp{s}", 1, f"spl2_{s}", 0)
        p.con(f"spl2_{s}", 0, f"ps{s}", 0)
        p.obj(f"spl3_{s}", 880, y + 32, "list split 1")
        p.con(f"spl2_{s}", 1, f"spl3_{s}", 0)
        p.obj(f"fg{s}", 880, y + 16, "f 1")
        p.con(f"spl3_{s}", 0, f"fg{s}", 0)
        p.con(f"fg{s}", 0, "f_gn", 0)
        p.obj(f"fi{s}", 960, y + 32, "f 0")
        p.con(f"spl3_{s}", 1, f"fi{s}", 0)
        p.con(f"fi{s}", 0, "f_int", 0)
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
    _w(p, "player_state_08.pd")


def gen_cortex_amb_08():
    """2 nappes globales → HP7 (musicale) et HP5 (texture) + respiration LFO."""
    hp_tex = PR.AMBI_TEXTURE_HP - 1
    hp_mus = PR.AMBI_MUSICAL_HP - 1
    p = P(520, 340)
    p.text(20, 8, f"cortex_amb_08 HP{PR.AMBI_MUSICAL_HP} musicale HP{PR.AMBI_TEXTURE_HP} texture")
    for i in range(2):
        p.obj(f"in{i}", 40 + i * 200, 40, "inlet~")
    for k in range(8):
        p.obj(f"out{k}", 20 + k * 55, 300, "outlet~")
    specs = [(0, hp_mus, 0.028, 0.14, 0.82), (1, hp_tex, 0.022, 0.10, 0.80)]
    for idx, hp, hz, depth, base in specs:
        x = 40 + idx * 200
        p.obj(f"lfo{idx}", x, 80, f"osc~ {hz:.3f}")
        p.obj(f"lg{idx}", x, 110, f"*~ {depth:.2f}")
        p.obj(f"la{idx}", x, 140, f"+~ {base:.2f}")
        p.obj(f"g{idx}", x, 180, "*~")
        p.con(f"lfo{idx}", 0, f"lg{idx}", 0)
        p.con(f"lg{idx}", 0, f"la{idx}", 0)
        p.con(f"in{idx}", 0, f"g{idx}", 0)
        p.con(f"la{idx}", 0, f"g{idx}", 1)
        p.con(f"g{idx}", 0, f"out{hp}", 0)
    _w(p, "cortex_amb_08.pd")


def gen_cortex_amb_behav_08():
    """Gestes EMERGER / RECOUVRIR sur les 2 nappes — mutex RECOUVRIR [Q17]."""
    p = P(900, 420)
    p.text(20, 8, "cortex_amb_behav_08 EMERGER 6-10s · RECOUVRIR 3-6s · mutex Q17")

    for i in range(2):
        x = 40 + i * 380
        p.obj(f"in{i}", x, 40, "inlet~")
        p.obj(f"out{i}", x, 340, "outlet~")
        p.obj(f"lg{i}", x + 100, 160, "line~")
        p.obj(f"mg{i}", x + 100, 220, "*~")
        p.con(f"in{i}", 0, f"mg{i}", 0)
        p.con(f"lg{i}", 0, f"mg{i}", 1)
        p.con(f"mg{i}", 0, f"out{i}", 0)
        p.msg(f"zi{i}", x, 80, "1 10")
        p.con("lb0", 0, f"zi{i}", 0)
        p.con(f"zi{i}", 0, f"lg{i}", 0)

    p.obj("r_et", 40, 280, "r s6_etat")
    p.obj("chg", 40, 308, "change")
    p.obj("sel_cx", 40, 336, "sel 0")
    p.obj("cx_t", 120, 336, "t b b b b")
    p.obj("lb0", 120, 280, "loadbang")
    p.con("r_et", 0, "chg", 0)
    p.con("chg", 0, "sel_cx", 0)
    p.con("sel_cx", 0, "cx_t", 0)

    p.obj("rg0", 220, 336, "random 2")
    p.obj("rg1", 220, 364, "random 2")
    p.obj("fg0", 300, 336, "f 0")
    p.obj("fg1", 300, 364, "f 0")
    p.con("cx_t", 0, "rg0", 0)
    p.con("cx_t", 1, "rg1", 0)
    p.con("rg0", 0, "fg0", 0)
    p.con("rg1", 0, "fg1", 0)

    # Mutex Q17 : si les deux veulent RECOUVRIR (1), en garder un seul
    p.obj("eq0", 400, 336, "== 1")
    p.obj("eq1", 400, 364, "== 1")
    p.obj("sp_m1", 480, 350, "spigot")
    p.obj("sp_m2", 560, 350, "spigot")
    p.con("fg0", 0, "eq0", 0)
    p.con("fg1", 0, "eq1", 0)
    p.obj("del_mx", 480, 336, "delay 2")
    p.con("cx_t", 2, "del_mx", 0)
    p.con("del_mx", 0, "sp_m1", 0)
    p.con("eq1", 0, "sp_m1", 1)
    p.con("sp_m1", 0, "sp_m2", 0)
    p.con("eq0", 0, "sp_m2", 1)
    p.obj("rpick", 640, 350, "random 2")
    p.obj("sel_mx", 720, 350, "sel 0 1")
    p.con("sp_m2", 0, "rpick", 0)
    p.con("rpick", 0, "sel_mx", 0)
    p.msg("mx0", 800, 336, "0")
    p.msg("mx1", 800, 364, "0")
    p.con("sel_mx", 0, "mx1", 0)
    p.con("sel_mx", 1, "mx0", 0)
    p.con("mx0", 0, "fg0", 0)
    p.con("mx1", 0, "fg1", 0)

    p.obj("del_go", 640, 336, "delay 8")
    p.con("cx_t", 3, "del_go", 0)

    for i in range(2):
        x = 40 + i * 380
        cy = 260
        p.obj(f"sg{i}", x, cy, "sel 0 1")
        p.con("del_go", 0, f"fg{i}", 0)
        p.con(f"fg{i}", 0, f"sg{i}", 0)

        p.obj(f"re{i}", x + 100, cy, "random 4001")
        p.obj(f"ae{i}", x + 100, cy + 22, "+ 6000")
        p.obj(f"rr{i}", x + 100, cy + 48, "random 3001")
        p.obj(f"ar{i}", x + 100, cy + 70, "+ 3000")
        p.obj(f"ste{i}", x + 100, cy + 96, "t b b")
        p.obj(f"str{i}", x + 100, cy + 122, "t b b")
        p.con(f"sg{i}", 0, f"ste{i}", 0)
        p.con(f"sg{i}", 1, f"str{i}", 0)
        p.con(f"ste{i}", 0, f"re{i}", 0)
        p.con(f"ste{i}", 1, f"me{i}", 0)
        p.con(f"str{i}", 0, f"rr{i}", 0)
        p.con(f"str{i}", 1, f"mr{i}", 0)
        p.con(f"re{i}", 0, f"ae{i}", 0)
        p.con(f"rr{i}", 0, f"ar{i}", 0)

        p.msg(f"me{i}", x + 200, cy, "0.45 0")
        p.msg(f"mr{i}", x + 200, cy + 48, "0.7 0")
        p.obj(f"pk_e{i}", x + 200, cy + 22, "pack 1 7000")
        p.obj(f"pk_r{i}", x + 200, cy + 70, "pack 1.15 7000")
        p.con(f"ae{i}", 0, f"pk_e{i}", 1)
        p.con(f"ar{i}", 0, f"pk_r{i}", 1)
        p.con(f"me{i}", 0, f"lg{i}", 0)
        p.con(f"mr{i}", 0, f"lg{i}", 0)
        p.obj(f"d_e{i}", x + 280, cy + 22, "delay 3")
        p.obj(f"d_r{i}", x + 280, cy + 70, "delay 3")
        p.con(f"me{i}", 0, f"d_e{i}", 0)
        p.con(f"mr{i}", 0, f"d_r{i}", 0)
        p.con(f"d_e{i}", 0, f"pk_e{i}", 0)
        p.con(f"d_r{i}", 0, f"pk_r{i}", 0)
        p.con(f"pk_e{i}", 0, f"lg{i}", 0)
        p.con(f"pk_r{i}", 0, f"lg{i}", 0)

    # Piezo Q14 — fondu sortie nappes 0,5–2 s
    p.obj("r_pf", 40, 380, "r s6_piezo_fade")
    p.obj("rp", 40, 410, "random 1501")
    p.obj("ap", 120, 410, "+ 500")
    p.obj("tp", 200, 410, "t b")
    p.con("r_pf", 0, "tp", 0)
    p.con("tp", 0, "rp", 0)
    p.con("rp", 0, "ap", 0)
    for i in range(2):
        p.obj(f"pkf{i}", 280 + i * 100, 410, "pack 0 1500")
        p.con("ap", 0, f"pkf{i}", 1)
        p.con("tp", 0, f"pkf{i}", 0)
        p.con(f"pkf{i}", 0, f"lg{i}", 0)

    _w(p, "cortex_amb_behav_08.pd")


def gen_cortex_pair_08():
    """6 baffles × 2 voix — gestes EMERGER / RECOUVRIR [Q11]."""
    p = P(1280, 580)
    p.text(20, 8, "cortex_pair_08 EMERGER 6-10s · RECOUVRIR 3-6s · décalage aléatoire")

    for i in range(12):
        p.obj(f"in{i}", 24 + (i % 6) * 200, 28 + (i // 6) * 22, "inlet~")
    for k in range(6):
        p.obj(f"out{k}", 24 + k * 200, 540, "outlet~")

    p.obj("r_et", 980, 28, "r s6_etat")
    p.obj("chg", 980, 56, "change")
    p.obj("sel_cx", 980, 84, "sel 0")
    p.obj("cx_t", 980, 112, "t b b b b b b")
    p.obj("lb0", 980, 140, "loadbang")
    p.con("r_et", 0, "chg", 0)
    p.con("chg", 0, "sel_cx", 0)
    p.con("sel_cx", 0, "cx_t", 0)

    for pr in range(6):
        a, b = pr * 2, pr * 2 + 1
        x = 24 + pr * 200
        y = 80

        p.obj(f"gb{pr}", x + 88, y + 96, "line~")
        p.obj(f"gar{pr}", x + 88, y + 68, "*~ 0.79")
        p.obj(f"mb{pr}", x + 88, y + 132, "*~")
        p.con(f"in{b}", 0, f"gar{pr}", 0)
        p.con(f"gar{pr}", 0, f"mb{pr}", 0)
        p.con(f"gb{pr}", 0, f"mb{pr}", 1)

        p.obj(f"ma{pr}", x, y + 132, "*~ 1")
        p.con(f"in{a}", 0, f"ma{pr}", 0)

        p.obj(f"sm{pr}", x + 44, y + 168, "+~")
        p.con(f"ma{pr}", 0, f"sm{pr}", 0)
        p.con(f"mb{pr}", 0, f"sm{pr}", 1)

        hz = 0.045 + pr * 0.012
        p.obj(f"lf{pr}", x, y + 204, f"osc~ {hz:.3f}")
        p.obj(f"lg{pr}", x, y + 232, "*~ 0.08")
        p.obj(f"la{pr}", x, y + 260, "+~ 0.88")
        p.obj(f"at{pr}", x + 44, y + 296, "*~")
        p.con(f"lf{pr}", 0, f"lg{pr}", 0)
        p.con(f"lg{pr}", 0, f"la{pr}", 0)
        p.con(f"sm{pr}", 0, f"at{pr}", 0)
        p.con(f"la{pr}", 0, f"at{pr}", 1)
        p.con(f"at{pr}", 0, f"out{pr}", 0)

        cy = y + 328
        p.obj(f"tr{pr}", x, cy, "t b b b")
        p.con("cx_t", pr, f"tr{pr}", 0)
        p.msg(f"z{pr}", x + 56, cy, "0")
        p.con(f"tr{pr}", 0, f"z{pr}", 0)
        p.con(f"z{pr}", 0, f"gb{pr}", 0)
        p.con("lb0", 0, f"z{pr}", 0)

        p.obj(f"rg{pr}", x + 56, cy + 24, "random 2")
        p.obj(f"sg{pr}", x + 56, cy + 52, "sel 0 1")
        p.con(f"tr{pr}", 1, f"rg{pr}", 0)
        p.con(f"rg{pr}", 0, f"sg{pr}", 0)

        p.obj(f"re{pr}", x + 140, cy + 24, "random 4001")
        p.obj(f"ae{pr}", x + 140, cy + 44, "+ 6000")
        p.obj(f"rr{pr}", x + 140, cy + 68, "random 3001")
        p.obj(f"ar{pr}", x + 140, cy + 88, "+ 3000")
        p.con(f"sg{pr}", 0, f"re{pr}", 0)
        p.con(f"sg{pr}", 1, f"rr{pr}", 0)
        p.con(f"re{pr}", 0, f"ae{pr}", 0)
        p.con(f"rr{pr}", 0, f"ar{pr}", 0)

        p.obj(f"mf{pr}", x + 220, cy + 52, "f 7000")
        p.con(f"ae{pr}", 0, f"mf{pr}", 0)
        p.con(f"ar{pr}", 0, f"mf{pr}", 0)

        p.obj(f"rd{pr}", x + 56, cy + 112, "random 3501")
        p.obj(f"dt{pr}", x + 140, cy + 112, "t f b")
        p.obj(f"dl{pr}", x + 220, cy + 112, "delay 500")
        p.obj(f"pk{pr}", x + 300, cy + 112, "pack 1 7000")
        p.con(f"tr{pr}", 2, f"rd{pr}", 0)
        p.con(f"rd{pr}", 0, f"dt{pr}", 0)
        p.con(f"dt{pr}", 0, f"dl{pr}", 1)
        p.con(f"dt{pr}", 1, f"dl{pr}", 0)
        p.con(f"mf{pr}", 0, f"pk{pr}", 1)
        p.con(f"dl{pr}", 0, f"pk{pr}", 0)
        p.con(f"pk{pr}", 0, f"gb{pr}", 0)

    _w(p, "cortex_pair_08.pd")


def ensure():
    for script in (
        os.path.join(_REPO, "scripts", "gen_assoc_hippo.py"),
        os.path.join(_REPO, "scripts", "gen_formes_recon.py"),
    ):
        if os.path.isfile(script):
            import subprocess
            subprocess.run([sys.executable, script], cwd=_REPO, check=False)
    stale = os.path.join(LIBDIR, "recon_pulse_08.pd")
    if os.path.isfile(stale):
        os.remove(stale)
    gen_fsm_memory_08()
    gen_fsm_presets_08()
    gen_hippo_motion_08()
    gen_amb_route_08()
    gen_cortex_ctrl_08()
    gen_presence_08()
    gen_recon_formes_08()
    gen_hippo_assoc_08()
    gen_hippo_duck_08()
    gen_boucle_inject_08()
    gen_player_state_08()
    gen_cortex_amb_08()
    gen_cortex_amb_behav_08()
    gen_cortex_pair_08()
