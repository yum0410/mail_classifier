// https://jp.vuejs.org/v2/examples/todomvc.html
new Vue({
    el: '#select_table',
    data: {
        items: [
            {"word": "hoge", "count": 5},
            {"word": "huga", "count": 3}
        ]
    },
    methods: {
        doSearch: function(event) {
          // ES
          var query = {
            "query": {
              "bool": { 
                "should": [
                  {"match": { "author": this.form.author } },
                  {"match": { "title": this.form.title } }
                ]
              }
            }
          }
          axios.post('http://localhost:9200/aozora/_search', query).then((res) => {
            var hit_book = res.data.hits.hits;
            var score = hit_book.map(i => i._score);
            this.results = hit_book.map(i => i._source);
            for ( let i =0; i < this.results.length; i++) {
              this.results[i].score = score[i]
            }
          });
        },
    }
})