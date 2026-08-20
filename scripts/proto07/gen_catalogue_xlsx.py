#!/usr/bin/env python3
"""Génère docs/Matiere/catalogue_fragments.xlsx.

Feuilles :
  - Cortex, Hippocampe, Reconstruction — paroles uniquement (FRAGMENTS + LONG_MOYEN)
  - Ambiances — pool partagé SONS_V3/AMBIANCE/

Schéma : docs/Matiere/Attributs.md §5.
Colonnes vertes = auto. Le reste = à remplir à l'oreille.
Si le xlsx existe déjà, les cellules remplies sont conservées (clé = ID).
"""
from __future__ import annotations

import csv
import re
import sys
import wave
from pathlib import Path

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.comments import Comment
    from openpyxl.styles import Alignment, Font, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.table import Table, TableStyleInfo
except ImportError:
    sys.exit("pip3 install openpyxl")

ROOT = Path(__file__).resolve().parents[2]
SONS = ROOT / "SONS_V3"
AMBIANCE_DIR = SONS / "AMBIANCE"
REGISTRE = ROOT / "docs" / "Matiere" / "registre_ids.csv"
OUT = ROOT / "docs" / "Matiere" / "catalogue_fragments.xlsx"

ZONES = (
    ("CORTEX", "Cortex"),
    ("HIPPOCAMPE", "Hippocampe"),
    ("RECONSTRUCTION", "Reconstruction"),
)
BUCKET_TYPE = {
    "FRAGMENTS": "court",
    "LONG_MOYEN": "long",
}

# Paroles — une feuille par zone
PAROLE_COLUMNS = (
    ("id", "ID", True),
    ("type", "Type", True),
    ("duree_s", "Durée (s)", True),
    ("contexte", "Contexte", False),
    ("type_discours", "Type discours", False),
    ("fonction_sociale", "Fonction sociale", False),
    ("densite_parole", "Densité parole", False),
    ("famille_son", "Famille son", False),
    ("usage_prefere", "Usage préféré", False),
    ("notes", "Notes", False),
)

# Ambiances — pool partagé
AMBIANCE_COLUMNS = (
    ("id", "ID", True),
    ("duree_s", "Durée (s)", True),
    ("master", "Master", True),
    ("type_ambiance", "Type ambiance", False),
    ("activite", "Activité", False),
    ("continuite", "Continuité", False),
    ("espace", "Espace", False),
    ("presence_humaine", "Présence humaine", False),
    ("famille_son", "Famille son", False),
    ("usage_prefere", "Usage préféré", False),
    ("notes", "Notes", False),
)

NOTE_PAROLE = (
    "Vert = auto (SONS_V3/<zone>/FRAGMENTS|LONG_MOYEN). "
    "Contexte BELGIQUE/CONGO · discours · fonction · densité = paroles. "
    "Listes multiples séparées par +."
)
NOTE_AMBIANCE = (
    "Vert = auto (SONS_V3/AMBIANCE/, pool partagé). "
    "Type ambiance MUSICALE/TEXTURE · activité · continuité · espace · présence = ambiances. "
    "Usage préféré = où ce wav sert le mieux (cortex · nappe · hippo · recon…). "
    "Listes multiples séparées par +."
)

FILL_AUTO = PatternFill("solid", fgColor="C6EFCE")
FONT_AUTO = Font(color="006100", name="Calibri", size=11)
FILL_HEAD = PatternFill("solid", fgColor="1B4F3A")
FONT_HEAD = Font(color="FFFFFF", name="Calibri", size=11, bold=True)
FILL_NOTE = PatternFill("solid", fgColor="FFF2CC")
FONT_NOTE = Font(name="Calibri", size=10, italic=True, color="7F6000")
FONT_CELL = Font(name="Calibri", size=11)
THIN = Border(
    left=Side(style="thin", color="B8D4C4"),
    right=Side(style="thin", color="B8D4C4"),
    top=Side(style="thin", color="B8D4C4"),
    bottom=Side(style="thin", color="B8D4C4"),
)
WRAP = Alignment(wrap_text=True, vertical="center")

OLD_HEADER_MAP = {
    "id": "id",
    "type": "type",
    "phrase / parole (belgique · congo)": "_legacy_phrase",
    "attributs": "_legacy_attributs",
    "comportements": "_legacy_comportements",
}
AMBIANCE_SHEET = "Ambiances"
AMBIANCE_KEYS = {k for k, _, _ in AMBIANCE_COLUMNS}
PAROLE_KEYS = {k for k, _, _ in PAROLE_COLUMNS}
ALL_MANUAL = {k for k, _, manual in (*PAROLE_COLUMNS, *AMBIANCE_COLUMNS) if not manual}


