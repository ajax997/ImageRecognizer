import cv2


def equal(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]


def tract(img, sx, sy):
    print(img[sx, sy])
    max_x, min_x, max_y, min_y = sx, sx, sy, sy

    x_las, y_las = sx, sy

    while equal(img[x_las, y_las], img[sx, sy]):


        if equal(img[x_las + 1, y_las], img[sx, sy]):
            x_las += 1
            continue
        if equal(img[x_las - 1, y_las], img[sx, sy]):
            x_las -= 1
            continue
        if equal(img[x_las, y_las + 1], img[sx, sy]):
            y_las += 1
            continue
        if equal(img[x_las, y_las - 1], img[sx, sy]):
            y_las -= 1
            continue
        if equal(img[x_las + 1, y_las + 1], img[sx, sy]):
            x_las += 1
            y_las += 1
            continue
        if equal(img[x_las - 1, y_las - 1], img[sx, sy]):
            x_las -= 1
            y_las -= 1
            continue

        if x_las == sx and y_las == sy:
            break

    cv2.imshow("image", image)
    cv2.waitKey(0)


image = cv2.imread("drawisland.png")
c, r, k = image.shape

print(c, r, k)

for i in range(c):
    for j in range(r):
        if image[i, j][0] == 0 or image[i, j][1] == 0 or image[i, j][2] == 0:
            # image[i, j] = [0, 0, 255]
            tract(image, i, j)

# cv2.imshow("image", image)
# cv2.waitKey(0)
