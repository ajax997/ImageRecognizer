from tkinter import *
import cv2

# create the canvas, size in pixels
import numpy as np

canvas = Canvas(width=800, height=400, bg='white')

# pack the canvas into a frame/form
canvas.pack(expand=YES, fill=BOTH)

# load the .gif image file
img = PhotoImage(file='drawisland.png')

# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(0, 0, image=img, anchor=NW)


def click2(event):
    print(image[event.y, event.x])


canvas.bind("<Button-1>", click2)

image = cv2.imread("drawisland.png")

print(image.shape)

sizeof = 10
x, y = 10, 10


def chklrud(x1, y1, x2, y2):
    for i in range(x1, x2):
        canvas.create_line(y2, i, y2 + 1, i + 1, fill='red')
        if equal(image[i, y2], [0, 0, 0]):
            return 1
        else:
            image[i, y2] = [1000, 50, 100]
    for i in range(y1, y2):
        # canvas.create_line(x2, i, x2+1, i+1, fill='red')
        if equal(image[x2, i], [0, 0, 0]):
            return 2

    for i in range(x1, x2):
        # canvas.create_line(i, y1, i + 1, y1 + 1, fill='red')
        if equal(image[i, y1], [0, 0, 0]):
            return 3
        else:
            image[i, y1] = [78, 78, 78]

    for i in range(y1, y2):
        # canvas.create_line(x1, i, x1+1, i+1, fill='red')
        if equal(image[x1, i], [0, 0, 0]):
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

        if x1 <= 0 or x2 >= 399 or y2 >= 799 or y1 <= 0:
            break
        else:
            traced = chklrud(x1, y1, x2, y2)

    canvas.create_rectangle(y1, x1, y2, x2)
    for i in range(x1, x2):
        for j in range(y1, y2):
            image[i, j] = [255, 255, 255]
    # cv2.imshow('image', image)
    # cv2.waitKey(0)


def equal(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]


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
        print(res[1], res[2])
        canvas.create_rectangle(res[2] - sizeof, res[1] - sizeof, res[2] + sizeof, res[1] + sizeof)
        canvas.create_line(res[1], res[2], res[1] + 1, res[2] + 1, fill='red')
        trace(res[1] - sizeof, res[2] - sizeof, res[1] + sizeof, res[2] + sizeof)

    if x + sizeof >= 399 and y + sizeof >= 799:
        break
    elif y + sizeof > 799:
        y = 0
        x = x + 2 * sizeof
    else:
        y += 1

# run it ...

mainloop()
