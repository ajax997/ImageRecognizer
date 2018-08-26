import cv2
import numpy as np


def isblackPx(c1):
    return c1[0] != 255 and c1[1] != 255 and c1[2] != 255
    # return c1[0] + c1[1] + c1[2] < 200


def checkInline(_line, _H, epsilon):
    blPercentage = 1
    for j in range(0, len(_line) - 1):
        if isblackPx(_line[j]):
            blPercentage += 1
    return blPercentage / _H > epsilon


def checkInline2(_line, _H):
    for j in range(1, len(_line) - 1):
        if isblackPx(_line[j][0]):
            return True
    return False


image = cv2.imread('images/ff.png')

wnName = "Image"
cv2.namedWindow(wnName)

W, H = image.shape[:2]
startLine = True
previousLine = 0


def boxer(_previousLine, currentLine, _H, _image):
    startVertical = True
    previousVertical = 0
    for _i in range(0, _H):
        verticalLine = _image[_previousLine:currentLine, _i:_i + 1]
        cilV = checkInline2(verticalLine, currentLine - _previousLine)
        if cilV and startVertical:
            previousVertical = _i
            # cv2.line(image, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = False
        if not cilV and not startVertical:
            # cv2.line(image, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = True
            cv2.rectangle(_image, (previousVertical, _previousLine), (_i, currentLine), (30, 255, 50))
            previousVertical = _i


for i in range(0, W):
    line = image[i, :]
    cilR = checkInline(line, H, 0.01)
    if cilR and startLine:
        # cv2.line(image, (0, i), (H, i), (0, 255, 0), 1)
        previousLine = i
        startLine = False

    if not cilR and not startLine:
        # cv2.line(image, (0, i), (H, i), (100, 255, 50), 1)
        startLine = True
        if i - previousLine > 5:
            boxer(previousLine, i, H, image)
        previousLine = i

cv2.imshow(wnName, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
