import cv2
import numpy as np

from scipy.misc import imresize


def isblackPx(c1):
    return c1 != 255


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


image = cv2.imread('images/excel.png')
image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)

original = image

edges = cv2.Canny(image, 50, 150, apertureSize=5, L2gradient=True)
image = 255 - edges
# cv2.imshow('w', image)
# lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
#
# if lines is not None:
#     for i in range(len(lines)):
#         for rho, theta in lines[i]:
#             a = np.cos(theta)
#             b = np.sin(theta)
#             x0 = a * rho
#             y0 = b * rho
#
#             pts1 = (int(x0 + 100 * -b), int(y0 + 1000 * a))
#             pts2 = (int(x0 - 100 * -b), int(y0 - 1000 * a))
#             cv2.line(image, pts1, pts2, (0, 255, 0), 2)


ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite("dd_gray.png", image)
W, H = image.shape[:2]
image = imresize(image, 800 / max(W, H))
original = imresize(original, 800 / max(W, H))
W, H = image.shape[:2]
print(W, H)
wnName = "Image"
cv2.namedWindow(wnName)

startLine = True
previousLine = 0


def box_content(box):
    count = 0
    r, c = box.shape[0:2]
    for _i in range(0, r):
        for j in range(0, c):

            if box[_i, j] != 255:
                count += 1
    return count / (r * c) > 0.5


def boxer(_previousLine, currentLine, _H, _image):
    startVertical = True
    previousVertical = 0
    for _i in range(0, _H):
        verticalLine = _image[_previousLine:currentLine, _i:_i + 1]
        cilV = checkInline2(verticalLine, currentLine - _previousLine)
        if cilV and startVertical:
            previousVertical = _i
            startVertical = False
        if not cilV and not startVertical:
            startVertical = True
            if box_content(_image[previousLine:currentLine, previousVertical: _i]):
                cv2.rectangle(_image, (previousVertical, _previousLine), (_i, currentLine), (30, 255, 50))
                previousVertical = _i


for i in range(0, W):
    line = image[i, :]
    cilR = checkInline(line, H, 0.08)
    if cilR and startLine:
        previousLine = i
        startLine = False

    if not cilR and not startLine:
        startLine = True
        if i - previousLine > 5:
            boxer(previousLine, i, H, image)
        previousLine = i

cv2.imshow(wnName, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
