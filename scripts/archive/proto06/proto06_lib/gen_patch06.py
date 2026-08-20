"""Construit pd/prototype_06_fsm_{4hp,6hp,8hp}.pd à partir des libs *_06.

Architecture (docs/10_proto_06_handoff_technique.md):
- UI épurée sur le canvas principal (TRANSPORT / ETAT_FSM / PRESETS_V0);
- panneau VISU (samples + historique cerveau) toujours visible (8HP);
- moteur audio complet dans le subpatch `moteur_06_<v>` (masquable);
- contrôles debug dans le subpatch `debug_06_<v>` (masquable);
- INSTALL_MODE ON = fenêtres moteur+debug fermées, OFF = ouvertes (L4);
- communication uniquement par send/receive s6_* (aucun câble inter-canvas).
"""
import os

from .pdbuild import P
from . import presets06 as PR

PDDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "pd"))

DECLARE = ("#X declare -path .. -path . -path lib -path externals/iem_ambi-master"
           " -path externals/iemmatrix -lib iem_ambi -lib iemmatrix;")

CFG = {
    "4hp": dict(
        fname="prototype_06_fsm_4hp.pd",
        title="MET_PROTOTYPE_06_4HP",
        decode="lib/decode_4hp_06",
        dac="dac~ 1 2 3 4",
        nch=4,
        nhp=4,
        n_layers=PR.MAX_LAYERS,
        layer_gain=0.4,
        fsm="lib/fsm_memory_06",
        presets="lib/fsm_presets_06",
        anchors=PR.ANCHORS_4HP,
        direct=[0, 1, 2, 3],
        visu=False,
        note="sorties carte 1-2-3-4 (L2) | gain 0.65 (L3)",
    ),
    "6hp": dict(
        fname="prototype_06_fsm_6hp.pd",
        title="MET_PROTOTYPE_06_6HP",
        decode="lib/decode_6hp_06",
        dac="dac~ 1 2 4 5 6",
        nch=5,
        nhp=5,
        n_layers=PR.MAX_LAYERS,
        layer_gain=0.4,
        fsm="lib/fsm_memory_06",
        presets="lib/fsm_presets_06",
        anchors=PR.ANCHORS_6HP,
        direct=[0, 1, 2, 3, 4],
        visu=False,
        note="sorties carte 1-2-4-5-6 - sortie 3 inutilisee (L2) | geometrie rectangle + paire mediane",
    ),
    "8hp": dict(
        fname="prototype_06_fsm_8hp.pd",
        title="MET_PROTOTYPE_06_8HP",
        decode="lib/decode_8hp_06",
        dac="dac~ 1 2 3 4 5 6 7 8",
        nch=8,
        nhp=8,
        n_layers=PR.MAX_LAYERS_8HP,
        layer_gain=0.14,
        fsm="lib/fsm_memory_06_8hp",
        presets="lib/fsm_presets_06_8hp",
        anchors=PR.ANCHORS_8HP,
        direct=[0, 1, 2, 3, 4, 5, 6, 7],
        visu=True,
        all_layers_loop=True,
        cortex_exclusive_slots=True,
        hippo_motion=True,
        note="sorties carte 1-8 | CORTEX 5x2 exclusifs | HIPPO sweep+local | pas de sample principal",
    ),
}


