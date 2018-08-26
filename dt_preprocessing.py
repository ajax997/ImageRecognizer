from tkinter import *
from tkinter.filedialog import askopenfilenames
import numpy as np

import cv2

# create the canvas, size in pixels
from ImageCropper import ImageCropper

filenames = askopenfilenames(initialdir="/", title="Select file",
                             filetypes=(("jpeg files", "*.jpg"), ("png file", "*.png")))


for i in range(0, len(filenames)):
    chopper = ImageCropper(cv2.imread(filenames[i]))
    res = np.array(chopper.crop())
    res.astype('float32')
    print(res)
