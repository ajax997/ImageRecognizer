import cv2
import numpy as np

def detect_background(_image):
    colorList = {
    }
    W, H = _image.shape[:2]
    for _i in range(0, W):
        for _j in range(0, H):
            pixel = _image[_i, _j]
            if pixel in colorList:
                colorList[pixel] = colorList[pixel] + 1
            else:
                colorList[pixel] = 1
    return colorList


image = cv2.imread('images/preprocessed.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
print(max(detect_background(image)))