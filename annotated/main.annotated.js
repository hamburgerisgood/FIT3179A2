// 【带注释的副本】网站实际用的是 js/main.js，这份只是方便你看懂，改这里不会影响网站。
// 作用：把 12 张图依次嵌入到 index.html 里对应的 <div> 中。

// 图表清单：[页面里的 div 选择器, 图的 JSON 文件路径]，每张图一行
const CHARTS = [
  ["#c01", "specs/01_symbol_map.vl.json"],        // 图 1：比例符号地图，放进 <div id="c01">
  ["#c02", "specs/02_choropleth.vl.json"],        // 图 2：分级着色地图
  ["#c03", "specs/03_dorling_cartogram.vg.json"], // 图 3：Dorling 变形图（.vg = Vega，不是 Vega-Lite）
  ["#c04", "specs/04_tile_grid_map.vl.json"],     // 图 4：瓦片网格地图
  ["#c05", "specs/05_waffle.vl.json"],            // 图 5：华夫图
  ["#c06", "specs/06_mosaic.vl.json"],            // 图 6：马赛克图 (Marimekko)
  ["#c07", "specs/07_beeswarm.vg.json"],          // 图 7：蜂群图（Vega）
  ["#c08", "specs/08_remoteness_bars.vl.json"],   // 图 8：三联柱状图
  ["#c09", "specs/09_bump_chart.vl.json"],        // 图 9：名次变化图
  ["#c10", "specs/10_winner_matrix.vl.json"],     // 图 10：热力图
  ["#c11", "specs/11_treemap.vg.json"],           // 图 11：矩形树图（Vega）
  ["#c12", "specs/12_ridgeline.vl.json"]          // 图 12：山脊图
];

// async 函数：里面可以用 await 等待“加载文件”这类要花时间的事
async function start() {
  let theme = {};                                   // 主题默认空对象；加载失败时图表就用 Vega 默认样式
  try {
    // fetch 读取主题文件，.json() 把文本变成对象；两个 await 依次等待下载和解析
    theme = await (await fetch("specs/_theme.json")).json();
  } catch (e) {
    // 加载失败不让整个网站挂掉，只在控制台提醒
    console.warn("Theme not loaded; charts use Vega defaults.", e);
  }
  // 等网页字体加载完再画图，否则文字宽度会按错的字体测量，标签位置会偏
  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (e) { /* 出错也继续，不影响画图 */ }
  }
  // 遍历清单：每次取出 [选择器, 文件路径]（解构赋值）
  for (const [el, spec] of CHARTS) {
    const target = document.querySelector(el);      // 在页面里找到那个 div
    if (!target) continue;                          // 页面里没有这个 div 就跳过这张图
    // vegaEmbed(容器, 图的JSON, 选项)：真正画图的一行
    //   config: theme    → 把主题当作全局默认样式
    //   actions: false   → 不显示右上角“导出/查看源码”菜单
    //   renderer: "svg"  → 用 SVG 渲染（清晰、可缩放、文字可选中）
    vegaEmbed(el, spec, { config: theme, actions: false, renderer: "svg" })
      .then(() => {                                 // 画好之后执行
        // 给 SVG 加 viewBox，让它能按列宽等比缩小，而不是出现横向滚动条
        const svg = target.querySelector("svg");
        if (svg && !svg.getAttribute("viewBox")) {
          svg.setAttribute("viewBox", "0 0 " + svg.getAttribute("width") + " " + svg.getAttribute("height"));
        }
      })
      .catch(err => {                               // 画图失败（比如 JSON 写错）
        // 在页面上显示提示，而不是留一块空白
        target.innerHTML = '<p class="chart-error">This chart could not load (' + spec + '). ' +
          'If you opened the file directly, run it from a local web server instead.</p>';
        console.error(spec, err);                   // 详细错误打印到浏览器控制台
      });
  }
}

start();                                            // 页面脚本加载后立刻开始
