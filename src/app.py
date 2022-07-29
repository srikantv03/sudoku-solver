import numpy as np
from flask import Flask, request
import cv2
import base64
import src.main

app = Flask(__name__)

def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
   return img

@app.route('/solve', methods=['GET'])
def search():
   args = request.args
   console.log(args)

# class SudokuHandler(RequestHandler):
#    def get(self):
#       self.set_header("Access-Control-Allow-Origin", "*")
#       puzzle = list(json.loads(self.get_argument("puzzle", None, True)))
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
