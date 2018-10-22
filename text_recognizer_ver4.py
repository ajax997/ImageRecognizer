import operator
import cv2
import numpy as np
from scipy.misc import imresize
import matplotlib.pyplot as plt

from processing_helper import detect_background, tracePx, image_elements_wise, produce_size


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


def pre_processing(image):
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    print((detect_background(image)))
    print(max(detect_background(image).items(), key=operator.itemgetter(1))[0])
    if max(detect_background(image).items(), key=operator.itemgetter(1))[0] == 0:
        image = 255 - image
    return image


def erosion(image):
    kernel = np.ones((10, 10), np.uint8)
    _erosion = cv2.erode(image, kernel, iterations=1)
    return _erosion


def detect_block(erosioned, original,  W, H):
    for i in range(0, W):
        for j in range(0, H):
            if erosioned[i, j] != 255:
                block, erosioned = np.array(tracePx(erosioned, i, j, W, H))
                wised = image_elements_wise(block, original, W, H)
                produced_image = produce_size(wised)[0]



def detect_rotate_angle():
    pass


def main():
    f_name = "images/polistic.png"
    image, W, H = read_input(f_name, w=500)
    image = pre_processing(image)
    original = image
    erosioned = erosion(image)
    cv2_image_show("", erosioned)
    detect_block(erosioned,original, W, H)


if __name__ == '__main__':
    main()
