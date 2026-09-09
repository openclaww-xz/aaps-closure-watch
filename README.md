# AAPS Closure Watch

Tracking the Ann Arbor Public Schools (AAPS) fiscal crisis and school-closure outlook with open census data.

## What this is

A reproducible research pipeline analyzing:

1. **Fiscal structure** — Proposal A's sealed capital/operating ledgers, the 2019 $1B bond, the 2024 budget shock ($14M pension misposting; ~$12M unfunded raises), and the structural deficit.
2. **Demographics** — 15-year tract-level age-structure time series (ACS 5-year, 2005-09 through 2020-24) for the 63 census tracts intersecting the AAPS boundary, built from key-free Census bulk files.
3. **Closure outlook** — geographic divergence in school-age population (inner-ring loss vs southern growth) as the leading indicator of closure risk; no official list exists yet.

## Key findings (2026-09-09)

- School-age (5-17) population inside AAPS: **19,840 → 18,249 (-8.0%)** over 15 years; future entrants (0-4): **-12.7%**, at a 15-year low with no recovery inflection.
- Total district population **grew +6.8%** — the district is aging in place, not shrinking.
- Losses concentrate in inner-ring tracts (one lost half its school-age population); gains in southern new-development tracts.

## Repo layout

```
data/       tract-level time series, school list, district boundary (GeoJSON)
report/     R Markdown report (render with rmarkdown::render)
scripts/    Python pipeline (extract → aggregate → analyze; choropleth map)
sources/    research notes: official/state/social-media/local-news/methodology
analysis/   narrative analysis of the population data
```

## Reproduce

```bash
# Python deps (uv)
uv venv && uv pip install shapely geopandas pyproj pandas matplotlib

# Population pipeline (key-free; downloads ACS bulk files from www2.census.gov)
python scripts/extract.py && python scripts/aggregate.py && python scripts/analyze.py

# Choropleth map
python scripts/make_map.py

# Report (R + rmarkdown + TinyTeX)
cd report && Rscript -e 'rmarkdown::render("report.Rmd")'
```

## Method notes

- ACS 5-year windows overlap; trend claims use non-overlapping anchors (2005-09, 2010-14, 2015-19, 2020-24).
- Tract vintages: 2010 vintage for windows ending 2009-2019, 2020 vintage for 2020-2024 (break <0.2% of total population).
- Cross-boundary tracts (~15% of district population) area-weighted.
- MOE via Census Handbook independent-sum approximation.

## Sources

All sources inventoried in `sources/`. Data: U.S. Census Bureau (ACS 5-year summary files, TIGER/Line 2024). Research notes compiled September 9, 2026 from ~130 sources across district, state, social-media, and local-news tracks.

## License

MIT
