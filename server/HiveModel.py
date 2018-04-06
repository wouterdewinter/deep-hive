import os, keras
from keras.layers import GlobalMaxPooling2D, GlobalAveragePooling2D, Dense, Dropout
from os.path import join
from keras.preprocessing import image
import random
from keras.applications.resnet50 import preprocess_input
import numpy as np

class HiveModel:

    def __init__(self, img_size = 128):
        self._img_size = img_size
        self._model = None
        self._classes = []

        self.init_model()
        self.load_data()

    def init_model(self):

        base_model = keras.applications.VGG16(
            include_top=False,
            weights='imagenet',
            input_shape=(self._img_size, self._img_size, 3)
        )

        base_model.trainable = False

        self._model = keras.models.Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(2, activation='softmax')
        ])

        self._model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
        self._model.summary()

    def load_data(self):
        print("Loading images")

        path = '../data/128x128'
        self._classes = next(os.walk(path))[1]
        samples = []
        for label, class_name in enumerate(self._classes):
            files = next(os.walk(join(path, class_name)))[2]
            for file in files:
                filename = join(path, class_name, file)
                try:
                    img = image.load_img(filename)
                    img_arr = image.img_to_array(img)
                    samples.append((img_arr, label))
                except:
                    print("Error loading image")
                    pass

        # shuffle all samples
        random.shuffle(samples)
        images, labels = zip(*samples)

        # make numpy arrays
        images = np.array(images)
        labels = np.array(labels)

        # check shapes
        print(images.shape, labels.shape)

        # split test / train set
        split = 100
        train_size = 200

        self._test_images = images[:split]
        self._test_labels = labels[:split]
        self._train_images = images[split:split + train_size]
        self._train_labels = labels[split:split + train_size]

        # perform preprocessing for vgg16
        self._train_x = preprocess_input(self._train_images)
        self._test_x = preprocess_input(self._test_images)

        # one hot encoding of labels
        self._train_y = keras.utils.to_categorical(self._train_labels, num_classes=len(self._classes))
        self._test_y = keras.utils.to_categorical(self._test_labels, num_classes=len(self._classes))

        print("Loaded %d images" % images.shape[0])

    def label(self, image_id, class_id):
        x = np.expand_dims(self._train_x[image_id], axis=0)
        y = keras.utils.to_categorical(np.expand_dims(np.array(class_id), axis=0), num_classes=len(self._classes))

        print(x.shape, y.shape, y)


        self.train(x, y)

    def train(self, x, y):
        self._model.fit(x=x, y=y, batch_size=1, epochs=1, verbose=2)