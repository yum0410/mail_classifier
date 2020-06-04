var DATA_FILE_PATH = './js/word_data.json'; // 読み込みデータファイル
var TARGET_ELEMENT_ID = '#cloud'; // 描画先


d3.json(DATA_FILE_PATH).then(function(data) { // v5

  var h = 490;
  var w = 600;

  var random = d3.randomIrwinHall(2);
  var countMax = d3.max(data, function(d){ return d.count} );
  var sizeScale = d3.scaleLinear().domain([0, countMax]).range([10, 100])

  var words = data.map(function(d) {
    return {
    text: d.word,
    size: sizeScale(d.count) //頻出カウントを文字サイズに反映
    };
  });

  d3.layout.cloud().size([w, h])
    .words(words)
    .font("Impact")
    .rotate(function() { return ~~ (Math.random() * 2) * 90; })
    .fontSize(function(d) { return d.size; })
    .on("end", draw) //描画関数の読み込み
    .start();


  // wordcloud 描画
  function draw(words) {
    d3.select(TARGET_ELEMENT_ID)
      .append("svg")
        .attr("class", "ui fluid image") // style using semantic ui
        .attr("viewBox", "0 0 " + w + " " + h )  // ViewBox : x, y, width, height
        .attr("width", "100%")    // 表示サイズの設定
        .attr("height", "100%")   // 表示サイズの設定
      .append("g")
        .attr("transform", "translate(" + w / 2 + "," + h / 2 + ")")
      .selectAll("text")
        .data(words)
      .enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        .style("fill", function(d, i) { return d3.schemeCategory10[i % 10]; })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
      .text(function(d) { return d.text; })
      .on("click", function (d, i){
        app.append_data({"word": d.text, "count": d.size})
      });
  }
});

var app = new Vue({
  el: '#app',
  data: {
      items: [
          {"word": "hoge", "count": 5},
          {"word": "huga", "count": 3}
      ]
  },
  methods: {
    append_data: function(event) {
        var item = {"word": event.word, "count": event.count}
        this.items.push(item)
    }
}
})