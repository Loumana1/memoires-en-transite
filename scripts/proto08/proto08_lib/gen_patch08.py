"""Construit pd/prototype_08_fsm_8hp.pd — Proto 08 8HP seulement.

Proto 06 figé. DSP partagé: fx_router_06, spatial_router_06, decode_8hp_06.
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(_REPO, "scripts"))
from shared.pdbuild import P
from . import presets08 as PR

PDDIR = os.path.join(_REPO, "pd")

DECLARE = ("#X declare -path .. -path . -path lib -path externals/iem_ambi-master"
           " -path externals/iemmatrix -lib iem_ambi -lib iemmatrix;")

CFG = dict(
    fname="prototype_08_fsm_8hp.pd",
    title="MET_PROTOTYPE_08_8HP",
    decode="lib/decode_8hp_06",
    dac="dac~ 1 2 3 4 5 6 7 8",
    nch=8,
    nhp=8,
    n_layers=PR.MAX_LAYERS_8HP,
    layer_gain=PR.CORTEX_LAYER_GAIN,
    amb_gain=PR.CORTEX_AMB_GAIN,
    inj_gain=0.16,
    fsm="lib/fsm_memory_08_8hp",
    presets="lib/fsm_presets_08_8hp",
    anchors=PR.ANCHORS_8HP,
    direct=[0, 1, 2, 3, 4, 5, 6, 7],
    visu=True,
    note="08 8HP | Cortex: 6x2 HP1-6 + 2 nappes HP5/HP7",
)


def build_engine(cfg):
    nl = cfg["n_layers"]
    gain = cfg["layer_gain"]
    bang_out = 3 + nl
    e = P(2000, max(1500, 500 + nl * 70 + 620), x=100, y=100)
    e.text(40, 20, "MOTEUR_08 genere par script - DSP fx/spatial/decode = 06")

    e.obj("r_auto", 40, 60, "r s6_auto")
    e.obj("r_force", 160, 60, "r s6_force")
    e.obj("r_sess", 280, 60, "r s6_session")
    e.obj("fsm", 40, 110, cfg["fsm"])
    e.con("r_auto", 0, "fsm", 0)
    e.con("r_force", 0, "fsm", 1)
    e.con("r_sess", 0, "fsm", 2)

    e.obj("prs", 340, 160, cfg["presets"])
    e.obj("s_var", 340, 200, "s s6_variante")
    e.obj("s_etat", 40, 160, "s s6_etat")
    e.con("fsm", 0, "s_etat", 0)
    e.con("fsm", 0, "prs", 1)
    e.con("fsm", 1, "prs", 0)
    e.con("prs", 0, "s_var", 0)

    e.obj("visu", 480, 160, "lib/visu_cerveau_06")
    e.con("fsm", 0, "visu", 0)

    e.obj("cxctrl", 640, 60, "lib/cortex_ctrl_08")
    e.obj("pres", 780, 60, "lib/presence_08")
    e.obj("rform", 920, 60, "lib/recon_formes_08")
    e.obj("hasoc", 1060, 60, "lib/hippo_assoc_08")
    e.obj("binj", 1200, 60, "lib/boucle_inject_08")
    e.obj("hmot", 1340, 60, "lib/hippo_motion_08")
    e.obj("cxpair", 1480, 60, "lib/cortex_pair_08")
    e.obj("cxamb", 1480, 100, "lib/cortex_amb_08")

    e.obj("f_n", 480, 110, "f 12")
    e.con("fsm", 2, "f_n", 0)
    e.obj("r_cn", 600, 110, "r s6_cortex_n")
    e.con("r_cn", 0, "f_n", 0)
    for k in range(2, nl):
        e.obj(f"ge{k}", 480 + (k - 2) * 70, 140, f">= {k}")
        e.con("f_n", 0, f"ge{k}", 0)

    # L13 nappe mobile: Hippo seulement (Cortex = 2 nappes HP5/HP7)
    e.obj("sel_amb", 1100, 110, "sel 1")
    e.msg("amb1", 1100, 140, "1")
    e.msg("amb0", 1180, 140, "0")
    e.con("fsm", 0, "sel_amb", 0)
    e.con("sel_amb", 0, "amb1", 0)
    e.con("sel_amb", 1, "amb0", 0)

    e.obj("selcxsp", 1280, 110, "sel 0")
    e.msg("m_cxon", 1280, 140, "1")
    e.msg("m_cxoff", 1340, 140, "0")
    e.msg("m_oton", 1400, 140, "1")
    e.msg("m_otoff", 1460, 140, "0")
    e.obj("pk_cx", 1280, 170, "pack 0 3")
    e.obj("ln_cx", 1280, 200, "line~")
    e.obj("pk_ot", 1400, 170, "pack 0 3")
    e.obj("ln_ot", 1400, 200, "line~")
    e.con("fsm", 0, "selcxsp", 0)
    e.con("selcxsp", 0, "m_cxon", 0)
    e.con("selcxsp", 0, "m_otoff", 0)
    e.con("selcxsp", 1, "m_cxoff", 0)
    e.con("selcxsp", 1, "m_oton", 0)
    e.con("m_cxon", 0, "pk_cx", 0)
    e.con("m_cxoff", 0, "pk_cx", 0)
    e.con("m_oton", 0, "pk_ot", 0)
    e.con("m_otoff", 0, "pk_ot", 0)
    e.con("pk_cx", 0, "ln_cx", 0)
    e.con("pk_ot", 0, "ln_ot", 0)
    e.obj("lb_sp", 1520, 140, "loadbang")
    e.con("lb_sp", 0, "m_cxoff", 0)
    e.con("lb_sp", 0, "m_oton", 0)

    for i in range(nl):
        y = 240 + i * 40
        e.obj(f"stt_{i}", 20, y - 18, "t f f")
        if i == 12:
            e.obj(f"selcx_{i}", 20, y, "sel 0 1")
            e.msg(f"mcx_{i}", 100, y, "40")
            e.msg(f"mhp_{i}", 100, y + 18, "41")
            e.obj(f"m3_{i}", 200, y, "* 3")
            e.obj(f"sa_{i}", 280, y, "+")
            e.con("fsm", 0, f"stt_{i}", 0)
            e.con(f"stt_{i}", 0, f"selcx_{i}", 0)
            e.con(f"selcx_{i}", 0, f"mcx_{i}", 0)
            e.con(f"selcx_{i}", 1, f"mhp_{i}", 0)
            e.con(f"selcx_{i}", 2, f"m3_{i}", 0)
            e.con("fsm", 3 + i, f"sa_{i}", 1)
            e.con(f"m3_{i}", 0, f"sa_{i}", 0)
        else:
            e.obj(f"selcx_{i}", 20, y, "sel 0 1")
            slot_cx = 20 + i
            e.msg(f"mcx_{i}", 100, y, str(slot_cx))
            e.obj(f"m3_{i}", 200, y, "* 3")
            e.obj(f"fb{i}", 280, y - 10, f"f {slot_cx}")
            e.obj(f"sa_{i}", 280, y, "+")
            e.con("fsm", 0, f"stt_{i}", 0)
            e.con(f"stt_{i}", 0, f"selcx_{i}", 0)
            e.con(f"selcx_{i}", 0, f"mcx_{i}", 0)
            e.con(f"selcx_{i}", 1, f"m3_{i}", 0)
            e.con(f"mcx_{i}", 0, f"fb{i}", 0)
            e.con(f"m3_{i}", 0, f"fb{i}", 0)
            e.con(f"fb{i}", 0, f"sa_{i}", 0)
            e.con("fsm", 3 + i, f"sa_{i}", 1)

    e.obj("r_ovl", 780, 140, "r s6_cortex_ovl")
    for i in range(nl):
        n = i + 1
        e.obj(f"del{n}", 640, 140 + i * 28, "delay 5")
    e.con("fsm", bang_out, "del1", 0)
    for i in range(1, nl):
        e.con("fsm", bang_out, f"del{i + 1}", 0)

    amb_gain = cfg["amb_gain"]
    e.obj("duck", 300, 720, "lib/hippo_duck_08")
    for i in range(nl):
        y = 400 + i * 58
        n = i + 1
        hp, az = cfg["anchors"][i]
        loop = 1
        if i < 12:
            pg = PR.GAIN_PREMIER_PLAN if i % 2 == 0 else PR.GAIN_ARRIERE_PLAN
            lg = gain * pg
        elif i == 12:
            lg = amb_gain
        else:
            lg = gain
        e.obj(f"p{n}", 40, y, f"lib/player_state_08 {loop}")
        e.obj(f"g{n}", 220, y, f"*~ {lg}")
        if i < 12:
            e.obj(f"trp{n}", 40, y - 22, "t b b")
            e.con(f"del{n}", 0, f"trp{n}", 0)
            e.con(f"trp{n}", 0, f"mcx_{i}", 0)
            e.con(f"trp{n}", 1, f"p{n}", 0)
        else:
            e.con(f"del{n}", 0, f"p{n}", 0)
        if i == 12:
            e.con(f"mhp_{i}", 0, f"p{n}", 1)
        e.con(f"sa_{i}", 0, f"p{n}", 1)
        e.con(f"p{n}", 0, f"g{n}", 0)
        e.obj(f"s_samp{n}", 40, y + 28, f"s s6_sample{n}")
        e.con(f"p{n}", 1, f"s_samp{n}", 0)
        src = f"g{n}"
        if i == 12:
            e.obj("pk13", 320, y - 25, "pack 0 3")
            e.obj("ln13", 320, y, "line~")
            e.obj("mul13", 400, y, "*~")
            e.obj("mul_dk", 560, y, "*~")
            e.con("amb1", 0, "pk13", 0)
            e.con("amb0", 0, "pk13", 0)
            e.con("pk13", 0, "ln13", 0)
            e.con("ln13", 0, "mul13", 1)
            e.con("g13", 0, "mul_dk", 0)
            e.con("mul_dk", 0, "mul13", 0)
            src = "mul13"
        elif i > 0 and i < 12:
            pass
        elif i > 0:
            ge = f"ge{i + 1}"
            e.obj(f"pk{n}", 320, y - 25, "pack 0 3")
            e.obj(f"ln{n}", 320, y, "line~")
            e.obj(f"mul{n}", 400, y, "*~")
            e.con(ge, 0, f"pk{n}", 0)
            e.con(f"pk{n}", 0, f"ln{n}", 0)
            e.con(f"ln{n}", 0, f"mul{n}", 1)
            e.con(f"g{n}", 0, f"mul{n}", 0)
            src = f"mul{n}"
        e.obj(f"fx{n}", 500, y, f"lib/fx_router_06 {n}")
        e.con(src, 0, f"fx{n}", 0)
        if i < 12:
            e.obj(f"cxg{n}", 560, y - 22, "*~")
            e.obj(f"otg{n}", 560, y, "*~")
            e.con(f"fx{n}", 0, f"cxg{n}", 0)
            e.con(f"fx{n}", 0, f"otg{n}", 0)
            e.con("ln_cx", 0, f"cxg{n}", 1)
            e.con("ln_ot", 0, f"otg{n}", 1)
            e.con(f"cxg{n}", 0, "cxpair", i)
        if i == 12:
            e.obj("r_am", 500, y - 48, "r s6_etat")
            e.obj("sel_am", 500, y - 28, "sel 1")
            e.msg("mv1", 620, y - 48, "1")
            e.msg("mv0", 680, y - 48, "0")
            e.msg("fix1", 740, y - 48, "1")
            e.msg("fix0", 800, y - 48, "0")
            e.obj("pk_mv", 620, y - 22, "pack 0 3")
            e.obj("ln_mv", 620, y, "line~")
            e.obj("mul_mv", 700, y, "*~")
            e.obj("pk_fx", 780, y - 22, "pack 0 3")
            e.obj("ln_fx", 780, y, "line~")
            e.obj("mul_fx", 860, y, "*~")
            e.con("r_am", 0, "sel_am", 0)
            e.con("sel_am", 0, "mv1", 0)
            e.con("sel_am", 0, "fix0", 0)
            e.con("sel_am", 1, "mv0", 0)
            e.con("sel_am", 1, "fix1", 0)
            e.con("mv1", 0, "pk_mv", 0)
            e.con("mv0", 0, "pk_mv", 0)
            e.con("fix1", 0, "pk_fx", 0)
            e.con("fix0", 0, "pk_fx", 0)
            e.con("pk_mv", 0, "ln_mv", 0)
            e.con("ln_mv", 0, "mul_mv", 1)
            e.con("pk_fx", 0, "ln_fx", 0)
            e.con("ln_fx", 0, "mul_fx", 1)
            e.con("fx13", 0, "mul_mv", 0)
            e.con("fx13", 0, "mul_fx", 0)
            e.obj("lb_am", 880, y - 48, "loadbang")
            e.con("lb_am", 0, "fix1", 0)
            e.con("lb_am", 0, "mv0", 0)
            e.obj("amb", 940, y, "lib/amb_route_08")
            e.obj("sr13", 940, y + 28,
                  f"lib/spatial_router_06 13 {az} {hp} {cfg['nhp']} {cfg['nhp'] - 1}")
            e.con("mul_fx", 0, "amb", 0)
            e.con("mul_mv", 0, "sr13", 0)
        else:
            e.obj(f"sr{n}", 640, y,
                  f"lib/spatial_router_06 {n} {az} {hp} {cfg['nhp']} {cfg['nhp'] - 1}")
            e.con(f"otg{n}", 0, f"sr{n}", 0)

    e.con("duck", 0, "mul_dk", 1)
    for i in range(4):
        e.con(f"g{i + 1}", 0, "duck", i)

    for layer in range(1, 3):
        lx = 40 + layer * 90
        e.obj(f"r_r{layer}", lx, 360, f"r s6_recon_b{layer}")
        e.obj(f"r_rc{layer}", lx, 380, f"r s6_recon_cut{layer}")
        e.con(f"r_r{layer}", 0, f"p{layer}", 0)
        e.con(f"r_rc{layer}", 0, f"p{layer}", 2)
    for layer in range(1, 5):
        lx = 120 + layer * 100
        e.obj(f"r_h{layer}", lx, 380, f"r s6_hippo_b{layer}")
        e.obj(f"r_c{layer}", lx, 400, f"r s6_hippo_cut{layer}")
        e.con(f"r_h{layer}", 0, f"p{layer}", 0)
        e.con(f"r_c{layer}", 0, f"p{layer}", 2)

    # inject Boucle one-shot (couche 10, hors n)
    yinj = 400 + nl * 58
    e.obj("pinj", 40, yinj, "lib/player_state_08 0")
    e.obj("ginj", 220, yinj, f"*~ {cfg['inj_gain']}")
    e.obj("r_inj", 40, yinj - 28, "r s6_boucle_bang")
    e.msg("mslot9", 160, yinj - 28, "9")
    e.obj("lb_inj", 280, yinj - 28, "loadbang")
    e.con("lb_inj", 0, "mslot9", 0)
    e.con("mslot9", 0, "pinj", 1)
    e.con("r_inj", 0, "pinj", 0)
    e.con("pinj", 0, "ginj", 0)
    e.obj("fxinj", 500, yinj, "lib/fx_router_06 14")
    e.obj("srinj", 640, yinj, f"lib/spatial_router_06 14 0 1 {cfg['nhp']} {cfg['nhp'] - 1}")
    e.con("ginj", 0, "fxinj", 0)
    e.con("fxinj", 0, "srinj", 0)
    e.msg("injfx", 780, yinj,
          "\\; s6_l14_mode 2 \\; s6_l14_step 1800 \\; s6_l14_xfade 40 \\; "
          "s6_l14_wet 0.18 \\; s6_l14_del 260 \\; s6_l14_fb 0.22 \\; s6_l14_on 1 \\; "
          "s6_l14_sat 0.12 \\; s6_l14_lpf 5500 \\; s6_l14_hpf 40")
    e.con("lb_inj", 0, "injfx", 0)
    e.obj("s_samp_inj", 40, yinj + 28, "s s6_sample_inj")
    e.con("pinj", 1, "s_samp_inj", 0)

    yamb = yinj + 80
    e.obj("r_et_amb", 40, yamb - 48, "r s6_etat")
    e.obj("chg_amb", 40, yamb - 24, "change")
    e.obj("sel_ambcx", 120, yamb - 24, "sel 0")
    e.obj("t_ambgo", 120, yamb - 48, "t b b")
    e.obj("lb_ambs", 200, yamb - 48, "loadbang")
    e.obj("ambbeh", 320, yamb + 20, "lib/cortex_amb_behav_08")
    for i in range(2):
        ya = yamb + i * 42
        e.obj(f"pamb{i}", 40, ya, "lib/player_state_08 1")
        e.msg(f"msamb{i}", 200, ya - 18, str(32 + i))
        e.msg(f"bang_amb{i}", 200, ya + 18, "bang")
        e.con("lb_ambs", 0, f"msamb{i}", 0)
        e.con("lb_ambs", 0, f"bang_amb{i}", 0)
        e.con("t_ambgo", i, f"bang_amb{i}", 0)
        e.con(f"msamb{i}", 0, f"pamb{i}", 1)
        e.con(f"bang_amb{i}", 0, f"pamb{i}", 0)
        e.obj(f"gamb{i}", 220, ya, f"*~ {amb_gain}")
        e.obj(f"fxamb{i}", 360, ya, f"lib/fx_router_06 {15 + i}")
        e.obj(f"cxag{i}", 480, ya, "*~")
        e.con(f"pamb{i}", 0, f"gamb{i}", 0)
        e.con(f"gamb{i}", 0, "ambbeh", i)
        e.con("ambbeh", i, f"fxamb{i}", 0)
        e.con(f"fxamb{i}", 0, f"cxag{i}", 0)
        e.con("ln_cx", 0, f"cxag{i}", 1)
        e.con(f"cxag{i}", 0, "cxamb", i)
        e.obj(f"s_amba{i}", 560, ya, f"s s6_sample_amb{i + 1}")
        e.con(f"pamb{i}", 1, f"s_amba{i}", 0)
    e.con("r_et_amb", 0, "chg_amb", 0)
    e.con("chg_amb", 0, "sel_ambcx", 0)
    e.con("sel_ambcx", 0, "t_ambgo", 0)

    dac_y = yamb + 2 * 42 + 70
    e.obj("dec", 640, dac_y, cfg["decode"])
    for n in range(1, nl):
        for c in range(3):
            e.con(f"sr{n}", c, "dec", c)
    for c in range(3):
        e.con("srinj", c, "dec", c)
        e.con("sr13", c, "dec", c)
    e.obj("r_mas", 40, dac_y + 40, "r s6_master")
    e.obj("dac", 640, dac_y + 140, cfg["dac"])
    e.obj("lb_lvl", 40, dac_y + 155, "loadbang")
    e.obj("mlvl", 120, dac_y + 155, "metro 100")
    e.con("lb_lvl", 0, "mlvl", 0)
    for k in range(cfg["nch"]):
        e.obj(f"vol{k}", 40 + k * 100, dac_y + 70, "*~ 1")
        e.con("dec", k, f"vol{k}", 0)
        e.con("r_mas", 0, f"vol{k}", 1)
        e.con(f"vol{k}", 0, "dac", k)
        e.obj(f"lvl{k}", 40 + k * 100, dac_y + 105, "env~ 16384")
        e.obj(f"snap{k}", 40 + k * 100, dac_y + 125, "snapshot~")
        e.obj(f"slvl{k}", 40 + k * 100, dac_y + 145, f"s s6_lvl{k + 1}")
        e.con(f"vol{k}", 0, f"lvl{k}", 0)
        e.con(f"lvl{k}", 0, f"snap{k}", 0)
        e.con("mlvl", 0, f"snap{k}", 0)
        e.con(f"snap{k}", 0, f"slvl{k}", 0)
    for n in range(1, nl):
        for k, vk in enumerate(cfg["direct"]):
            e.con(f"sr{n}", 3 + k, f"vol{vk}", 0)
    for k, vk in enumerate(cfg["direct"]):
        e.con("srinj", 3 + k, f"vol{vk}", 0)
        e.con("amb", k, f"vol{vk}", 0)
        e.con("sr13", 3 + k, f"vol{vk}", 0)
    for k in range(6):
        e.con("cxpair", k, f"vol{k}", 0)
    for k in range(cfg["nch"]):
        e.con("cxamb", k, f"vol{k}", 0)
    e.text(40, dac_y + 180, cfg["note"])
    return e


def build_debug(cfg):
    nl = cfg["n_layers"]
    d = P(1480, max(560, 80 + nl * 180 + 40), x=150, y=150)
    d.text(40, 14, "DEBUG_08 controles manuels par couche (INSTALL_MODE OFF)")
    d.text(40, 34, "mode: 0 dry | 1 rot | 2 saut | 3 seq | 4 local3-4 \\; L13=ambiance")
    params = [("rot", 5, 0, 2), ("step", 5, 100, 9000), ("xfade", 5, 0, 500),
              ("wet", 5, 0, 1), ("del", 5, 1, 3900), ("fb", 5, 0, 0.7),
              ("lfo", 5, 0, 5)]
    params2 = [("sat", 5, 0, 1), ("hpf", 5, 20, 1200), ("lpf", 5, 400, 20000),
               ("flfo", 5, 0, 1)]
    for i in range(1, nl + 1):
        y = 80 + (i - 1) * 180
        d.text(40, y, f"COUCHE_{i}")
        d.add(f"md{i}", f"#X obj {40} {y + 25} hradio 16 1 0 5 empty empty l{i}_mode 0 -8 0 10 #fcfcfc #000000 #000000 0;")
        d.obj(f"smd{i}", 40, y + 55, f"s s6_l{i}_mode")
        d.con(f"md{i}", 0, f"smd{i}", 0)
        d.add(f"sens{i}", f"#X obj 150 {y + 25} tgl 16 0 empty empty l{i}_sens 19 7 0 10 #fcfcfc #000000 #000000 0 1;")
        d.obj(f"ssens{i}", 150, y + 55, f"s s6_l{i}_sens")
        d.con(f"sens{i}", 0, f"ssens{i}", 0)
        d.add(f"on{i}", f"#X obj 250 {y + 25} tgl 16 0 empty empty l{i}_echo_on 19 7 0 10 #fcfcfc #000000 #000000 0 1;")
        d.obj(f"son{i}", 250, y + 55, f"s s6_l{i}_on")
        d.con(f"on{i}", 0, f"son{i}", 0)
        for j, (nm, w, lo, hi) in enumerate(params):
            x = 380 + j * 120
            d.add(f"fa_{nm}{i}", f"#X floatatom {x} {y + 25} {w} {lo} {hi} 0 l{i}_{nm} - - 0;")
            d.obj(f"s_{nm}{i}", x, y + 55, f"s s6_l{i}_{nm}")
            d.con(f"fa_{nm}{i}", 0, f"s_{nm}{i}", 0)
        for j, (nm, w, lo, hi) in enumerate(params2):
            x = 380 + j * 120
            d.add(f"fa_{nm}{i}", f"#X floatatom {x} {y + 90} {w} {lo} {hi} 0 l{i}_{nm} - - 0;")
            d.obj(f"s_{nm}{i}", x, y + 120, f"s s6_l{i}_{nm}")
            d.con(f"fa_{nm}{i}", 0, f"s_{nm}{i}", 0)
    d.text(40, 80 + nl * 180,
           "plafonds: wet .85 delay 800 fb .70 \\; sat 0-1 \\; LPF fragments Cortex 400-600")
    return d


def build():
    cfg = CFG
    nl = cfg["n_layers"]
    w, h = 1480, max(1100, 480 + (nl + 2) * 45 + 240)
    p = P(w, h, x=40, y=40, font=10)

    p.add("cnv_tr", "#X obj 40 40 cnv 15 300 120 empty empty TRANSPORT 10 14 0 13 #f0f0f0 #202020 0;")
    p.add("cnv_et", "#X obj 40 180 cnv 15 460 170 empty empty ETAT_FSM 10 14 0 13 #f8f0e8 #202020 0;")
    p.add("cnv_pr", "#X obj 40 370 cnv 15 460 190 empty empty PRESETS_V0 10 14 0 13 #e8f4e8 #202020 0;")
    p.add("cnv_im", "#X obj 360 40 cnv 15 300 120 empty empty INSTALLATION 10 14 0 13 #e8eef8 #202020 0;")
    p.add("cnv_pe", "#X obj 680 40 cnv 15 280 120 empty empty PRESENCE 10 14 0 13 #f8e8f0 #202020 0;")

    p.add("audio_on", "#X obj 60 85 tgl 19 0 empty r6_audio_set AUDIO_ON 22 8 0 10 #f0f0f0 #000000 #000000 0 1;")
    p.obj("ao_t", 60, 115, "t f f")
    p.add("dsp_msg", "#X msg 60 145 \\; pd dsp \\$1;")
    p.obj("sel_on", 160, 145, "sel 1")
    p.msg("m_stopd", 250, 145, "stop")
    p.obj("d_sess", 160, 175, "delay 200")
    p.obj("s_sess", 160, 205, "s s6_session")
    p.con("audio_on", 0, "ao_t", 0)
    p.con("ao_t", 0, "dsp_msg", 0)
    p.con("ao_t", 1, "sel_on", 0)
    p.con("sel_on", 0, "d_sess", 0)
    p.con("sel_on", 1, "m_stopd", 0)
    p.con("m_stopd", 0, "d_sess", 0)
    p.con("d_sess", 0, "s_sess", 0)
    p.add("master", "#X obj 380 155 hsl 140 16 0 2 0 1 empty empty MASTER 0 -8 0 10 #fcfcfc #000000 #000000 0 1.2;")
    p.obj("s_mas", 530, 155, "s s6_master")
    p.con("master", 0, "s_mas", 0)
    p.add("mas_d", "#X floatatom 530 175 5 0 0 0 - - - 0;")
    p.con("master", 0, "mas_d", 0)
    p.text(120, 88, cfg["note"])

    p.add("inst", "#X obj 380 85 tgl 19 0 empty r6_install_set INSTALL_MODE 22 8 0 10 #e8eef8 #000000 #000000 0 1;")
    p.obj("im", 380, 120, "lib/install_mode_06")
    p.obj("im_t", 500, 120, "t f f")
    p.msg("vis_mot", 500, 155, "\\; pd-moteur_08_8hp vis \\$1")
    p.msg("vis_dbg", 500, 190, "\\; pd-debug_08_8hp vis \\$1")
    p.con("inst", 0, "im", 0)
    p.con("im", 0, "im_t", 0)
    p.con("im_t", 1, "vis_mot", 0)
    p.con("im_t", 0, "vis_dbg", 0)

    p.add("input_on", "#X obj 700 70 tgl 18 0 empty empty INPUT_ON 21 8 0 10 #f8e8f0 #000000 #000000 0 1;")
    p.obj("s_in", 700, 100, "s s6_input_on")
    p.con("input_on", 0, "s_in", 0)
    p.add("rms_sim", "#X obj 820 70 tgl 18 0 empty empty RMS_SIM 21 8 0 10 #f8e8f0 #000000 #000000 0 1;")
    p.obj("s_sim", 820, 100, "s s6_rms_sim")
    p.con("rms_sim", 0, "s_sim", 0)
    p.text(700, 125, "piezo/micro: jamais vers HP")
    p.obj("r_rms", 700, 145, "r s6_presence_rms")
    p.add("rms_d", "#X floatatom 820 145 5 0 0 0 rms - - 0;")
    p.con("r_rms", 0, "rms_d", 0)

    p.add("fsm_auto", "#X obj 60 220 tgl 18 0 empty r6_auto_set FSM_AUTO 21 8 0 10 #f8f0e8 #000000 #000000 0 1;")
    p.obj("auto_t", 60, 250, "t f f")
    p.obj("s_auto", 150, 250, "s s6_auto")
    p.obj("eq_a0", 60, 280, "== 0")
    p.con("fsm_auto", 0, "auto_t", 0)
    p.con("auto_t", 1, "s_auto", 0)
    p.con("auto_t", 0, "eq_a0", 0)
    p.add("force_st", "#X obj 240 250 hradio 18 1 0 4 empty empty FORCE_ETAT 0 -8 0 10 #f8f0e8 #000000 #000000 0;")
    p.obj("spig_f", 240, 285, "spigot")
    p.obj("s_force", 240, 315, "s s6_force")
    p.con("force_st", 0, "spig_f", 0)
    p.con("eq_a0", 0, "spig_f", 1)
    p.con("spig_f", 0, "s_force", 0)
    p.text(240, 220, "0 Cortex 1 Hippocampe 2 Reconstruction 3 Boucle")
    p.obj("r_etat", 60, 315, "r s6_etat")
    p.add("etat_disp", "#X floatatom 130 315 5 0 3 0 etat_courant - - 0;")
    p.con("r_etat", 0, "etat_disp", 0)
    p.obj("r_var", 380, 285, "r s6_variante")
    p.add("var_disp", "#X floatatom 400 315 5 0 11 0 variante_id - - 0;")
    p.con("r_var", 0, "var_disp", 0)

    p.add("contr", "#X obj 560 250 tgl 18 0 empty r6_contraste_set CONTRASTE_HAUT 21 8 0 10 #f8f0e8 #000000 #000000 0 1;")
    p.obj("csel", 560, 285, "sel 0 1")
    p.msg("c_bas", 560, 320, str(PR.CONTRASTE_BAS))
    p.msg("c_haut", 630, 320, "1")
    p.obj("s_contr", 560, 355, "s s6_contraste_f")
    p.con("contr", 0, "csel", 0)
    p.con("csel", 0, "c_bas", 0)
    p.con("csel", 1, "c_haut", 0)
    p.con("c_bas", 0, "s_contr", 0)
    p.con("c_haut", 0, "s_contr", 0)

    for k, (name, auto, inst, contr) in enumerate(PR.PRESETS_V0):
        y = 410 + k * 36
        p.msg(f"pv{k}", 60, y,
              f"\\; r6_auto_set {auto} \\; r6_install_set {inst} \\; r6_contraste_set {contr}")
        p.text(340, y, name)

    samp_h = 40 + (nl + 2) * 38
    p.add("cnv_sam", f"#X obj 540 370 cnv 15 420 {samp_h} empty empty SAMPLES_EN_COURS 10 14 0 13 #fff8e8 #202020 0;")
    p.add("cnv_his", "#X obj 980 40 cnv 15 460 520 empty empty HISTORIQUE_CERVEAU 10 14 0 13 #f0f8ff #202020 0;")
    roles = [
        "HP1 A", "HP1 B", "HP2 A", "HP2 B", "HP3 A", "HP3 B",
        "HP4 A", "HP4 B", "HP5 A", "HP5 B", "HP6 A", "HP6 B",
        "nappe mobile L13",
    ]
    for i, role in enumerate(roles):
        y = 400 + i * 36
        p.text(560, y, f"couche {i + 1} - {role}")
        p.obj(f"r_sam{i+1}", 560, y + 16, f"r s6_sample{i + 1}")
        p.add(f"sam{i+1}", f"#X symbolatom 700 {y + 16} 28 0 0 0 - - - 0;")
        p.con(f"r_sam{i+1}", 0, f"sam{i+1}", 0)
    for i, label in enumerate(("musicale HP7", "texture HP5")):
        y = 400 + (nl + i) * 36
        p.text(560, y, f"nappe {label}")
        p.obj(f"r_amba{i}", 560, y + 16, f"r s6_sample_amb{i + 1}")
        p.add(f"samba{i}", f"#X symbolatom 700 {y + 16} 28 0 0 0 - - - 0;")
        p.con(f"r_amba{i}", 0, f"samba{i}", 0)

    p.text(1000, 70, "MAINTENANT")
    p.obj("r_nom", 1000, 95, "r s6_etat_nom")
    p.add("nom_cur", "#X symbolatom 1000 120 22 0 0 0 - - - 0;")
    p.con("r_nom", 0, "nom_cur", 0)
    p.obj("r_cdur", 1220, 95, "r s6_etat_dur")
    p.add("dur_cur", "#X floatatom 1220 120 8 0 0 0 sec - - 0;")
    p.con("r_cdur", 0, "dur_cur", 0)
    p.text(1000, 155, "PASSE (plus recent en haut)")
    p.text(1000, 175, "partie du cerveau")
    p.text(1220, 175, "duree s")
    for i in range(8):
        y = 200 + i * 40
        p.obj(f"r_hn{i}", 1000, y, f"r s6_hist_nom{i}")
        p.add(f"hn{i}", f"#X symbolatom 1000 {y + 18} 20 0 0 0 - - - 0;")
        p.con(f"r_hn{i}", 0, f"hn{i}", 0)
        p.obj(f"r_hd{i}", 1220, y, f"r s6_hist_dur{i}")
        p.add(f"hd{i}", f"#X floatatom 1220 {y + 18} 8 0 0 0 - - - 0;")
        p.con(f"r_hd{i}", 0, f"hd{i}", 0)

    boot_y = 400 + (nl + 2) * 36 + 80
    p.obj("lb", 60, boot_y, "loadbang")
    p.obj("lb_del", 60, boot_y + 30, "delay 100")
    p.msg("m_vol", 180, boot_y, "1.2")
    p.con("lb", 0, "lb_del", 0)
    p.con("lb", 0, "m_vol", 0)
    p.con("m_vol", 0, "s_mas", 0)
    p.con("lb_del", 0, "pv0", 0)
    p.msg("boot_inst", 180, boot_y + 30, "1")
    p.msg("boot_auto", 60, boot_y + 30, "1")
    p.con("lb", 0, "boot_inst", 0)
    p.con("lb", 0, "boot_auto", 0)
    p.con("boot_inst", 0, "inst", 0)
    p.con("boot_auto", 0, "fsm_auto", 0)

    p.obj("r_expo", 300, boot_y, "r r6_boot_expo")
    p.obj("d_expo", 300, boot_y + 30, "delay 250")
    p.obj("tx_expo", 300, boot_y + 60, "t b b")
    p.msg("m_au1", 380, boot_y + 30, "1")
    p.con("r_expo", 0, "d_expo", 0)
    p.con("d_expo", 0, "tx_expo", 0)
    p.con("tx_expo", 0, "pv0", 0)
    p.con("tx_expo", 1, "m_au1", 0)
    p.con("m_au1", 0, "audio_on", 0)

    p.sub("moteur", 60, boot_y + 65, "moteur_08_8hp", build_engine(cfg))
    p.sub("debug", 300, boot_y + 65, "debug_08_8hp", build_debug(cfg))

    out = os.path.join(PDDIR, cfg["fname"])
    p.write(out, declare=DECLARE)
    print(f"OK patch: {cfg['fname']} ({p.n} objets, {len(p.conns)} connexions)")
    return out
