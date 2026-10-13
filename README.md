# Big Smoke, Back Paddock

Where Australia's ARIA Award winners come from. A data visualisation story for **FIT3179 Data Visualisation 2** (Monash University, Clayton), by **Lee Wei Han**, 12 October 2026.

Live page: <https://hamburgerisgood.github.io/FIT3179A2/>

## What's here

| Path | What it is |
|---|---|
| `index.html` | The single scrolling web page |
| `css/style.css` | Layout and typography |
| `js/main.js` | Loads each chart spec with vega-embed |
| `specs/` | **One JSON file per chart** (Vega-Lite `.vl.json`, Vega `.vg.json`), plus `_theme.json` shared styling |
| `data/aria_wins.csv` | 116 wins joined with each winner's hometown, state and ABS remoteness class |
| `data/state_points.csv` | Label point and tile-grid position per state (layout helper) |
| `data/waffle.csv` | Each state's 100-square share of people and of wins |
| `data/au_states.topo.json` | Simplified state boundaries (13 KB) |
| `data/source/` | The source tables exactly as collected |
| `build_data.py` | Joins the source tables into the files above (no values are changed) |

## Charts (12, including 4 maps)

1. Proportional symbol map – hometowns sized by wins (radio filter by award)
2. Choropleth map – wins per million residents (dropdown filter)
3. Dorling cartogram – states as circles sized by wins, coloured by fair-share ratio
4. Tile-grid map of small multiples – wins per decade per state
5. Paired waffle charts – share of people vs share of wins
6. Marimekko (mosaic) chart – state × award
7. Beeswarm – every win by year and remoteness
8. Aligned bar charts – remoteness of population vs winners
9. Bump chart – running rank of the ten biggest winners (hover)
10. Matrix chart – every winner by year and award (legend click)
11. Treemap – artists grouped by state
12. Ridgeline plot – smoothed timeline of wins per state

## Data sources

1. Wikipedia: winner lists for ARIA Album of the Year, Best Group and Best Country Album; artist infobox origin / birthplace. Retrieved 12 Oct 2026.
2. ABS, *National, state and territory population*, March 2026.
3. AIHW, *Rural and remote health* (ABS population share by Remoteness Area, June 2023).
4. github.com/matthewproctor/australianpostcodes (coordinates, ABS Remoteness Area 2021).
5. github.com/rowanhogan/australian-states (boundaries), simplified with mapshaper.

## Run locally

The page loads JSON and CSV files, so open it through a local server, not by double-clicking:

```
python3 -m http.server 8000
```

then visit http://localhost:8000 (or use VS Code's Live Server).

## Publish on GitHub Pages

1. Create a public repository and push these files to the `main` branch.
2. Settings → Pages → Source: *Deploy from a branch*, Branch: `main`, folder `/ (root)`.
3. The page appears at <https://hamburgerisgood.github.io/FIT3179A2/> within a minute or two.

## Licence

Text and charts: CC BY-SA 4.0. Data remains under the licences of its sources.
