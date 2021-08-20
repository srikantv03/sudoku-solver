//temp array with empty values to generate entry boxes
//dynamic temp to allow for 4x4, 16x16, etc.

var temp = [];
for (var i = 0; i < 9; i++) {
    temp.push([]);
    for (var j = 0; j < 9; j++) {
        temp[i].push('')
    }
}

Vue.component('entry-box', {
    data: function () {
        return {
            set: temp
        };
    },
    template: `<div id="puzzle"><div v-for="(array, index) in set">
    <div class="entry-box" v-for="(element, index) in array"><input type="number" min="1" max="${temp.length}" class="entry-box-input" :value="element" /></div>
    </div></div>`
});

const vm = new Vue({
    el: '#app',
    data: {
        title: 'SUDOKU SOLVER',
        footer: 'Made by Srikant Vasudevan'
    },
    methods: {
        solve: async function () {
            var sendPuzzle = [];
            var rows = document.getElementById('puzzle').children;
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i].firstChild;
                var cells = rows[i].children;
                sendPuzzle.push([])
                for (var j = 0; j < cells.length; j++) {
                    var cell = cells[j];
                    var entry = cell.firstChild;
                    if (entry.value != '') {
                        sendPuzzle[i].push(entry.value);
                    } else {
                        sendPuzzle[i].push(0)
                    }
                }

            }

            var puzzleStringArr = []
            for (row of sendPuzzle) {
                puzzleStringArr.push(`[${row}]`);
                var puzzleString = `[${puzzleStringArr}]`;
            }

            var apiResponse = await fetch(`http://localhost:3000/solve?puzzle=${puzzleString}`);
            var solution = await apiResponse.json();

            for (var i = 0; i < rows.length; i++) {
                var row = rows[i].firstChild;
                var cells = rows[i].children;
                sendPuzzle.push([])
                for (var j = 0; j < cells.length; j++) {
                    var cell = cells[j];
                    var entry = cell.firstChild;
                    entry.value = solution.solved[i][j]
                }
            }
        },
        createGrids: function() {
            var rows = document.getElementById('puzzle').children;
            var nums = parseInt(Math.sqrt(temp.length))
            for (var i = 0; i < rows.length; i++) {
                var row = rows[i].firstChild;
                var cells = rows[i].children;
                for (var j = 0; j < cells.length; j++) {
                    var cell = cells[j];
                    if((j + 1) % nums == 0) {
                        cell.firstChild.classList.add('right-border');
                    } else if(j == 0) {
                        cell.firstChild.classList.add('left-border');
                    }

                    if((i) % nums == 0) {
                        cell.firstChild.classList.add('top-border');

                    } else if(i == temp.length - 1) {
                        cell.firstChild.classList.add('bottom-border');
                    }
                }

            }
        }
    }
})

vm.createGrids();