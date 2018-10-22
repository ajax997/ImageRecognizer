import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imresize
from scipy.stats import stats
from sklearn.cluster import KMeans

img = cv2.imread('images/newrotation.png', 0)
ori = img
img = 255 - cv2.Canny(img, 50, 150, apertureSize=5, L2gradient=True)
W, H = img.shape[:2]
img = imresize(img, 600 / max(W, H))
kernel = np.ones((15, 15), np.uint8)
erosion = cv2.erode(img, kernel, iterations=1)
erosion = imresize(erosion, 600 / max(W, H))
img = imresize(img, 600 / max(W, H))
# erosion = 255 - cv2.Canny(erosion, 50, 150, apertureSize=5, L2gradient=True)
cv2.imshow('', erosion)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
_W, _H = erosion.shape[:2]


def detect_centroid(x1):
    x2 = np.zeros((len(x1)))
    X = np.array(list(zip(x1, x2))).reshape(len(x1), 2)
    K = 2
    kmeans_model = KMeans(n_clusters=K).fit(X)
    centers = np.array(kmeans_model.cluster_centers_)
    print(centers)
    _min = np.math.inf
    xcc = 0
    for _x, _y in centers:
        cc = 0

        for xx in x1:
            cc += (np.math.fabs(_x - xx) ** 2)
        if cc < _min:
            _min = cc
            xcc = _x
    return xcc


def mode_point(_ls):
    return max(set(_ls.tolist()), key=_ls.tolist().count)


def tracePx(x, y):
    visited = []
    ls = [[x, y]]
    while len(ls) != 0:
        cx, cy = ls.pop()
        erosion[cx, cy] = 255

        if cx + 1 < _W and cx - 1 > 0 and cy - 1 > 0 and cy + 1 < _H:
            if erosion[cx + 1, cy + 1] != 255:
                visited.append([cx + 1, cy + 1])
                ls.append([cx + 1, cy + 1])
            if erosion[cx + 1, cy - 1] != 255:
                visited.append([cx + 1, cy - 1])
                ls.append([cx + 1, cy - 1])
            if erosion[cx - 1, cy + 1] != 255:
                visited.append([cx - 1, cy + 1])
                ls.append([cx - 1, cy + 1])
            if erosion[cx - 1, cy - 1] != 255:
                visited.append([cx - 1, cy - 1])
                ls.append([cx - 1, cy - 1])
            if erosion[cx, cy + 1] != 255:
                visited.append([cx, cy + 1])
                ls.append([cx, cy + 1])
            if erosion[cx, cy - 1] != 255:
                visited.append([cx, cy - 1])
                ls.append([cx, cy - 1])
            if erosion[cx + 1, cy] != 255:
                visited.append([cx + 1, cy])
                ls.append([cx + 1, cy])
            if erosion[cx - 1, cy] != 255:
                visited.append([cx - 1, cy])
                ls.append([cx - 1, cy])
    return visited


angles = []
count = 0
br = False
for i in range(0, _W):
    if br:
        break
    for j in range(0, _H):
        if erosion[i, j] != 255:
            ls = np.array(tracePx(i, j))
            if len(ls) != 0:
                count += 1
                max_X = max(ls[:, 0])
                min_X = min(ls[:, 0])
                max_Y = max(ls[:, 1])
                min_Y = min(ls[:, 1])
                cv2.line(img, (min_Y, min_X), (max_Y, min_X), color=0)
                cv2.line(img, (min_Y, min_X), (min_Y, max_X), color=0)
                cv2.line(img, (min_Y, max_X), (max_Y, max_X), color=0)
                cv2.line(img, (max_Y, max_X), (max_Y, min_X), color=0)
                # newImg = np.full((max_X - min_X, max_Y - min_Y), 255)
                newImg = np.full((_W, _H), 255, dtype=np.uint8)
                for x, y in ls:
                    newImg[x, y] = 0
                slope, intercept, r_value, p_value, std_err = stats.linregress(ls[:, 0], ls[:, 1])
                angle = (np.math.atan(slope)) * (180 / np.math.pi)
                print(angle)
                angles.append(angle)
                M = cv2.getRotationMatrix2D(((max_X - min_X) / 2, (max_Y - min_Y) / 2), angle, 1)
                dst = cv2.warpAffine(newImg, M, (W, H), borderValue=255)
                plt.imshow(dst)
                plt.show()

nW, nH = ori.shape[:2]
# m = (detect_centroid(np.array(angles)))
m = mode_point(np.array(angles, dtype=np.uint8))

print(m)
M = cv2.getRotationMatrix2D((nW / 2, nH / 2), m+90, 1)
dst = cv2.warpAffine(ori, M, (H, H), borderValue=255)
cv2.imshow("s", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(count)
cv2.imshow('', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)