# ---------------------------------------------------------------------------
def build_engine(cfg):
    """Subpatch moteur: FSM + presets + N lecteurs -> FX -> SPAT -> decode -> dac."""
    nl = cfg["n_layers"]
    gain = cfg["layer_gain"]
    bang_out = 3 + nl  # outlet index of bang lecteurs
    e = P(1600, max(920, 380 + nl * 70 + 280), x=100, y=100)
    e.text(40, 20, "MOTEUR_INTERNE_06 (NON_MODIFIABLE) - genere par script;")

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

    if cfg.get("visu"):
        e.obj("visu", 480, 160, "lib/visu_cerveau_06")
        e.con("fsm", 0, "visu", 0)

    # gates couches 2..N: >= k  (+ mute HIPPO sweep via s6_hippo_solo)
    e.obj("f_n", 480, 80, "f 1")
    e.con("fsm", 2, "f_n", 1)
    for k in range(2, nl + 1):
        e.obj(f"ge{k}", 480 + (k - 2) * 80, 110, f">= {k}")
        e.con("f_n", 0, f"ge{k}", 0)
    if cfg.get("hippo_motion"):
        e.obj("r_solo", 900, 80, "r s6_hippo_solo")
        e.obj("sel_solo", 900, 110, "sel 1")
        e.obj("hmot", 1040, 80, "lib/hippo_motion_06")
        e.con("r_solo", 0, "sel_solo", 0)
        # solo=1 → forcer gates couches 2+ à 0 ; sinon re-bang n
        for k in range(2, nl + 1):
            e.msg(f"m0_{k}", 900 + (k - 2) * 40, 180, "0")
            e.con("sel_solo", 0, f"m0_{k}", 0)
            e.con(f"m0_{k}", 0, f"ge{k}", 0)
        e.con("sel_solo", 1, "f_n", 0)

    for i in range(nl):
        y = 240 + i * 40
        # 8HP CORTEX: slot fixe 20+i (fragment exclusif / couche).
        # Autres états: state*3+durée (COURT/MOYEN/LONG) comme 4/6HP.
        if cfg.get("cortex_exclusive_slots"):
            e.obj(f"stt_{i}", 20, y - 18, "t f f")
            e.obj(f"selcx_{i}", 20, y, "sel 0")
            e.msg(f"mcx_{i}", 100, y, str(20 + i))
            e.obj(f"m3_{i}", 200, y, "* 3")
            e.obj(f"sa_{i}", 280, y, "+")
            e.con("fsm", 0, f"stt_{i}", 0)
            e.con(f"stt_{i}", 0, f"selcx_{i}", 0)
            e.con(f"selcx_{i}", 0, f"mcx_{i}", 0)
            e.con(f"selcx_{i}", 1, f"m3_{i}", 0)
            e.con("fsm", 3 + i, f"sa_{i}", 1)
            e.con(f"m3_{i}", 0, f"sa_{i}", 0)
        else:
            e.obj(f"m3_{i}", 40, y, "* 3")
            e.obj(f"sa_{i}", 130, y, "+")
            e.con("fsm", 0, f"m3_{i}", 0)
            e.con("fsm", 3 + i, f"sa_{i}", 1)
            e.con(f"m3_{i}", 0, f"sa_{i}", 0)

    # chaîne bang: couche1 immédiat, couche2 après cortex_ovl, puis cascade 80 ms
    e.obj("r_ovl", 780, 110, "r s6_cortex_ovl")
    for i in range(nl):
        n = i + 1
        e.obj(f"del{n}", 640, 110 + i * 50, "delay 80")
    e.con("fsm", bang_out, "del1", 0)
    if nl >= 2:
        e.con("del1", 0, "del2", 0)
        e.con("r_ovl", 0, "del2", 1)
    for i in range(2, nl):
        e.con(f"del{i}", 0, f"del{i + 1}", 0)

    # 8HP CORTEX: toutes les couches en loop (pas de « sample principal »)
    all_loop = bool(cfg.get("all_layers_loop"))
    for i in range(nl):
        y = 380 + i * 60
        n = i + 1
        hp, az = cfg["anchors"][i]
        loop = 1 if (all_loop or i == 0) else 0
        e.obj(f"p{n}", 40, y, f"lib/player_state_06 {loop}")
        e.obj(f"g{n}", 220, y, f"*~ {gain}")
        if cfg.get("cortex_exclusive_slots"):
            e.con(f"mcx_{i}", 0, f"p{n}", 1)
            e.con(f"sa_{i}", 0, f"p{n}", 1)
        else:
            e.con(f"sa_{i}", 0, f"p{n}", 1)
        e.con(f"del{n}", 0, f"p{n}", 0)
        e.con(f"p{n}", 0, f"g{n}", 0)
        e.obj(f"s_samp{n}", 40, y + 30, f"s s6_sample{n}")
        e.con(f"p{n}", 1, f"s_samp{n}", 0)
        src = f"g{n}"
        if i > 0:
            ge = f"ge{i + 1}"
            e.obj(f"pk{n}", 320, y - 25, "pack 0 30")
            e.obj(f"ln{n}", 320, y, "line~")
            e.obj(f"mul{n}", 400, y, "*~")
            e.con(ge, 0, f"pk{n}", 0)
            e.con(f"pk{n}", 0, f"ln{n}", 0)
            e.con(f"ln{n}", 0, f"mul{n}", 1)
            e.con(f"g{n}", 0, f"mul{n}", 0)
            src = f"mul{n}"
        e.obj(f"fx{n}", 500, y, f"lib/fx_router_06 {n}")
        e.obj(f"sr{n}", 640, y,
              f"lib/spatial_router_06 {n} {az} {hp} {cfg['nhp']} {cfg['nhp'] - 1}")
        e.con(src, 0, f"fx{n}", 0)
        e.con(f"fx{n}", 0, f"sr{n}", 0)

    dac_y = 380 + nl * 60 + 80
    e.obj("dec", 640, dac_y, cfg["decode"])
    for n in range(1, nl + 1):
        for c in range(3):
            e.con(f"sr{n}", c, "dec", c)
    e.obj("dac", 640, dac_y + 140, cfg["dac"])
    for k in range(cfg["nch"]):
        e.obj(f"vol{k}", 40 + k * 100, dac_y + 70, "*~ 0.65")
        e.con("dec", k, f"vol{k}", 0)
        e.con(f"vol{k}", 0, "dac", k)
        e.obj(f"lvl{k}", 40 + k * 100, dac_y + 105, "env~ 16384")
        e.obj(f"slvl{k}", 40 + k * 100, dac_y + 125, f"s s6_lvl{k + 1}")
        e.con(f"vol{k}", 0, f"lvl{k}", 0)
        e.con(f"lvl{k}", 0, f"slvl{k}", 0)
    for n in range(1, nl + 1):
        for k, vk in enumerate(cfg["direct"]):
            e.con(f"sr{n}", 3 + k, f"vol{vk}", 0)
    e.text(40, dac_y + 180, cfg["note"] + ";")
    return e


