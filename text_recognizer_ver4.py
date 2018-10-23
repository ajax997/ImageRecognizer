import operator
import cv2
import numpy as np
from scipy.misc import imresize
import matplotlib.pyplot as plt

from detect_rotate_slope import cross_line
from processing_helper import detect_background, tracePx, image_elements_wise, produce_size, img_scaler


def cv2_image_show(window, img):
    cv2.imshow(window, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def plt_image_show(image):
    plt.imshow(image)
    plt.show()


def read_input(f_name, w=0):
    img = cv2.imread(f_name)
    W, H = img.shape[:2]
    if w == 0:
        return [img, W, H]
    elif w != 0:
        img = imresize(img, w / max(W, H))
        return [img] + list(img.shape[:2])


def pre_processing(image, W, H):
    # image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2_image_show("", image)

    if max(detect_background(image).items(), key=operator.itemgetter(1))[0] == 0:
        image = 255 - image

    return image


def erosion(image, W, H):
    kernel = np.ones((10, 10), np.uint8)
    _erosion = cv2.erode(image, kernel, iterations=1)
    _erosion[0, :] = 255
    _erosion[W - 1, :] = 255
    _erosion[:, 0] = 255
    _erosion[:, H - 1] = 255
    return _erosion


def detect_block(erosioned, original, W, H):
    blocks = []
    for i in range(0, W):
        for j in range(0, H):
            if erosioned[i, j] != 255:
                print(erosioned[i, j], i, " ", j)

                block, erosioned = (tracePx(erosioned, i, j, W, H))
                plt_image_show(erosioned)
                wised = image_elements_wise(block, original, W, H)
                # quest = cv2.rectangle(wised, (j - 10, i - 10), (j + 10, i + 10), color=0)
                # debug
                # plt_image_show(quest)
                try:
                    produced_image = produce_size(wised, W, H)[0]
                    if produced_image is not None:
                        blocks.append(produced_image)
                except:
                    pass
    return blocks


def detect_rotate_angle(img):
    W, H = img.shape[:2]
    # img = 255 - cv2.Canny(img, 50, 150, apertureSize=5, L2gradient=True)
    img = img_scaler(img, 0.2)
    plt_image_show(img)
    slopes = {}
    for i in range(0, 180):
        big_count = 0
        cross_l = cross_line(0, 0, W, H, W)
        for x, y in cross_l:
            m = np.math.tan(np.deg2rad(i))
            n = x - (m * y)
            _count = 0
            count = 0
            for j in range(0, H):
                _count += 1
                try:
                    if img[j, int(m * j + n)] != 255:
                        count += 1
                except:
                    pass

            for j in range(0, W):
                try:
                    if img[int((j - n) / m), j] != 255:
                        count += 1
                except:
                    pass
            if count == 0:
                big_count += 1
        slopes[i] = big_count

    rotate_slope = max(slopes.items(), key=operator.itemgetter(1))
    return rotate_slope[0] if rotate_slope[0] != 0 else 90


def main():
    f_name = "images/polistic.png"
    image, W, H = read_input(f_name, w=500)
    image = pre_processing(image, W, H)
    original = image
    erosioned = erosion(image, W, H)
    cv2_image_show("", erosioned)
    blocks = detect_block(erosioned, original, W, H)
    angles = []
    for block in blocks:
        angle = (detect_rotate_angle(block))
        angles.append([angle, block.shape[0] * block.shape[1]])

    rotate = 0
    max_size = 0
    for an, size in angles:
        if size > max_size:
            rotate = an
            max_size = size

    print(rotate)

    M = cv2.getRotationMatrix2D((H / 2, W / 2), -(rotate - 90), 1)
    rotated_image = cv2.warpAffine(original, M, (H, W), borderValue=255)
    cv2_image_show("Final", rotated_image)


if __name__ == '__main__':
    main()
