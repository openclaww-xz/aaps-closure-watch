#!/usr/bin/env python3
"""Compute headline numbers + per-tract change highlights for the analysis doc."""
import csv, json, math

OUT = "/tmp/aaps-research/population"
rows = list(csv.DictReader(open(f"{OUT}/aaps_summary_trend.csv")))
by = {int(r["end_year"]): r for r in rows}


def pct(a, b):
    return round(100 * (float(b) - float(a)) / float(a), 1)


# Non-overlapping anchors: 2005-09, 2010-14, 2015-19, 2020-24
for band, col in [("5-17", "age_5_17"), ("0-4", "age_0_4"), ("total", "total_pop")]:
    a09, a14, a19, a24 = by[2009][col], by[2014][col], by[2019][col], by[2024][col]
    print(f"{band}: 2009={a09} 2014={a14} 2019={a19} 2024={a24} | 09->24 {pct(a09,a24)}% | 09->14 {pct(a09,a14)}% 14->19 {pct(a14,a19)}% 19->24 {pct(a19,a24)}%")

# MOE-significance of 5-17 change 2009 vs 2024
e1, m1 = float(by[2009]["age_5_17"]), float(by[2009]["age_5_17_moe"])
e2, m2 = float(by[2024]["age_5_17"]), float(by[2024]["age_5_17_moe"])
se = math.sqrt(m1**2 + m2**2) / 1.645
z = (e2 - e1) / se
print(f"5-17 change 2009->2024: {e2-e1:+.0f}, z={z:.2f} (90% CI of diff: +/-{1.645*se:.0f})")
e1, m1 = float(by[2009]["age_0_4"]), float(by[2009]["age_0_4_moe"])
e2, m2 = float(by[2024]["age_0_4"]), float(by[2024]["age_0_4_moe"])
se = math.sqrt(m1**2 + m2**2) / 1.645
print(f"0-4 change 2009->2024: {e2-e1:+.0f}, z={(e2-e1)/se:.2f} (90% CI +/-{1.645*se:.0f})")

# peak/trough of sliding series
s517 = [(int(r["end_year"]), int(r["age_5_17"])) for r in rows]
pk = max(s517, key=lambda x: x[1])
tr = min(s517, key=lambda x: x[1])
print("5-17 sliding peak:", pk, "trough:", tr)
s04 = [(int(r["end_year"]), int(r["age_0_4"])) for r in rows]
print("0-4 sliding peak:", max(s04, key=lambda x: x[1]), "trough:", min(s04, key=lambda x: x[1]))

# per-tract change: 2009 vs 2024 and 2019 vs 2024 (5-17), top movers by absolute weighted change
RAWP = f"{OUT}/raw/parsed"
def w517(y, g):
    d = json.load(open(f"{RAWP}/{y}.json")).get(g)
    if not d:
        return None
    return sum(d[f"{b}_{s}"][0] for b in ["5-9", "10-14", "15-17"] for s in ["m", "f"])

def wpct(y, g):
    src = "/tmp/aaps_geo/aaps_tracts_2010vintage.csv" if y <= 2019 else "/tmp/aaps_geo/aaps_tracts.csv"
    for r in csv.DictReader(open(src)):
        if r["GEOID"] == g and float(r["pct_in"]) >= 5:
            return float(r["pct_in"]) / 100, r.get("NAMELSAD10") or r.get("NAMELSAD", "")
    return None, None

chg = []
for g in sorted(json.load(open(f"{RAWP}/2024.json"))):
    a, b = w517(2009, g), w517(2024, g)
    w1, nm = wpct(2009, g)
    w2, _ = wpct(2024, g)
    if a is None or b is None or w1 is None or w2 is None:
        continue
    chg.append((g, nm, round(a * w1), round(b * w2), round(b * w2 - a * w1), round(100 * (b * w2 - a * w1) / (a * w1)) if a * w1 > 50 else None))
chg.sort(key=lambda x: -abs(x[4]))
print("\nTop movers 5-17 (weighted), 2009 -> 2024:")
for c in chg[:20]:
    print(" ", c)
