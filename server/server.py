#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import numpy as np
import PIL
import io
from HiveModel import HiveModel
from Config import Config
import redis, json

# start with the first image
image_id = 0

# init keras model
model = HiveModel(path='../' + Config.IMAGE_PATH, img_size=Config.IMAGE_SIZE)

# connect to redis
r = redis.StrictRedis(host=Config.REDIS_HOST, port=6379, charset="utf-8", decode_responses=True)

# init flask application
app = Flask(__name__, static_url_path='/static')
CORS(app)

# static route
@app.route("/")
def root():
    return app.send_static_file('index.html')

# static route
@app.route("/bundle.js")
def js():
    return app.send_static_file('bundle.js')

# get a new annotation task
@app.route("/api/task")
def get_task():
    global image_id, model

    image_url = '/api/image/train/%d' % image_id
    data = {
        'image': image_url,
        'image_id': image_id,
        'labels': model._classes,
    }

    # loop trough all images in dataset
    image_id += 1
    if image_id >= len(model._train_images):
        image_id = 0

    return jsonify(data)

# get metrics about model
@app.route("/api/status")
def get_status():
    acc = r.lrange('accuracies', 0, -1) # fetch complete list
    acc = np.array(acc).astype('float')
    mean = np.mean(acc)

    data = {
        'accuracy': mean if not np.isnan(mean) else 0,
        'test_labels': r.lrange('test_labels', 0, -1),
        'test_scores': r.lrange('test_scores', 0, -1),
        'annotation_count': r.get('annotation_count'),
        'labels': model._classes
    }

    return jsonify(data)

# process user annotation
@app.route("/api/label", methods=['POST'])
def post_label():
    global r

    data = request.get_json()
    data['action'] = 'label'

    # put message in queue for processing
    r.publish('hive_messages', json.dumps(data))

    data['result'] = 'ok'
    return jsonify(data)


# reset model
@app.route("/api/reset")
def reset():
    global r

    # put message in queue for processing
    r.publish('hive_messages', json.dumps({'action': 'reset'}))

    return jsonify({'result': 'ok'})

# simulate crowd annotating
@app.route("/api/simulate")
def simulate():
    global r

    # put message in queue for processing
    r.publish('hive_messages', json.dumps({'action': 'simulate'}))

    return jsonify({'result': 'ok'})

# return image from dataset
def return_image(img_data):
    img = PIL.Image.fromarray(img_data)
    bytes = io.BytesIO()
    img.save(bytes, 'PNG')
    bytes.seek(0)
    return send_file(bytes, mimetype='image/png')

# return training image
@app.route("/api/image/train/<int:image_id>")
def get_train_image(image_id):
    img_data = np.uint8(model._train_images[image_id])
    return return_image(img_data)

# return test image
@app.route("/api/image/test/<int:image_id>")
def get_test_image(image_id):
    img_data = np.uint8(model._test_images[image_id])
    return return_image(img_data)

# default no cache
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    return r