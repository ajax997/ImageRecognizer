import cv2
import numpy as np
import os
import base64
import matplotlib.pyplot as plt
import operator

from scipy.misc import imresize


def image_pre_processing(img):
    print(img.shape)
    _img_h, _img_w = img.shape[:2]
    sq_max = max(_img_h, _img_w)
    sq_min = min(_img_h, _img_w)
    newImg = np.full((sq_max, sq_max), 255, dtype=int)
    print(newImg.shape)

    padding = (sq_max - sq_min) // 2
    if _img_w < _img_h:

        newImg[:, padding: + sq_min + padding] = img
    else:
        newImg[padding: padding + sq_min, :] = img

    newImg = imresize(newImg, [32, 32])
    return newImg


def boxer(_previousLine, currentLine, _H, _image, _original):
    _original = cv2.cvtColor(_original, cv2.COLOR_BGR2GRAY)
    startVertical = True
    previousVertical = 0
    for _i in range(0, _H):
        verticalLine = _image[_previousLine:currentLine, _i:_i + 1]
        cilV = checkInline2(verticalLine, currentLine - _previousLine, 0.0)
        if cilV and startVertical:
            previousVertical = _i
            # cv2.line(_original, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = False
        if not cilV and not startVertical:
            # cv2.line(_original, (_i, _previousLine), (_i, currentLine), (30, 255, 50), 1)
            startVertical = True
            # cv2.rectangle(_original, (previousVertical, _previousLine), (_i, currentLine), (30, 255, 50))
            img = 255-image_pre_processing(_original[_previousLine: currentLine, previousVertical:_i])
            print(img)
            _str = base64.b64encode(img)
            base64_2_numpy(_str, img.shape)
            previousVertical = _i


def isblackPx(c1):
    return c1 != 255


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


def main():
    image = cv2.imread('images/vn.png')
    original = image
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


def base64_2_numpy(base64_str, shape):
    print(base64_str)
    print(shape)
    img = np.frombuffer(base64.b64decode(base64_str), np.uint8)
    print(img)
    img = np.reshape(img, shape)
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
