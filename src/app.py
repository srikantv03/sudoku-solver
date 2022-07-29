import numpy as np
from flask import Flask, request
from flask_api import status
import cv2
import base64
import json
from src.main import SudokuBoard

app = Flask(__name__)

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

@app.route('/solve', methods=['GET'])
def solve():
   args = request.args
   if "puzzle" in args:
      puzzle = json.loads(args.get("puzzle"), None, True)
      sudoku_board = SudokuBoard(puzzle)
      return sudoku_board

   return {"error": "Puzzle not found"}, status.HTTP_400_BAD_REQUEST





# class SudokuHandler(RequestHandler):
#    def get(self):
#       self.set_header("Access-Control-Allow-Origin", "*")
#      puzzle = list(json.loads(self.get_argument("puzzle", None, True)))
#       solved = [list(map(int, arr)) for arr in solve(puzzle)]
#       self.write({'solved': solved})
#
#
# class ScannerHandler(RequestHandler):
#    def post(self):
#       self.set_header("Access-Control-Allow-Origin", "*")
#       image = readb64(self.get_body_argument("image"))
#       scanned = getImageSudoku(image, debug=False)
#       print(scanned)
#       self.write({'scanned': str(scanned)})
#
#
# def make_app():
#    urls = [('/solve', SudokuHandler), ('/scan', ScannerHandler)]
#    return Application(urls)
#
#
# if __name__ == '__main__':
#    app = make_app()
#    app.listen(3000)
#    IOLoop.instance().start()
