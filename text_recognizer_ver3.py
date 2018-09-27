import cv2
import numpy as np
import os
import operator

from scipy.misc import imresize


def isblackPx(c1):
    return c1 != 255
    # return c1[0] + c1[1] + c1[2] < 200


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


def checkInline(_line, _H, epsilon):
    blPercentage = 0
    for j in range(0, len(_line) - 1):
        if isblackPx(_line[j]):
            blPercentage += 1
    return blPercentage / _H > epsilon


def checkInline2(_line, _H, epsilon):
    blPercentage = 0
    for j in range(1, len(_line) - 1):
        if isblackPx(_line[j][0]):
            blPercentage += 1
    return blPercentage / _H > epsilon


# files = os.listdir('images')
# for file in files:
#     print(file)

image = cv2.imread('images/easy.png')
# image = cv2.imread('images/blur_text.png')
# image = cv2.imread('images/background.png')
# image = cv2.imread('images/chinese.png')
# image = cv2.imread('images/excel.png')
# image = cv2.imread('images/MultiColors.png')
# image = cv2.imread('images/italic3.png')
# image = cv2.imread('images/coloredText.png')
# image = cv2.imread('images/italic2.png')
original = image
W, H = image.shape[:2]

image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('threshold1', image)

print((detect_background(image)))
print(max(detect_background(image).items(), key=operator.itemgetter(1))[0])
if max(detect_background(image).items(), key=operator.itemgetter(1))[0] == 0:
    image = 255 - image

cv2.imshow('threshold2', image)
W, H = image.shape[:2]
print(W, H)
wnName = "Image"
cv2.namedWindow(wnName)

startLine = True
previousLine = 0


def boxer(_previousLine, currentLine, _H, _image, _original):
    startVertical = True
    previousVertical = 0
    for _i in range(0, _H):
        verticalLine = _image[_previousLine:currentLine, _i:_i + 1]
        cilV = checkInline2(verticalLine, currentLine - _previousLine, 0.01)
        if cilV and startVertical:
            previousVertical = _i
            cv2.line(original, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = False
        if not cilV and not startVertical:
            cv2.line(_original, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = True
            cv2.rectangle(original, (previousVertical, _previousLine), (_i, currentLine), (30, 255, 50))
            previousVertical = _i


for i in range(0, W):
    line = image[i, :]
    cilR = checkInline(line, H, 0.01)
    # if not cilR:
    #     cv2.line(original, (0, i), (H, i), (0, 255, 0), 1)

    if cilR and startLine:
        # cv2.line(original, (0, i), (H, i), (0, 255, 0), 1)
        previousLine = i
        startLine = False

    if not cilR and not startLine:
        # cv2.line(original, (0, i), (H, i), (100, 255, 50), 1)
        startLine = True
        if i - previousLine > 5:
            boxer(previousLine, i, H, image, original)
        previousLine = i

original = imresize(original, 800 / max(W, H))
cv2.imshow(wnName, original)
cv2.waitKey(0)
cv2.destroyAllWindows()
