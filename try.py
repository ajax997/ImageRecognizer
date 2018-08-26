import numpy as np
import cv2

img = np.zeros((512, 512, 3), np.uint8)
r, g, b = 0, 0, 0


def change():
    global r,g,b
    img[:] = [int(b), int(g), int(r)]
    cv2.imshow(wn, img)
    print([int(b), int(g), int(r)])


def bf(ff):
    global r, g, b
    b = ff
    change()


def rf(ff):
    global r, g, b
    r = ff
    change()


def gf(ff):
    global r, g, b
    g = ff
    change()


wn = 'Palete'
cv2.namedWindow(wn)
cv2.createTrackbar('B', wn, 0, 255, bf)
cv2.createTrackbar('G', wn, 0, 255, gf)
cv2.createTrackbar('R', wn, 0, 255, rf)

cv2.imshow(wn, img)
cv2.waitKey(0)
cv2.destroyAllWindows()
