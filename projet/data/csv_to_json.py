import csv, json

def to_int(x):
    x = (x or "").strip()
    return int(float(x)) if x else None

def clean_key(k: str) -> str:
    return (k or "").replace("\ufeff", "").replace("\t", "").strip()

def clean_val(v: str) -> str:
    # NBSP + trim (au cas où)
    return (v or "").replace("\xa0", " ").strip()

def clean_row(row: dict) -> dict:
    return {clean_key(k): clean_val(v) for k, v in row.items()}

in_path = "projet/data/global_air_pollution_data.csv"
out_path = "projet/data/pollution_facelift.json"

out = {"measurements": []}
skipped = 0

with open(in_path, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for lineno, raw in enumerate(reader, start=2):  # 1 = header
        r = clean_row(raw)

        country = r.get("country_name", "")
        city = r.get("city_name", "")

        if not country or not city:
            skipped += 1
            # Décommenter pour voir les premières lignes problématiques :
            if skipped <= 5:
                print(f"[SKIP line {lineno}] country='{country}' city='{city}' row_keys={list(r.keys())}")
            continue

        out["measurements"].append({
            "country_name": country,
            "city_name": city,
            "aqi": {"value": to_int(r.get("aqi_value")), "category": r.get("aqi_category")},
            "iaqi": {
                "co":   {"value": to_int(r.get("co_aqi_value")),    "category": r.get("co_aqi_category")},
                "o3":   {"value": to_int(r.get("ozone_aqi_value")), "category": r.get("ozone_aqi_category")},
                "no2":  {"value": to_int(r.get("no2_aqi_value")),   "category": r.get("no2_aqi_category")},
                "pm25": {"value": to_int(r.get("pm2.5_aqi_value")), "category": r.get("pm2.5_aqi_category")},
            }
        })

with open(out_path, "w", encoding="utf-8") as g:
    json.dump(out, g, ensure_ascii=False, indent=2)

print(f"OK -> {out_path} ({len(out['measurements'])} lignes) | skipped={skipped}")