# ---------------------------------------------------------------------------
def build_debug(cfg):
    """Subpatch debug: controles manuels par couche (send s6_l*_*)."""
    nl = cfg["n_layers"]
    d = P(1480, max(560, 80 + nl * 180 + 40), x=150, y=150)
    d.text(40, 14, "DEBUG_06 - controles manuels par couche (INSTALL_MODE OFF);")
    d.text(40, 34, "mode: 0 dry | 1 rot | 2 saut | 3 seq | 4 local3-4 \\; FX: sat -> filtre -> echo;")
    params = [("rot", 5, 0, 2), ("step", 5, 100, 9000), ("xfade", 5, 0, 500),
              ("wet", 5, 0, 1), ("del", 5, 1, 3900), ("fb", 5, 0, 0.7),
              ("lfo", 5, 0, 5)]
    params2 = [("sat", 5, 0, 1), ("hpf", 5, 20, 1200), ("lpf", 5, 400, 20000),
               ("flfo", 5, 0, 1)]
    for i in range(1, nl + 1):
        y = 80 + (i - 1) * 180
        d.text(40, y, f"COUCHE_{i};")
        d.add(f"md{i}", f"#X obj 40 {y + 25} hradio 16 1 0 5 empty empty l{i}_mode 0 -8 0 10 #fcfcfc #000000 #000000 0;")
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
           "plafonds: wet .85 delay 800 fb .70 \\; sat 0-1 \\; hpf 20-1200 \\; lpf 400-20k;")
    return d


