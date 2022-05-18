import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt

def detect(image):
    if countBlanks(image < 0.1):
        return 0
    else:
        return 1


def countBlanks(image):
    grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
    # print(len(blackAndWhiteImage))
    # print(sum(blackAndWhiteImage))


