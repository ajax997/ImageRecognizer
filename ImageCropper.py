import numpy as np
from scipy.misc import imresize


class ImageCropper:
    def __init__(self, image):
        self.image = image
        self.img_h, self.img_w, self.three = self.image.shape
        self.x, self.y = 3, 3
        self.sizeof = 3

    @staticmethod
    def equal(c1, c2):
        return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]

    @staticmethod
    def image_pre_processing(img):
        img2Predict = []
        _img_h, _img_w, _three = img.shape
        sq = max(_img_h, _img_w)
        sq_min = min(_img_h, _img_w)
        newImg = np.full((sq, sq, 3), [255, 255, 255], dtype=int)
        print(newImg.shape)
        for i in range(0, sq):
            count = 0
            for j in range(0, sq):
                # print(j)
                if sq / 2 - sq_min / 2 < j < sq / 2 + sq_min / 2:
                    try:
                        newImg[i, j] = img[i, count]
                        count += 1
                    except:
                        pass
        newImg = imresize(newImg, [28, 28], 'nearest')

        for i in range(0, 28):
            for j in range(0, 28):
                if newImg[i, j][0] == 255 and newImg[i, j][1] == 255 and newImg[i, j][2] == 255:
                    img2Predict.append(0)
                else:
                    img2Predict.append(int(np.mean(np.invert(newImg[i, j]))))
        return img2Predict

    def chklrud(self, x1, y1, x2, y2):
        for i in range(x1, x2):

            if not self.equals(self.image[i, y2], [255, 255, 255]):
                return 1

        for i in range(y1, y2):

            if not self.equals(self.image[x2, i], [255, 255, 255]):
                return 2

        for i in range(x1, x2):

            if not self.equals(self.image[i, y1], [255, 255, 255]):
                return 3

        for i in range(y1, y2):

            if not self.equals(self.image[x1, i], [255, 255, 255]):
                return 4
        return 0

    def trace(self, x1, y1, x2, y2):

        traced = self.chklrud(x1, y1, x2, y2)
        while traced != 0:
            if traced == 1:
                y2 += 2
            if traced == 2:
                x2 += 2
            if traced == 3:
                y1 -= 2
            if traced == 4:
                x1 -= 2

            if x1 <= 0 or x2 >= self.img_h - 1 or y2 >= self.img_w or y1 <= 0:
                break
            else:
                traced = self.chklrud(x1, y1, x2, y2)

        crop_img = self.image[x1 - 5:x2 + 5, y1 - 5:y2 + 5]

        # reset area that already crop
        pp = self.image_pre_processing(crop_img)
        for i in range(x1, x2):
            for j in range(y1, y2):
                self.image[i, j] = [255, 255, 255]

        return pp

    @staticmethod
    def equals(c1, c2):
        return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]

    def check_inside(self, x, y):
        for i in range(x - self.sizeof, x + self.sizeof):
            for j in range(y - self.sizeof, y + self.sizeof):
                try:
                    if self.equals(self.image[i, j], [0, 0, 0]):
                        return [True, i, j]
                except:
                    pass
        return [False, 0, 0]

    def crop(self):
        arrResult = []
        while True:
            res = self.check_inside(self.x, self.y)
            if res[0]:
                print(res[1], res[2])

                arrImg = self.trace(res[1] - self.sizeof, res[2] - self.sizeof, res[1] + self.sizeof,
                                    res[2] + self.sizeof)
                arrResult.append(np.reshape(arrImg, [28, 28]))

            if self.x + self.sizeof >= self.img_h and self.y + self.sizeof >= self.img_w:
                break
            elif self.y + self.sizeof > self.img_w:
                self.y = 0
                self.x = self.x + 2 * self.sizeof
            else:
                self.y += 1
        return arrResult
