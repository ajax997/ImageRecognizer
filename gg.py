import cv2

img = cv2.imread('drawisland.png')
img[100, 200] = [0,255,0]
cv2.imshow('image', img)
cv2.waitKey(0)
