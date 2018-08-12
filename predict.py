from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

from keras.datasets import mnist


# dimensions of our images

class Predict:
    def __init__(self):
        # load the model we saved
        self.model = load_model('model.h5')
        self.model.compile(loss='binary_crossentropy',
                           optimizer='rmsprop',
                           metrics=['accuracy'])

        # # predicting images
        # (x_train, y_train), (x_test, y_test) = mnist.load_data()
        #
        # img = x_test[130]
        # test_img = img.reshape(1, 28, 28, 1)
        # img_class = model.predict_classes(test_img)
        # prediction = img_class[0]
        # classname = img_class[0]
        # print("Class: ", classname)
        # plt.imshow(img)
        # plt.title(classname)
        # plt.show()

    def predict(self, img):
        test_img = np.reshape(img, [1, 28, 28, 1])
        img_class = self.model.predict_classes(test_img)
        classname = img_class[0]
        plt.imshow(np.reshape(img, [28, 28]))
        plt.show()
        print("Class: ", classname)
