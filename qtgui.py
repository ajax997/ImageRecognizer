import tkinter as tk
from PIL import Image, ImageDraw
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

from predict import Predict

class ImageGenerator:
    def __init__(self, parent, posx, posy, *kwargs):

        self.predict = Predict()
        self.parent = parent
        self.posx = posx
        self.posy = posy
        self.sizex = 400
        self.sizey = 400
        self.b1 = "up"
        self.xold = None
        self.yold = None
        self.coords = []
        self.drawing_area = tk.Canvas(self.parent, width=self.sizex, bg='black', height=self.sizey)
        self.drawing_area.place(x=self.posx, y=self.posy)
        self.drawing_area.bind("<Motion>", self.motion)
        self.drawing_area.bind("<ButtonPress-1>", self.b1down)
        self.drawing_area.bind("<ButtonRelease-1>", self.b1up)
        self.button = tk.Button(self.parent, text="Done!", width=10, bg='white', command=self.save)
        self.button.place(x=self.sizex / 7, y=self.sizey + 20)
        self.button1 = tk.Button(self.parent, text="Clear!", width=10, bg='white', command=self.clear)
        self.button1.place(x=(self.sizex / 7) + 80, y=self.sizey + 20)

        self.img2Predict = []
        self.image = Image.new("RGB", (400, 400), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def save(self):

        print("Image Saved")
        filename = "temp.jpg"
        self.image.save(filename)
        self.image.close()
        self.image = Image.new("RGB", (400, 400), (255, 255, 255))
        imagex = cv2.imread("temp.jpg")
        resized = cv2.resize(imagex, (28, 28))
        plt.imshow(resized)
        plt.show()

        r, c, k = resized.shape
        for i in range(0, r):
            for j in range(0, c):
                if resized[i, j][0] == 255 and resized[i, j][1] == 255 and resized[i, j][2] == 255:
                    self.img2Predict.append(0)
                else:
                    self.img2Predict.append(1)
        self.predict.predict(self.img2Predict)

    def clear(self):
        self.drawing_area.delete("all")
        self.coords = []
        self.img2Predict = []
        os.remove("temp.jpg")
        self.image = Image.new("RGB", (400, 400), (255, 255, 255))
        self.draw = ImageDraw.Draw(self.image)

    def b1down(self, event):
        self.b1 = "down"

    def b1up(self, event):
        self.b1 = "up"

        self.xold = None
        self.yold = None
        self.draw.line(self.coords, (0, 0, 0), width=20)
        self.coords = []

    def motion(self, event):
        if self.b1 == "down":
            if self.xold is not None and self.yold is not None:
                event.widget.create_line(self.xold, self.yold, event.x, event.y, smooth='true', width=15, fill='blue')
                self.coords.append((self.xold, self.yold))
        self.xold = event.x


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_geometry("%dx%d+%d+%d" % (600, 600, 10, 10))
    root.config(bg='white')
    ImageGenerator(root, 10, 10)
    root.mainloop()
