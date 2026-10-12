// Embeds every chart. Each chart's full Vega / Vega-Lite JSON lives in /specs.
// The shared look (fonts, axis colours) is in specs/_theme.json and is passed as config.
const CHARTS = [
  ["#c01", "specs/01_symbol_map.vl.json"],
  ["#c02", "specs/02_choropleth.vl.json"],
  ["#c03", "specs/03_dorling_cartogram.vg.json"],
  ["#c04", "specs/04_tile_grid_map.vl.json"],
  ["#c05", "specs/05_waffle.vl.json"],
  ["#c06", "specs/06_mosaic.vl.json"],
  ["#c07", "specs/07_beeswarm.vg.json"],
  ["#c08", "specs/08_remoteness_bars.vl.json"],
  ["#c09", "specs/09_bump_chart.vl.json"],
  ["#c10", "specs/10_winner_matrix.vl.json"],
  ["#c11", "specs/11_treemap.vg.json"],
  ["#c12", "specs/12_ridgeline.vl.json"]
];

async function start() {
  let theme = {};
  try {
    theme = await (await fetch("specs/_theme.json")).json();
  } catch (e) {
    console.warn("Theme not loaded; charts use Vega defaults.", e);
  }
  // Wait for the web fonts so text inside the charts is measured with the right face.
  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (e) { /* keep going */ }
  }
  for (const [el, spec] of CHARTS) {
    const target = document.querySelector(el);
    if (!target) continue;
    vegaEmbed(el, spec, { config: theme, actions: false, renderer: "svg" })
      .catch(err => {
        target.innerHTML = '<p class="chart-error">This chart could not load (' + spec + '). ' +
          'If you opened the file directly, run it from a local web server instead.</p>';
        console.error(spec, err);
      });
  }
}

start();
