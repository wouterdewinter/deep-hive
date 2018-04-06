#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import keras
import numpy as np
import random
import os
import PIL
import io
from os.path import join
from HiveModel import HiveModel

IMG_SIZE = 128

path = '../data'
classes = next(os.walk(path))[1]
images = []
labels = []
for label, class_name in enumerate(classes):
    dirs = next(os.walk(join(path, class_name)))[1]
    for dir_name in dirs:
        files = next(os.walk(join(path, class_name, dir_name)))[2][:10]
        for file in files:
            filename = join(path, class_name, dir_name, file)
            try:
                img = image.load_img(filename, target_size=(IMG_SIZE, IMG_SIZE))
                img_arr = image.img_to_array(img)
            except:
                pass

            if not img_arr.shape == (IMG_SIZE, IMG_SIZE, 3):
                print("Unexpected shape")
                continue

            images.append(img_arr)
            labels.append(label)

print("Loaded %d images" % len(images))

# shuffle all samples
samples = list(zip(images,labels))
random.shuffle(samples)
x,y = zip(*samples)

# make numpy arrays
x = np.array(x)
y = np.array(y)

# one hot encoding of labels
y = keras.utils.to_categorical(y)

# perform preprocessing for vgg16
x = preprocess_input(x)

# split test / train set
split = 100
train_size = 200
test_x = x[:split]
test_y = y[:split]
train_x = x[split:split + train_size]
train_y = y[split:split + train_size]

image_id = 0
model = HiveModel()
x = np.expand_dims(train_x[0], axis=0)
y = np.expand_dims(train_y[0], axis=0)
model.train(x, y)

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route("/")
def hello():
    return render_template('realtime.html')

@app.route("/task")
def get_task():
    global image_id

    image_url = 'http://localhost:5000/image/%d' % image_id
    data = {
        'image': image_url,
        'image_id': image_id,
        'labels': classes,
    }

    # loop trough all images in dataset
    #@todo only pick training images!!!

    image_id += 1
    if image_id >= len(images):
        image_id = 0

    return jsonify(data)

@app.route("/label", methods=['POST'])
def post_label():
    global model

    data = request.get_json()
    print (data)

    image_id = data['image_id']
    #@todo use class from request
    x = np.expand_dims(train_x[image_id], axis=0)
    y = np.expand_dims(train_y[image_id], axis=0)
    print(x.shape, y.shape)

    model.train(x,y)

    data['result'] = 'ok'
    return jsonify(data)

@app.route("/image/<int:image_id>")
def get_image(image_id):
    img_data = np.uint8(images[image_id])
    img = PIL.Image.fromarray(img_data)
    bytes = io.BytesIO()
    img.save(bytes, 'PNG')
    print(bytes)
    bytes.seek(0)
    return send_file(bytes, mimetype='image/png')
