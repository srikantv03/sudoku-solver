const temp = [[
    '','','',''
],[
    '','','',''
],[
    '','','',''
],[
    '','','',''
]]
Vue.component('entry-box', {
    data: function() {
        return {
            set: temp
        };
    },
    template: `<div id="puzzle"><div v-for="array in set"><div class="entry-box" v-for="element in array"><input type="number" min="1" max="${temp.length}" class="entry-box-input" :value="element" /></div></div></div>`
});

new Vue({
    el: '#app',
    data: {
        title: 'Sudoku'
    },
    methods: {
        solve: async function () {
            var sendPuzzle = [];
            var rows = document.getElementById('puzzle').children;
            for (var i = 0; i < rows.length; i++) {
              var row = rows[i].firstChild;
              var cells = rows[i].children;
              sendPuzzle.push([])
              for(var j = 0; j < cells.length; j++) {
                  var cell = cells[j];
                  var entry = cell.firstChild;
                if(entry.value != '') {
                    sendPuzzle[i].push(entry.value);
                } else {
                    sendPuzzle[i].push(0)
                }
              }
              var puzzleStringArr = []
          for(row of sendPuzzle) {
              puzzleStringArr.push(`[${row}]`);
          }
          var puzzleString = `[${puzzleStringArr}]`;
            }

          
        }
      }
})