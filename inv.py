import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("digits.png")
img = np.invert(img)
plt.imshow(img)
plt.show()

cv2.imwrite('digit.png',img)