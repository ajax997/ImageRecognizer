import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

img = cv2.imread("images/ro.png")
W, H = img.shape[:2]
M = cv2.getRotationMatrix2D((W/2, H/2), 50,1)

newIMG = cv2.warpAffine(img, M, (W, H), borderValue=(255,255,255))


cv2.imwrite("images//newrotation.png", newIMG)