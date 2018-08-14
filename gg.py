import cv2

from keras.datasets import mnist
import matplotlib.pyplot as plt
from keras.models import load_model

(x_train, y_train), (x_test, y_test) = mnist.load_data()

model = load_model('model.h5')
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print(x_test.shape)

correct = 1

for i in range(1, x_test.shape[0]):
    img = x_test[i]
    test_img = img.reshape(1, 28, 28, 1)
    img_class = model.predict_classes(test_img)
    classname = img_class[0]
    if classname == y_test[i]:
        correct += 1
    if i % 500 == 0:
        print(correct / i)
        # plt.imshow(img)
        # plt.show()
        print(img)
