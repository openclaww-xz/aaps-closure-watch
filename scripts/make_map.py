# -*- coding: utf-8 -*-
"""Choropleth of 5-17 population change by tract, AAPS boundary, 2005-09 -> 2020-24."""
import geopandas as gpd
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
import matplotlib.patheffects as pe

# change data (same logic as report)
ts = pd.read_csv('/tmp/aaps-research/population/aaps_tract_age_timeseries.csv', dtype={'GEOID': str})
bands = ['5-9', '10-14', '15-17']
w09 = ts[(ts.year_window == '2005-2009') & (ts.age_band.isin(bands))].groupby('GEOID')['weighted_estimate'].sum()
w24 = ts[(ts.year_window == '2020-2024') & (ts.age_band.isin(bands))].groupby('GEOID')['weighted_estimate'].sum()
chg = pd.DataFrame({'e09': w09, 'e24': w24}).fillna(0)
chg['delta'] = chg['e24'] - chg['e09']

# tract polygons (2020 vintage — matches 2020-24 windows; historical vintages differ slightly)
tracts = gpd.read_file('/tmp/aaps_geo/tracts/tl_2024_26_tract.shp')
was = tracts[tracts.COUNTYFP == '161'].copy()
aaps = gpd.read_file('/tmp/aaps_geo/aaps_boundary.geojson')

was = was.merge(chg, left_on='GEOID', right_index=True, how='left')
# only keep tracts with data (the AAPS set)
m = was[was['delta'].notna()].to_crs(26917)
aaps_p = aaps.to_crs(26917)

# diverging palette: red = loss, blue = gain (colorblind-safe RdBu)
cmap = plt.get_cmap('RdBu')
vmax = m['delta'].abs().max()
norm = TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax)

fig, ax = plt.subplots(figsize=(11, 9))
m.plot(column='delta', cmap=cmap, norm=norm, ax=ax, edgecolor='white', linewidth=0.6, legend=False)
aaps_p.boundary.plot(ax=ax, color='#333333', linewidth=1.8)

# label notable tracts (|delta| >= 100 or |pct| large)
notable = m[(m['delta'].abs() >= 100) | ((m['e09'] >= 100) & ((m['delta'] / m['e09'].replace(0, 1)).abs() >= 0.4))]
for _, r in notable.iterrows():
    c = r.geometry.centroid
    sign = '+' if r['delta'] > 0 else ''
    ax.annotate(f"{r['TRACTCE'][-4:]}\n{sign}{int(r['delta'])}",
                (c.x, c.y), ha='center', va='center', fontsize=7.5, fontweight='bold', color='#111111',
                path_effects=[pe.withStroke(linewidth=2.5, foreground='white')])

# colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
cbar = fig.colorbar(sm, ax=ax, shrink=0.7, pad=0.01)
cbar.set_label('Change in age 5-17 population, 2005-09 to 2020-24 ACS windows', fontsize=9)

ax.set_title('AAPS Census Tracts — School-Age Population Change (2009 → 2024)', fontsize=14, fontweight='bold')
ax.set_axis_off()
plt.tight_layout()
plt.savefig('/tmp/aaps-report/tract_map.png', dpi=200, bbox_inches='tight', facecolor='white')
print('saved', len(m), 'tracts;', len(notable), 'labeled')