def _natkey(name: str):
    return [int(x) if x.isdigit() else x.lower() for x in re.split(r"(\d+)", name)]


def _label_to_key(columns: tuple) -> dict[str, str]:
    return {label.lower(): key for key, label, _ in columns}


def wav_duration(path: Path) -> float:
    try:
        with wave.open(str(path), "rb") as w:
            rate = w.getframerate()
            if rate <= 0:
                return 0.0
            return w.getnframes() / rate
    except Exception:
        return 0.0


def load_registre_masters() -> dict[str, str]:
    if not REGISTRE.is_file():
        return {}
    out = {}
    with REGISTRE.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row.get("role") == "AMBIANCE" and row.get("id"):
                out[row["id"]] = row.get("src", "")
    return out


def scan_zone_parole(etat: str) -> list[dict]:
    rows = []
    for bucket, typ in BUCKET_TYPE.items():
        folder = SONS / etat / bucket
        if not folder.is_dir():
            continue
        for wav in sorted(folder.glob("*.wav"), key=lambda p: _natkey(p.name)):
            rows.append({
                "id": wav.stem,
                "type": typ,
                "duree_s": round(wav_duration(wav), 2),
                "_bucket": bucket,
            })
    rows.sort(key=lambda r: (r["type"] != "court", r["type"] != "long", _natkey(r["id"])))
    return rows


def scan_ambiances(masters: dict[str, str]) -> list[dict]:
    if not AMBIANCE_DIR.is_dir():
        return []
    rows = []
    for wav in sorted(AMBIANCE_DIR.glob("*.wav"), key=lambda p: _natkey(p.name)):
        stem = wav.stem
        rows.append({
            "id": stem,
            "duree_s": round(wav_duration(wav), 2),
            "master": masters.get(stem, ""),
        })
    return rows


def _norm_header(h: str) -> str:
    return re.sub(r"\s+", " ", str(h or "").strip().lower())


def _merge_legacy_notes(data: dict[str, str]) -> None:
    parts = []
    for leg in ("_legacy_phrase", "_legacy_attributs", "_legacy_comportements"):
        v = (data.pop(leg, "") or "").strip()
        if v:
            label = leg.replace("_legacy_", "").capitalize()
            parts.append(f"{label}: {v}")
    if parts and not (data.get("notes") or "").strip():
        data["notes"] = " | ".join(parts)
    elif parts:
        extra = " | ".join(parts)
        data["notes"] = f"{data['notes'].strip()} | [migré] {extra}"


def _detect_schema(headers: list[str]) -> tuple[str, list[str | None]]:
    """Retourne ('parole'|'ambiance'|'legacy', col_keys)."""
    hset = set(headers)
    if "master" in hset or "type ambiance" in hset:
        return "ambiance", [_label_to_key(AMBIANCE_COLUMNS).get(h) for h in headers]
    if "nature" in hset:
        return "parole_old", [_label_to_key(PAROLE_COLUMNS).get(h) or
                              {"nature": None, "durée (s)": "duree_s", "duree (s)": "duree_s"}.get(h)
                              for h in headers]
    is_old = len(headers) <= 5 and "durée (s)" not in hset and "duree (s)" not in hset
    if is_old:
        return "legacy", [OLD_HEADER_MAP.get(h) for h in headers]
    return "parole", [_label_to_key(PAROLE_COLUMNS).get(h) for h in headers]


def load_manual(path: Path) -> dict[str, dict[str, dict[str, str]]]:
    """sheet -> id -> {column_key: value}."""
    if not path.is_file():
        return {}
    wb = load_workbook(path, read_only=True, data_only=True)
    out: dict[str, dict[str, dict[str, str]]] = {}
    ambiance_pool: dict[str, dict[str, str]] = {}

    for name in wb.sheetnames:
        ws = wb[name]
        rows = list(ws.iter_rows(min_row=2, max_row=2, values_only=True))
        if not rows or not rows[0]:
            continue
        headers = [_norm_header(h) for h in rows[0]]
        schema, col_keys = _detect_schema(headers)

        by_id: dict[str, dict[str, str]] = {}
        for row in ws.iter_rows(min_row=3, values_only=True):
            if not row or not row[0]:
                continue
            sid = str(row[0]).strip()
            data: dict[str, str] = {}
            for i, key in enumerate(col_keys):
                if not key or i >= len(row):
                    continue
                val = row[i]
                if val is None:
                    continue
                s = str(val).strip()
                if s:
                    data[key] = s
            if schema == "legacy":
                _merge_legacy_notes(data)
            elif schema == "parole_old":
                nature = (data.pop("nature", "") or "").lower()
                if nature == "ambiance" or sid.upper().startswith("A"):
                    ambiance_pool[sid] = {k: v for k, v in data.items()
                                          if k in AMBIANCE_KEYS and k not in ("id", "duree_s", "master")}
                    continue
                data.pop("nature", None)
                for k in ("type_ambiance", "activite", "continuite", "espace", "presence_humaine"):
                    data.pop(k, None)
            manual = {k: v for k, v in data.items() if k in ALL_MANUAL}
            if manual:
                if name == AMBIANCE_SHEET or schema == "ambiance":
                    by_id[sid] = manual
                elif sid.upper().startswith("A") and any(k in AMBIANCE_KEYS for k in manual):
                    ambiance_pool.setdefault(sid, {}).update(manual)
                else:
                    by_id[sid] = manual
        if name == AMBIANCE_SHEET:
            out[name] = by_id
        elif name not in out:
            out[name] = by_id

    if ambiance_pool:
        amb = out.setdefault(AMBIANCE_SHEET, {})
        for sid, data in ambiance_pool.items():
            amb.setdefault(sid, {}).update(data)

    wb.close()
    return out


