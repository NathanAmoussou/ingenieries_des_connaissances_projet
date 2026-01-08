#!/usr/bin/env python3
"""Détecte les valeurs dupliquées dans une colonne d'un fichier Excel.

Usage:
  python projet/scripts/find_duplicate_excel_column.py
  python projet/scripts/find_duplicate_excel_column.py --path ./projet/data/Share_of_green_areas_and_green_area_per_capita_in_cities_and_urban_areas_1990_-_2020.xlsx --sheet Data --column Share_of_green_areas

Le script tente d'importer `pandas`; si absent, affiche les instructions d'installation.
"""
from collections import Counter, defaultdict
import argparse
from pathlib import Path
import json
import sys


def normalize(v):
    if v is None:
        return ""
    s = str(v)
    return " ".join(s.split()).casefold()


def main():
    p = argparse.ArgumentParser(description="Trouve les valeurs dupliquées dans une colonne Excel")
    p.add_argument("--path", type=Path, default=Path(__file__).parent.parent / "data" / "Share_of_green_areas_and_green_area_per_capita_in_cities_and_urban_areas_1990_-_2020.xlsx")
    p.add_argument("--sheet", default="Data")
    p.add_argument("--column", default="Share_of_green_areas")
    p.add_argument("--min-count", type=int, default=2)
    p.add_argument("--examples", type=int, default=3)
    p.add_argument("--write-json", type=Path, default=None)
    args = p.parse_args()

    try:
        import pandas as pd
    except Exception:
        print("Le module 'pandas' est requis pour lire les fichiers Excel.")
        print("Installez-le avec: pip install pandas openpyxl")
        raise SystemExit(2)

    path = args.path
    if not path.exists():
        print(f"Fichier introuvable: {path}")
        raise SystemExit(2)

    xl = pd.read_excel(path, sheet_name=args.sheet)

    print(f"Feuille chargée: {args.sheet} — colonnes disponibles:")
    for c in xl.columns:
        print(" -", c)

    col = args.column
    if col not in xl.columns:
        print(f"\nColonne '{col}' non trouvée dans la feuille. Spécifiez --column avec l'un des noms ci-dessus.")
        raise SystemExit(2)

    values = xl[col].fillna("")
    norm_map = defaultdict(list)
    counts = Counter()

    for idx, v in values.items():
        n = normalize(v)
        counts[n] += 1
        if len(norm_map[n]) < args.examples:
            # store a small context (index + row subset)
            row = xl.loc[idx].to_dict()
            norm_map[n].append({"index": int(idx), "value": row.get(col), "row": {k: row.get(k) for k in list(xl.columns)[:6]}})

    duplicates = [(n, counts[n]) for n in counts if counts[n] >= args.min_count and n != ""]
    duplicates.sort(key=lambda x: -x[1])

    report = {
        "file": str(path),
        "sheet": args.sheet,
        "column": col,
        "total_rows": len(xl),
        "unique_normalized_values": len(counts),
        "duplicates_count": len(duplicates),
        "duplicates": []
    }

    for n, c in duplicates:
        report_entry = {"normalized": n, "count": c, "examples": norm_map[n]}
        report["duplicates"].append(report_entry)

    # print summary
    print(f"\nTotal lignes: {report['total_rows']}")
    print(f"Valeurs normalisées distinctes: {report['unique_normalized_values']}")
    print(f"Valeurs apparaissant >= {args.min_count} fois: {report['duplicates_count']}\n")

    for d in report["duplicates"][:50]:
        variants = [str(e["value"]) for e in d["examples"]]
        print(f"- '{d['normalized']}' : {d['count']} occurrences — exemples: {variants}")
        for ex in d["examples"]:
            print(f"    index={ex['index']}, value={ex['value']}, row_sample={ex['row']}")
        print()

    if args.write_json:
        with args.write_json.open("w", encoding="utf-8") as jf:
            json.dump(report, jf, ensure_ascii=False, indent=2)
        print(f"Rapport JSON écrit: {args.write_json}")


if __name__ == '__main__':
    main()
