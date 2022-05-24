import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt

def detect(image):
    if (np.sum(image) == 0):
        return 0




