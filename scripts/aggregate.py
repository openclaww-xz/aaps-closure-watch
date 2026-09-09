#!/usr/bin/env python3
"""Aggregate AAPS tract B01001 -> district time series + deliverables.

Vintage rule (verified against parsed tract sets):
- 2009-2019 releases use 2010-vintage tract boundaries -> aaps_tracts_2010vintage.csv pct_in
- 2020-2024 releases use 2020-vintage boundaries       -> aaps_tracts.csv pct_in
Cross-boundary tracts weighted by pct_in (areal); MOE via census independent-sum formula.
Tracts with pct_in < 5 dropped (negligible, avoids noise).
"""
import csv, json, math, os

RAWP = "/tmp/aaps-research/population/raw/parsed"
OUT = "/tmp/aaps-research/population"
BANDS = ["0-4", "5-9", "10-14", "15-17"]
YEARS = list(range(2009, 2025))


def moe_of(terms):
    return 1.645 * math.sqrt(terms)


def load_pct(year):
    src = "/tmp/aaps_geo/aaps_tracts_2010vintage.csv" if year <= 2019 else "/tmp/aaps_geo/aaps_tracts.csv"
    pct, name = {}, {}
    with open(src) as f:
        for r in csv.DictReader(f):
            p = float(r["pct_in"])
            if p >= 5.0:
                pct[r["GEOID"]] = p / 100.0
                name[r["GEOID"]] = r.get("NAMELSAD10") or r.get("NAMELSAD", "")
    return pct, name


def bands_of(d):
    """combined-sex bands from parsed tract dict."""
    out = {"total": (d["total"][0], d["total"][1])}
    for b in BANDS:
        em, mm = d[f"{b}_m"]
        ef, mf = d[f"{b}_f"]
        out[b] = (em + ef, 1.645 * math.sqrt((mm / 1.645) ** 2 + (mf / 1.645) ** 2))
    return out


def main():
    long_rows, summary = [], {}
    vintage_note = {}
    for y in YEARS:
        data = json.load(open(f"{RAWP}/{y}.json"))
        pct, name = load_pct(y)
        vintage_note[y] = "2010" if y <= 2019 else "2020"
        matched = set(data) & set(pct)
        for g in sorted(matched):
            w = pct[g]
            bands = bands_of(data[g])
            for b, (e, m) in bands.items():
                long_rows.append({
                    "year_window": f"{y-4}-{y}",
                    "GEOID": g,
                    "age_band": b,
                    "estimate": e,
                    "moe": m,
                    "weighted_estimate": round(e * w, 1),
                    "weighted_moe": round(m * w, 1),
                    "pct_in": round(w * 100, 1),
                    "tract_name": name.get(g, ""),
                })
                s = summary.setdefault((y, b), {"est": 0.0, "terms": 0.0, "unw": 0, "n": 0})
                s["est"] += e * w
                s["terms"] += (m * w / 1.645) ** 2
                s["unw"] += e
                s["n"] += 1

    with open(f"{OUT}/aaps_tract_age_timeseries.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(long_rows[0].keys()))
        w.writeheader()
        w.writerows(long_rows)

    rows = []
    for y in YEARS:
        tot = summary[(y, "total")]
        e517 = sum(summary[(y, b)]["est"] for b in ["5-9", "10-14", "15-17"])
        t517 = sum(summary[(y, b)]["terms"] for b in ["5-9", "10-14", "15-17"])
        e04 = summary[(y, "0-4")]
        rows.append({
            "year_window": f"{y-4}-{y}",
            "end_year": y,
            "tract_vintage": vintage_note[y],
            "tracts_matched": tot["n"],
            "total_pop": round(tot["est"]),
            "total_pop_moe": round(1.645 * math.sqrt(tot["terms"])),
            "age_0_4": round(e04["est"]),
            "age_0_4_moe": round(1.645 * math.sqrt(e04["terms"])),
            "age_5_17": round(e517),
            "age_5_17_moe": round(1.645 * math.sqrt(t517)),
            "age_5_9": round(summary[(y, "5-9")]["est"]),
            "age_5_9_moe": round(1.645 * math.sqrt(summary[(y, "5-9")]["terms"])),
            "age_10_14": round(summary[(y, "10-14")]["est"]),
            "age_10_14_moe": round(1.645 * math.sqrt(summary[(y, "10-14")]["terms"])),
            "age_15_17": round(summary[(y, "15-17")]["est"]),
            "age_15_17_moe": round(1.645 * math.sqrt(summary[(y, "15-17")]["terms"])),
            "pct_5_17_of_total": round(100 * e517 / tot["est"], 1),
            "pct_0_4_of_total": round(100 * e04["est"] / tot["est"], 1),
        })
    with open(f"{OUT}/aaps_summary_trend.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    for r in rows:
        print(r["year_window"], "v", r["tract_vintage"], "n", r["tracts_matched"],
              "tot", r["total_pop"], "| 0-4", r["age_0_4"], "+/-", r["age_0_4_moe"],
              "| 5-17", r["age_5_17"], "+/-", r["age_5_17_moe"])


if __name__ == "__main__":
    main()
