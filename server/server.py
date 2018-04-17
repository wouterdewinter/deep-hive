#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, render_template, send_file
from flask_cors import CORS
import numpy as np
import PIL
import io
from HiveModel import HiveModel
import redis, json

image_id = 0
model = HiveModel(path='../data/128x128')

# connect to redis
r = redis.StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route("/")
def root():
    return app.send_static_file('index.html')

@app.route("/bundle.js")
def js():
    return app.send_static_file('bundle.js')

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

@app.route("/api/label", methods=['POST'])
def post_label():
    global r

    data = request.get_json()
    data['action'] = 'label'

    # put message in queue for processing
    r.publish('hive_messages', json.dumps(data))

    data['result'] = 'ok'
    return jsonify(data)


@app.route("/api/reset")
def reset():
    global r

    data = {'action': 'reset'}

    # put message in queue for processing
    r.publish('hive_messages', json.dumps(data))

    data['result'] = 'ok'
    return jsonify(data)

def return_image(img_data):
    img = PIL.Image.fromarray(img_data)
    bytes = io.BytesIO()
    img.save(bytes, 'PNG')
    bytes.seek(0)
    return send_file(bytes, mimetype='image/png')

@app.route("/api/image/train/<int:image_id>")
def get_train_image(image_id):
    img_data = np.uint8(model._train_images[image_id])
    return return_image(img_data)

@app.route("/api/image/test/<int:image_id>")
def get_test_image(image_id):
    img_data = np.uint8(model._test_images[image_id])
    return return_image(img_data)