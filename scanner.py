# Some of the following code was sourced on the internet to help me create this project
# A full list of the resources I used for this project will be available on the README.md of this repository

import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from transform import *
from classifier import *
from main import *
import tensorflow as tf


digit_prediction = tf.keras.models.load_model('model/final_model')
digit_prediction.summary()
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def relu(value):
    if value < 0:
        return 0
    return value

def getImageSudoku(imgPath, debug=True):
    image = cv2.imread(imgPath)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    ret_img = cv2.drawContours(image, contours, -1, (0, 255, 0), 3)

    orig_img = cv2.imread(imgPath)

    selectedCoords = np.array(separateBoard(image, debug=debug), dtype="float32")
    warped = four_point_transform(orig_img, selectedCoords)
    plt.imshow(warped)
    plt.show()
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
    plt.imshow(edged)
    plt.show()
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
        # if debug:
        #     # plt.imshow(img)
        #     # plt.plot(coords[0][0], coords[0][1], "or", markersize=10)
        #     # plt.show()

    return selectedCoords

def warpCell(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    keypoints = cv2.findContours(blackAndWhiteImage.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)

    newimg = cv2.drawContours(image.copy(), contours, -1, (0, 255, 0), 3)
    cv2.imshow("Contour", newimg)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = []

    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        if len(approx) == 4:
            location = approx
            break

    if len(location) == 0:
        return image
    selectedCoords = []
    for coords in location:
        selectedCoords.append((coords[0][0], coords[0][1]))
    selectedCoords = np.array(selectedCoords, dtype="float32")
    warped = four_point_transform(image, selectedCoords)
    return warped

def getCells(image):
    # Get the cells and perform a tesseract scrape with the cells
    # TODO: replace the tesseract scrape with a trained CNN

    w = image.shape[1]
    h = image.shape[0]
    cw = w/9
    ch = h/9
    sudoku = []
    for i in range(9):
        sudoku.append(list())
        for j in range(9):
            (y1, y2) = (int(j * ch - ch/4), int((j + 1) * ch + ch/4))
            (x1, x2) = (int(i * cw - ch/4), int((i + 1) * cw + cw/4))
            cell = warpCell(image[relu(y1):y2, relu(x1):x2])
            nh = cell.shape[0]
            nw = cell.shape[1]
            cell = cell[int(nh/20):int(19 * nh/20), int(nw/20): int(19 * nw/20)]
            gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
            gray[np.where(gray >= 150)] = 255
            gray[np.where(gray < 150)] = 0
            gray = cv2.resize(gray, (28, 28))
            gray[np.where(gray >= 200)] = 255
            gray[np.where(gray < 200)] = 0
            gray = cv2.bitwise_not(gray)

            if (np.sum(gray) == 0):
                sudoku[i].append(0)
                continue

            sudoku[i].append(np.argmax(digit_prediction.predict(tf.reshape(gray, [-1, 28, 28, 1]))))
    print(solve(sudoku))
getImageSudoku('sudoku_sample4.png', debug=True)
