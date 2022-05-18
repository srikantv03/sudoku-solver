# Some of the following code was sourced on the internet to help me create this project
# A full list of the resources I used for this project will be available on the README.md of this repository

import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from transform import *

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def getImageSudoku(imgPath, debug=True):
    image = cv2.imread(imgPath)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ret_img = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    orig_img = cv2.imread(imgPath)

    selectedCoords = np.array(separateBoard(image, debug=debug), dtype="float32")
    warped = four_point_transform(orig_img, selectedCoords)
    getCells(warped)
    cv2.imshow("Warped Image", warped)
    cv2.waitKey()




def checkNotBorder(location):
    for coord in location:
        if coord[0][0] < 5 or coord[0][1] < 5:
            return False

    return True


def separateBoard(img, debug=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)

    newimg = cv2.drawContours(img.copy(), contours, -1, (0, 255, 0), 3)
    cv2.imshow("Contour", newimg)

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None

    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4 and checkNotBorder(approx):
            location = approx
            break

    # Show all the contours if the debug option is shown
    selectedCoords = []
    for coords in location:
        selectedCoords.append((coords[0][0], coords[0][1]))
        if debug:
            plt.imshow(img)
            plt.plot(coords[0][0], coords[0][1], "or", markersize=10)
            plt.show()

    return selectedCoords

def getCells(image):
    # Get the cells and perform a tesseract scrape with the cells
    # TODO: replace the tesseract scrape with a trained CNN

    w = image.shape[1]
    h = image.shape[0]
    cw = w/9
    ch = h/9
    print(cw)
    print(ch//1)

    for i in range(9):
        for j in range(9):
            (y1, y2) = (int((j * ch)//1), int(((j + 1) * ch)))
            (x1, x2) = (int(i * cw), int((i + 1) * cw))
            wb = int(cw//5)
            hb = int(ch//5)
            cell = image[y1+hb:y2-hb, x1+wb:x2-wb]
            print(pytesseract.image_to_string(cell, config='--psm 11 --oem 1 -c tessedit_char_whitelist=0123456789'))

            # plt.imshow(cell)
            # plt.show()
getImageSudoku('sudoku_sample2.jpg', debug=True)
