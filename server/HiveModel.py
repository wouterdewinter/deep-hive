import os
from os.path import join
import random
import numpy as np
import keras
from keras.layers import GlobalMaxPooling2D, GlobalAveragePooling2D, Dense, Dropout
from keras.optimizers import SGD
from keras.preprocessing import image
from keras.applications.vgg16 import VGG16 as Backbone
from keras.applications.vgg16 import preprocess_input

class HiveModel:
    """Wrapper around keras model that provides convenience methods"""

    def __init__(self, img_size = 128, path='data/catsdogs'):
        self._img_size = img_size
        self._model = None
        self._classes = []
        self._path = path
        self._test_id = 0

        self.load_data()

    def init_model(self):
        """Compile and build the model"""

        base_model = Backbone(
            weights='imagenet',
            include_top=False,
            input_shape = (self._img_size, self._img_size, 3)
        )


        base_model.trainable = False

        self._model = keras.models.Sequential([
            base_model,
            GlobalAveragePooling2D(),
            Dense(256, activation='relu'),
            Dropout(0.3),
            Dense(len(self._classes), activation='softmax')
        ])

        sgd = SGD(lr=0.0005)

        self._model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        self._model.summary()

    def load_data(self):
        """Load data and create np arrays for training and testing"""

        print("Loading images ...")

        self._classes = next(os.walk(self._path))[1]
        samples = []
        for label, class_name in enumerate(self._classes):
            files = next(os.walk(join(self._path, class_name)))[2]
            for file in files:
                filename = join(self._path, class_name, file)
                try:
                    img = image.load_img(filename)
                    img_arr = image.img_to_array(img)
                    samples.append((img_arr, label))
                except:
                    print("Error loading image")
                    pass

        # shuffle all samples
        random.seed(4)  # deterministic
        random.shuffle(samples)
        images, labels = zip(*samples)

        # make numpy arrays
        images = np.array(images)
        labels = np.array(labels)

        # check shapes
        print(images.shape, labels.shape)

        # split test / train set
        split = 40

        self._test_images = images[:split]
        self._test_labels = labels[:split]
        self._train_images = images[split:]
        self._train_labels = labels[split:]

        # perform preprocessing for vgg16 (process copy because preprocess_input changes array)
        self._train_x = preprocess_input(np.copy(self._train_images))
        self._test_x = preprocess_input(np.copy(self._test_images))

        # one hot encoding of labels
        self._train_y = keras.utils.to_categorical(self._train_labels, num_classes=len(self._classes))
        self._test_y = keras.utils.to_categorical(self._test_labels, num_classes=len(self._classes))

        print("Loaded %d images" % images.shape[0])

    def label(self, image_id, class_id):
        """Label an image with a class id"""

        image_id = int(image_id)
        class_id = int(class_id)
        x = np.expand_dims(self._train_x[image_id], axis=0)
        y = keras.utils.to_categorical(np.expand_dims(np.array(class_id), axis=0), num_classes=len(self._classes))
        print("Training image %d with label %d" % (image_id, class_id))
        self.train(x, y)

    def evaluate(self, test_id):
        """evaluate accuracy of a single test image"""

        x = np.expand_dims(self._test_x[test_id], axis=0)
        y = np.expand_dims(self._test_y[test_id], axis=0)
        y_hat = self._model.predict(x, verbose=0)
        label = np.argmax(y_hat, axis=1)[0]

        accuracy = 1 if label == self._test_labels[test_id] else 0

        print(y, y_hat, accuracy, label)

        print("Evaluating id %d, score is %d, label is %d" % (self._test_id, accuracy, label))

        return accuracy, label

    def train(self, x, y):
        """Fit model on a dataset"""

        self._model.fit(x=x, y=y, batch_size=1, epochs=1, verbose=0)