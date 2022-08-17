# Some of the following code was sourced on the internet to help me create this project
# A full list of the resources I used for this project will be available on the README.md of this repository

import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
from transform import *
from classifier import *
import tensorflow as tf

def getImageSudoku(image, debug=True):
    # image = cv2.imread(imgPath)
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    orig_img = image

    selected_coords = np.array(separateBoard(image, debug=debug), dtype="float32")
    transformed_image = four_point_transform(orig_img, selected_coords)
    if debug:
        cv2.imshow("Transformed Image", transformed_image)
        cv2.waitKey()

    return getCells(transformed_image)



def contourSeparation(edged, check_for_edges = False):
    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    # cv2.imshow('title', edged)
    # cv2.waitKey()
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]
    location = None

    # Finds rectangular contour
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 15, True)
        print(len(approx))
        if len(approx) == 4 and (not check_for_edges or checkNotBorder(approx)):
            location = approx
            break

    # Show all the contours if the debug option is shown
    selectedCoords = []
    if isinstance(location, (np.ndarray, np.generic) ):
        for coords in location:
            selectedCoords.append((coords[0][0], coords[0][1]))

    return np.array(selectedCoords)

def relu(value):
    if value < 0:
        return 0
    return value


def checkNotBorder(location):
    for coord in location:
        if coord[0][0] < 5 or coord[0][1] < 5:
            return False

    return True

def separateBoard(img, debug=False):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bfilter = cv2.bilateralFilter(gray, 13, 20, 20)
    edged = cv2.Canny(bfilter, 30, 180)

    return contourSeparation(edged, check_for_edges=True)

def warpCell(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)

    return four_point_transform(image, contourSeparation(blackAndWhiteImage, check_for_edges=False))

def getCells(image):
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
            if not isinstance(cell, (np.ndarray, np.generic)):
                sudoku[i].append(0)
                continue
            sudoku[i].append(detect(cell))
    return sudoku


getImageSudoku()