def write_sheet(
    wb: Workbook,
    title: str,
    note: str,
    columns: tuple,
    files: list,
    manual: dict,
    tab_color: str = "1B4F3A",
    type_comment_idx: int | None = 2,
):
    ws = wb.create_sheet(title)
    col_count = len(columns)
    last_col = get_column_letter(col_count)
    ws.merge_cells(f"A1:{last_col}1")
    c0 = ws["A1"]
    c0.value = f"{title}  ·  {len(files)} lignes  —  {note}"
    c0.fill = FILL_NOTE
    c0.font = FONT_NOTE
    c0.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[1].height = 48

    auto_keys = [k for k, _, is_auto in columns if is_auto]

    for col, (_, label, _) in enumerate(columns, 1):
        cell = ws.cell(2, col, label)
        cell.fill = FILL_HEAD
        cell.font = FONT_HEAD
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        cell.border = THIN

    kept = 0
    for i, auto in enumerate(files):
        r = 3 + i
        stem = auto["id"]
        prev = manual.get(stem, {})
        if prev:
            kept += 1

        for col, (key, _, is_auto) in enumerate(columns, 1):
            val = auto.get(key, "") if is_auto else prev.get(key, "")
            cell = ws.cell(r, col, val)
            cell.border = THIN
            cell.alignment = WRAP
            cell.font = FONT_AUTO if is_auto else FONT_CELL
            if is_auto:
                cell.fill = FILL_AUTO

        bucket = auto.get("_bucket")
        if type_comment_idx and bucket:
            ws.cell(r, type_comment_idx).comment = Comment(f"dossier {bucket}", "MET")
        ws.row_dimensions[r].height = 18

    last = 2 + max(len(files), 1)
    tab_name = re.sub(r"[^A-Za-z0-9]", "", title)[:20] + "Tab"
    table = Table(displayName=tab_name, ref=f"A2:{last_col}{last}")
    table.tableStyleInfo = TableStyleInfo(
        name="TableStyleMedium2", showRowStripes=True, showFirstColumn=False,
        showLastColumn=False, showColumnStripes=False,
    )
    ws.add_table(table)
    ws.freeze_panes = "A3"
    if title == AMBIANCE_SHEET:
        widths = (36, 10, 42, 14, 12, 12, 12, 16, 12, 14, 32)
    else:
        widths = (36, 10, 10, 12, 22, 22, 14, 12, 14, 32)
    for i, w in enumerate(widths[:col_count], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.sheet_properties.tabColor = tab_color
    return kept


def main():
    if not SONS.is_dir():
        sys.exit(f"SONS_V3/ introuvable: {SONS}")
    masters = load_registre_masters()
    manual = load_manual(OUT)
    wb = Workbook()
    wb.remove(wb.active)
    print("catalogue_fragments.xlsx")
    for etat, title in ZONES:
        files = scan_zone_parole(etat)
        kept = write_sheet(
            wb, title, f"{etat}/  ·  {NOTE_PAROLE}",
            PAROLE_COLUMNS, files, manual.get(title, {}),
        )
        print(f"  {title}: {len(files)} paroles (dont {kept} avec données conservées)")
    amb = scan_ambiances(masters)
    kept_a = write_sheet(
        wb, AMBIANCE_SHEET, NOTE_AMBIANCE,
        AMBIANCE_COLUMNS, amb, manual.get(AMBIANCE_SHEET, {}),
        tab_color="4A235A", type_comment_idx=None,
    )
    print(f"  {AMBIANCE_SHEET}: {len(amb)} ambiances (dont {kept_a} avec données conservées)")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    wb.save(OUT)
    print(f"OK {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
