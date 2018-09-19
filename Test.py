import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)

if cap.isOpened():
    ret, previousFrame = cap.read()
else:
    ret = False

while ret:
    print(cap.get(3))
    ret, frame = cap.read()
    d = cv2.absdiff(frame, previousFrame)
    gray = cv2.cvtColor(d, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    blur = cv2.flip(blur, flipCode=1)
    ret, th = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(th, np.zeros((3, 3), np.uint8), iterations=10)
    img, c, h = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(blur, c, -1, (0, 0, 255), 3)

    cv2.imshow('frame', blur)
    if cv2.waitKey(1) == 32:
        break
    previousFrame = frame
cv2.destroyAllWindows()
cap.release()
