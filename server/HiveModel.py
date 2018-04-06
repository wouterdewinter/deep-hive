import keras
from keras.layers import GlobalMaxPooling2D, GlobalAveragePooling2D, Dense, Dropout

class HiveModel:

    def __init__(self, img_size = 128):
        self._img_size = img_size
        self._model = None

        self.init_model()

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

    def train(self, x, y):
        self._model.fit(x=x, y=y, batch_size=1, epochs=1, verbose=2)