# ---------------------------------------------------------------------------
def build(variant):
    cfg = CFG[variant]
    nl = cfg["n_layers"]
    w, h = (1480, max(900, 420 + nl * 45 + 200)) if cfg.get("visu") else (1100, 700)
    p = P(w, h, x=40, y=40, font=10)

    p.add("cnv_tr", "#X obj 40 40 cnv 15 300 120 empty empty TRANSPORT 10 14 0 13 #f0f0f0 #202020 0;")
    p.add("cnv_et", "#X obj 40 180 cnv 15 460 170 empty empty ETAT_FSM 10 14 0 13 #f8f0e8 #202020 0;")
    p.add("cnv_pr", "#X obj 40 370 cnv 15 460 190 empty empty PRESETS_V0 10 14 0 13 #e8f4e8 #202020 0;")
    p.add("cnv_im", "#X obj 360 40 cnv 15 300 120 empty empty INSTALLATION 10 14 0 13 #e8eef8 #202020 0;")

    p.add("audio_on", "#X obj 60 85 tgl 19 0 empty empty AUDIO_ON 22 8 0 10 #f0f0f0 #000000 #000000 0 1;")
    p.obj("ao_t", 60, 115, "t f f")
    p.add("dsp_msg", "#X msg 60 145 \\; pd dsp \\$1;")
    p.obj("sel_on", 160, 145, "sel 1")
    p.obj("s_sess", 160, 175, "s s6_session")
    p.con("audio_on", 0, "ao_t", 0)
    p.con("ao_t", 1, "dsp_msg", 0)
    p.con("ao_t", 0, "sel_on", 0)
    p.con("sel_on", 0, "s_sess", 0)
    p.text(120, 88, cfg["note"] + ";")

    p.add("inst", "#X obj 380 85 tgl 19 0 empty r6_install_set INSTALL_MODE 22 8 0 10 #e8eef8 #000000 #000000 0 1;")
    p.obj("im", 380, 120, "lib/install_mode_06")
    p.obj("im_t", 500, 120, "t f f")
    p.msg("vis_mot", 500, 155, f"\\; pd-moteur_06_{variant} vis \\$1")
    p.msg("vis_dbg", 500, 190, f"\\; pd-debug_06_{variant} vis \\$1")
    p.con("inst", 0, "im", 0)
    p.con("im", 0, "im_t", 0)
    p.con("im_t", 1, "vis_mot", 0)
    p.con("im_t", 0, "vis_dbg", 0)

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
    p.text(240, 220, "0 Cortex 1 Hippocampe 2 Reconstruction 3 Boucle;")
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
        p.text(340, y, name + ";")

    # --- VISU (8HP): samples en cours + historique cerveau ---
    if cfg.get("visu"):
        samp_h = 40 + nl * 38
        p.add("cnv_sam", f"#X obj 540 370 cnv 15 420 {samp_h} empty empty SAMPLES_EN_COURS 10 14 0 13 #fff8e8 #202020 0;")
        p.add("cnv_his", "#X obj 980 40 cnv 15 460 520 empty empty HISTORIQUE_CERVEAU 10 14 0 13 #f0f8ff #202020 0;")
        roles = (["principal (fond)"]
                 + [f"interference {i}" for i in range(1, nl)])
        for i, role in enumerate(roles):
            y = 400 + i * 36
            p.text(560, y, f"couche {i + 1} — {role};")
            p.obj(f"r_sam{i+1}", 560, y + 16, f"r s6_sample{i + 1}")
            p.add(f"sam{i+1}", f"#X symbolatom 700 {y + 16} 28 0 0 0 - - - 0;")
            p.con(f"r_sam{i+1}", 0, f"sam{i+1}", 0)

        p.text(1000, 70, "MAINTENANT;")
        p.obj("r_nom", 1000, 95, "r s6_etat_nom")
        p.add("nom_cur", "#X symbolatom 1000 120 22 0 0 0 - - - 0;")
        p.con("r_nom", 0, "nom_cur", 0)
        p.obj("r_cdur", 1220, 95, "r s6_etat_dur")
        p.add("dur_cur", "#X floatatom 1220 120 8 0 0 0 sec - - 0;")
        p.con("r_cdur", 0, "dur_cur", 0)
        p.text(1000, 155, "PASSE (plus recent en haut);")
        p.text(1000, 175, "partie du cerveau;")
        p.text(1220, 175, "duree s;")
        for i in range(8):
            y = 200 + i * 40
            p.obj(f"r_hn{i}", 1000, y, f"r s6_hist_nom{i}")
            p.add(f"hn{i}", f"#X symbolatom 1000 {y + 18} 20 0 0 0 - - - 0;")
            p.con(f"r_hn{i}", 0, f"hn{i}", 0)
            p.obj(f"r_hd{i}", 1220, y, f"r s6_hist_dur{i}")
            p.add(f"hd{i}", f"#X floatatom 1220 {y + 18} 8 0 0 0 - - - 0;")
            p.con(f"r_hd{i}", 0, f"hd{i}", 0)

    # init: 8HP ouvre en edition (VISU lisible); autres = mode_automatique
    boot_y = 600 if not cfg.get("visu") else 400 + nl * 36 + 80
    p.obj("lb", 60, boot_y, "loadbang")
    p.obj("lb_del", 60, boot_y + 30, "delay 100")
    p.con("lb", 0, "lb_del", 0)
    boot = "pv1" if cfg.get("visu") else "pv2"  # edition_complete vs automatique
    p.con("lb_del", 0, boot, 0)

    p.sub("moteur", 60, boot_y + 65, f"moteur_06_{variant}", build_engine(cfg))
    p.sub("debug", 300, boot_y + 65, f"debug_06_{variant}", build_debug(cfg))

    out = os.path.join(PDDIR, cfg["fname"])
    p.write(out, declare=DECLARE)
    print(f"OK patch: {cfg['fname']} ({p.n} objets, {len(p.conns)} connexions)")
    return out
