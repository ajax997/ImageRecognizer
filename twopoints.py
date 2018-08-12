import math
import tkinter as tk
from PIL import Image, ImageDraw, ImageColor


def width(x, y, x0, y0):
    return math.sqrt((x - x0) ** 2 + (y - y0) ** 2)


class ExampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.previous_x = self.previous_y = 0
        self.x = self.y = 0
        self.points_recorded = []
        self.canvas = tk.Canvas(self, width=400, height=400, bg="black", cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.button_print = tk.Button(self, text="Export", command=self.print_points)
        self.button_print.pack(side="top", fill="both", expand=True)
        self.button_clear = tk.Button(self, text="Clear", command=self.clear_all)
        self.button_clear.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<Motion>", self.tell_me_where_you_are)
        self.canvas.bind("<B1-Motion>", self.draw_from_where_you_are)

    def clear_all(self):
        self.canvas.delete("all")

    def pxaround(self, image, x1, y1):
        for i in range(x1 - 3, x1 + 3):
            for j in range(y1 - 3, y1 + 3):
                if round(width(i, j, x1, y1)) < 3:
                    image.putpixel((x1, y1), ImageColor.getcolor('black', 1))

    def print_points(self):
        image = Image.new("RGB", (400, 400), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        draw.line(self.points_recorded, fill='red')
        while self.points_recorded:
            try:
                self.pxaround(self.points_recorded.pop(), self.points_recorded.pop())
            except:
                pass
        image.save("xx.jpg")

    def tell_me_where_you_are(self, event):
        self.previous_x = event.x
        self.previous_y = event.y

    def draw_from_where_you_are(self, event):
        if self.points_recorded:
            self.points_recorded.pop()
            self.points_recorded.pop()

        self.x = event.x
        self.y = event.y
        self.canvas.create_line(self.previous_x, self.previous_y,
                                self.x, self.y, fill="yellow")
        self.points_recorded.append(self.previous_x)
        self.points_recorded.append(self.previous_y)
        self.points_recorded.append(self.x)
        self.points_recorded.append(self.x)
        self.previous_x = self.x
        self.previous_y = self.y


if __name__ == "__main__":
    app = ExampleApp()
    app.mainloop()
