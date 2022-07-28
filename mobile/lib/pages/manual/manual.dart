import 'package:flutter/material.dart';
import '../../../utils/rangeenforcer.dart';

class ManualPage extends StatefulWidget {
  const ManualPage({Key? key}) : super(key: key);

  @override
  State<ManualPage> createState() => _ManualPageState();
}

class _ManualPageState extends State<ManualPage> {
  List<List<int>> board = [
    for (var row = 0; row < 9; row += 1)
      [for (var column = 0; column < 9; column += 1)
        0],
  ];

  void replaceBoard(List<List<int>> newBoard) {
    board = newBoard;
  }

  void editBoard(int i, int j, int newVal) {
    if (newVal > 0 && newVal < 10) {
      board[i][j] = newVal;
    }
    print(board);
  }

  List<Widget> renderBoard() {
    List<Widget> returnBoard = [];
    for (int i = 0; i < 9; i++) {
      for (int j = 0; j < 9; j++) {
        var color = Colors.blue[200];
        if (((i < 3 || i > 5) && (j < 6 && j > 2)) || ((j < 3 || j > 5) && (i < 6 && i > 2))) {
          color = Colors.grey[200];
        }
        returnBoard.add(
            TextField(
              keyboardType: TextInputType.number,
              textAlign: TextAlign.center,
              style: TextStyle(fontSize: 20),
              decoration: InputDecoration(
                fillColor: color,
                filled: true,
                contentPadding: EdgeInsets.zero,
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(10.0),
                  borderSide:  BorderSide(color: Colors.white)
                )
              ),
              inputFormatters: [RangeEnforcer(1, 9)],
            )
        );
      }
    }
    return returnBoard;
  }



  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Manual Sudoku Entry'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            GridView.count(
              scrollDirection: Axis.vertical,
              shrinkWrap: true,
              primary: false,
              padding: const EdgeInsets.all(20),
              crossAxisCount: 9,
              children: renderBoard()
            )
          ],
        ),
      ), // This trailing comma makes auto-formatting nicer for build methods.
    );
  }
}
