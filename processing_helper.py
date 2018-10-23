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


def tracePx(erosion, x, y, W, H):
    visited = np.full((W, H), fill_value=255, dtype=np.uint8)
    ls = [[x, y]]
    while len(ls) != 0:
        cx, cy = ls.pop()
        erosion[cx, cy] = 255

        if cx + 1 < W and cx - 1 >= 0 and cy - 1 >= 0 and cy + 1 < H:
            if erosion[cx + 1, cy + 1] != 255:
                visited[cx + 1, cy + 1] = erosion[cx + 1, cy + 1]
                ls.append([cx + 1, cy + 1])
            if erosion[cx + 1, cy - 1] != 255:
                visited[cx + 1, cy - 1] = erosion[cx + 1, cy - 1]
                ls.append([cx + 1, cy - 1])
            if erosion[cx - 1, cy + 1] != 255:
                visited[cx - 1, cy + 1] = erosion[cx - 1, cy + 1]
                ls.append([cx - 1, cy + 1])
            if erosion[cx - 1, cy - 1] != 255:
                visited[cx - 1, cy - 1] = erosion[cx - 1, cy - 1]
                ls.append([cx - 1, cy - 1])
            if erosion[cx, cy + 1] != 255:
                visited[cx, cy + 1] = erosion[cx, cy + 1]
                ls.append([cx, cy + 1])
            if erosion[cx, cy - 1] != 255:
                visited[cx, cy - 1] = erosion[cx, cy - 1]
                ls.append([cx, cy - 1])
            if erosion[cx + 1, cy] != 255:
                visited[cx + 1, cy] = erosion[cx + 1, cy]
                ls.append([cx + 1, cy])
            if erosion[cx - 1, cy] != 255:
                visited[cx - 1, cy] = erosion[cx - 1, cy]
                ls.append([cx - 1, cy])
    return visited, erosion


def image_elements_wise(image, original, W, H):
    res_img = np.full((W, H), fill_value=255, dtype=np.uint8)
    for i in range(0, W):
        for j in range(0, H):
            if image[i, j] != 255 and original[i, j] != 255:
                res_img[i, j] = original[i, j]
    return res_img


def produce_size(image, W, H):
    max_X = 0
    min_X = np.math.inf
    max_Y = 0
    min_Y = np.math.inf

    for i in range(0, W):
        for j in range(0, H):
            if image[i, j] != 255:
                if i > max_X:
                    max_X = i
                if i < min_X:
                    min_X = i
                if j > max_Y:
                    max_Y = j
                if j < min_Y:
                    min_Y = j

    new_image = image[min_X:max_X, min_Y:max_Y]
    if len(new_image) == 0:
        return [None, max_X - min_X, max_Y - min_Y]
    return [new_image, max_X - min_X, max_Y - min_Y]


def cross_line(x1, y1, x2, y2, W):
    points = []
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1
    for i in range(0, W):
        points.append([i, int(slope * i + intercept)])
    return points


def img_scaler(img, p_W):
    W, H = img.shape[:2]
    new_img = np.full((int(W + W * p_W), H), fill_value=255)
    new_img[int((W * p_W) / 2): int((W * p_W) / 2 + W), :] = img
    return new_img
