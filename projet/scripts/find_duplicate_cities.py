#!/usr/bin/env python3
"""Trouve les noms de villes dupliqués dans le fichier CSV de pollution atmosphérique.

Usage:
  python projet/scripts/find_duplicate_cities.py              # utilise le chemin relatif par défaut
  python projet/scripts/find_duplicate_cities.py --path /chemin/vers/global_air_pollution_data.csv

Options:
  --min-count N    Nombre minimum d'occurrences pour afficher (défaut 2)
  --examples N     Nombre d'exemples à afficher par ville (défaut 3)
  --write-json f   Écrit le rapport des doublons en JSON dans le fichier `f`
"""
from collections import defaultdict, Counter
import csv
import argparse
import json
from pathlib import Path


def normalize(name: str) -> str:
    if name is None:
        return ""
    # Trim, collapse whitespace and casefold for robust matching
    s = " ".join(name.split())
    return s.casefold()


def find_duplicates(path: Path, min_count: int = 2, examples: int = 3):
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # detect city column
    city_col = None
    for c in (reader.fieldnames or []):
        if c and "city" in c.lower():
            city_col = c
            break
    if city_col is None:
        city_col = "city_name"

    counts = Counter()
    variants = defaultdict(set)
    examples_map = defaultdict(list)

    for r in rows:
        raw = r.get(city_col, "")
        norm = normalize(raw)
        counts[norm] += 1
        if raw is not None:
            variants[norm].add(raw)
        if len(examples_map[norm]) < examples:
            examples_map[norm].append(r)

    duplicates = [(n, counts[n]) for n in counts if counts[n] >= min_count and n != ""]
    duplicates.sort(key=lambda x: -x[1])

    report = {
        "file": str(path),
        "total_rows": len(rows),
        "city_column": city_col,
        "unique_normalized_cities": len(counts),
        "duplicates_count": len(duplicates),
        "duplicates": []
    }

    for norm, cnt in duplicates:
        item = {
            "normalized": norm,
            "count": cnt,
            "variants": sorted(list(variants[norm]))[:10],
            "examples": []
        }
        for ex in examples_map[norm]:
            # include some useful fields in example
            item["examples"].append({
                "country": ex.get("country_name"),
                "city": ex.get(city_col),
                "aqi": ex.get("aqi_value")
            })
        report["duplicates"].append(item)

    return report


def main():
    p = argparse.ArgumentParser(description="Trouve les noms de villes dupliqués dans un CSV")
    p.add_argument("--path", type=Path, default=Path(__file__).parent.parent / "data" / "global_air_pollution_data.csv")
    p.add_argument("--min-count", type=int, default=2)
    p.add_argument("--examples", type=int, default=3)
    p.add_argument("--write-json", type=Path, default=None)
    args = p.parse_args()

    path = args.path
    if not path.exists():
        print(f"Fichier introuvable: {path}")
        raise SystemExit(2)

    report = find_duplicates(path, min_count=args.min_count, examples=args.examples)

    print(f"Fichier: {report['file']}")
    print(f"Total lignes: {report['total_rows']}")
    print(f"Colonne ville détectée: {report['city_column']}")
    print(f"Noms de ville normalisés distincts: {report['unique_normalized_cities']}")
    print(f"Noms de ville apparaissant >= {args.min_count} fois: {report['duplicates_count']}\n")

    for d in report["duplicates"]:
        print(f"- '{d['normalized']}' : {d['count']} occurrences — variantes: {', '.join(d['variants'][:5])}")
        for ex in d["examples"]:
            print(f"    exemple: country={ex.get('country')}, city={ex.get('city')}, aqi={ex.get('aqi')}")
        print()

    if args.write_json:
        with args.write_json.open("w", encoding="utf-8") as jf:
            json.dump(report, jf, ensure_ascii=False, indent=2)
        print(f"Rapport JSON écrit dans: {args.write_json}")


if __name__ == "__main__":
    main()
