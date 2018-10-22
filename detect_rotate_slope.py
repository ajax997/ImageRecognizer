import operator
import cv2
import numpy as np
from scipy.misc import imresize


def cross_line(x1, y1, x2, y2, W):
    points = []
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    for i in range(0, W):
        points.append([i, int(slope * i + intercept)])
    return points


def draw_line(img, slope, step):
    print(slope)

    W, H = img.shape[:2]
    cross_l = cross_line(0, 0, W, H, H)
    print(cross_l)
    for x, y in cross_l:
        m = np.math.tan(np.deg2rad(slope))
        n = x - (m * y)
        for j in range(0, H, step):
            try:
                img[int(m * j + n), j] = 0
            except:
                pass


def main():
    img = cv2.imread('images/ww.png', 0)
    img = 255 - cv2.Canny(img, 50, 150, apertureSize=5, L2gradient=True)
    W, H = img.shape[:2]
    img = imresize(img, 400 / max(W, H))
    W, H = img.shape[:2]
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
                    # print("Wrong")
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
    print(slopes)
    print(type(rotate_slope))
    # draw_line(img, rotate_slope[0], 3)
    print(rotate_slope[0])
    cv2.imshow("ff", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
