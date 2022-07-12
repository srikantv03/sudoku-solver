import pytesseract
import cv2
import numpy as np
import imutils
import matplotlib.pyplot as plt
import tensorflow as tf

digit_prediction = tf.keras.models.load_model('src/model/final_model')
digit_prediction.summary()


def detect(image):
    nh = image.shape[0]
    nw = image.shape[1]
    cell = image[int(nh / 20):int(19 * nh / 20), int(nw / 20): int(19 * nw / 20)]
    gray = cv2.cvtColor(cell, cv2.COLOR_BGR2GRAY)
    gray[np.where(gray >= 150)] = 255
    gray[np.where(gray < 150)] = 0
    gray = cv2.resize(gray, (28, 28))
    gray[np.where(gray >= 200)] = 255
    gray[np.where(gray < 200)] = 0
    gray = cv2.bitwise_not(gray)
    if (np.sum(gray) == 0):
        return 0
    return np.argmax(digit_prediction.predict(tf.reshape(gray, [-1, 28, 28, 1])))



