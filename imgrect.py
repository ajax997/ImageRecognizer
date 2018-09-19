import json
import urllib.request
from tkinter import *
from tkinter.filedialog import askopenfilename

import cv2
# create the canvas, size in pixels
import numpy as np
from scipy.misc import imresize

filename = askopenfilename(initialdir="/", title="Select file",
                           filetypes=(("jpeg files", "*.jpg"), ("png file", "*.png")))

image = cv2.imread(filename)

img_h, img_w, three = image.shape

canvas = Canvas(width=img_w, height=img_h, bg='white')

# pack the canvas into a frame/form
canvas.pack(expand=YES, fill=BOTH)

img = PhotoImage(file=filename)

canvas.create_image(0, 0, image=img, anchor=NW)


def click2(event):
    print(image[event.y, event.x])


canvas.bind("<Button-1>", click2)

image = cv2.imread(filename)
print(type(image))

sizeof = 3


def sentAPI(data):
    body = {'data': data}

    myurl = "http://127.0.0.1:5000/request"
    req = urllib.request.Request(myurl)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')  # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    response = urllib.request.urlopen(req, jsondataasbytes)
    return str(response.read())


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
    newImg = imresize(newImg, [20, 20], )
    imgFull = np.full((28, 28, 3), [255, 255, 255], dtype=int)
    imgFull[5:25, 5:25] = newImg

    imgFull = (255 - imgFull)

    newImg = imgFull
    # plt.imshow(newImg)
    # plt.show()

    for i in range(0, 28):
        for j in range(0, 28):
            if newImg[i, j][0] == 0 and newImg[i, j][1] == 0 and newImg[i, j][2] == 0:
                img2Predict.append(0)
            else:
                img2Predict.append(int(np.mean(newImg[i, j])) + 100)
    return img2Predict


def chklrud(x1, y1, x2, y2):
    for i in range(x1, x2):
        # canvas.create_line(y2, i, y2 + 1, i + 1, fill='red')
        if not equal(image[i, y2], [255, 255, 255]):
            return 1
        # else:
        #     image[i, y2] = [100, 50, 100]
    for i in range(y1, y2):
        # canvas.create_line(x2, i, x2+1, i+1, fill='red')
        if not equal(image[x2, i], [255, 255, 255]):
            return 2

    for i in range(x1, x2):
        # canvas.create_line(i, y1, i + 1, y1 + 1, fill='red')
        if not equal(image[i, y1], [255, 255, 255]):
            return 3
        # else:
        #     image[i, y1] = [78, 78, 78]

    for i in range(y1, y2):
        # canvas.create_line(x1, i, x1+1, i+1, fill='red')
        if not equal(image[x1, i], [255, 255, 255]):
            return 4
    return 0


def trace(x1, y1, x2, y2):
    canvas.create_line(y1, x1, y2, x2, fill='blue')
    traced = chklrud(x1, y1, x2, y2)
    while traced != 0:
        if traced == 1:
            y2 += 2
        if traced == 2:
            x2 += 2
        if traced == 3:
            y1 -= 2
        if traced == 4:
            x1 -= 2

        if x1 <= 0 or x2 >= img_h - 1 or y2 >= img_w or y1 <= 0:
            break
        else:
            traced = chklrud(x1, y1, x2, y2)

    canvas.create_rectangle(y1, x1, y2, x2)
    crop_img = image[x1:x2, y1:y2]
    toPredict = image_pre_processing(crop_img)

    num = sentAPI(toPredict)
    #
    # print(toPredict)

    canvas.create_text(y1, x1, fill="darkblue", font="Times 20 italic bold",
                       text=str(num[2]))

    # reset area that already crop

    for i in range(x1, x2):
        for j in range(y1, y2):
            image[i, j] = [255, 255, 255]


# check 2 pixel

def equal(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]


x, y = 3, 3


def check_inside(x, y):
    for i in range(x - sizeof, x + sizeof):
        for j in range(y - sizeof, y + sizeof):
            try:
                if equal(image[i, j], [0, 0, 0]):
                    return [True, i, j]
            except:
                pass
    return [False, 0, 0]


# canvas.create_rectangle(x-sizeof, y+sizeof, x+sizeof, y-sizeof)
while True:
    res = check_inside(x, y)
    if res[0]:
        # print(res[1], res[2])
        canvas.create_rectangle(res[2] - sizeof, res[1] - sizeof, res[2] + sizeof, res[1] + sizeof)
        canvas.create_line(res[1], res[2], res[1] + 1, res[2] + 1, fill='red')
        trace(res[1] - sizeof, res[2] - sizeof, res[1] + sizeof, res[2] + sizeof)

    if x + sizeof >= img_h and y + sizeof >= img_w:
        break
    elif y + sizeof > img_w:
        y = 0
        x = x + 2 * sizeof
    else:
        y += 1

mainloop()
