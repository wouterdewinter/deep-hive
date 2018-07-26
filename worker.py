"""Worker that listens to events from the Flask webserver and runs the keras model
"""

import redis
import json, random
import logging, sys
from server.HiveModel import HiveModel
from server.Config import Config

# setup logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# connect redis
r = redis.StrictRedis(host=Config.REDIS_HOST, port=6379, charset="utf-8", decode_responses=True)

# setup model
model = HiveModel(path=Config.IMAGE_PATH, img_size=Config.IMAGE_SIZE)

# listen for labels
logging.info("Listening for new labels")
p = r.pubsub()
p.subscribe('hive_messages')


def run_test(model, r, test_id):
    """Evaluate a single image"""

    # evaluate
    acc, label = model.evaluate(test_id)

    # push to accuracy history and trim list to last n entries
    r.lpush('accuracies', acc)
    r.ltrim('accuracies', 0, 64)

    # save result
    r.lset('test_labels', test_id, label)
    r.lset('test_scores', test_id, acc)


def reset(r, model, test_ids):
    """Reset keras model"""

    # init (or reset) model
    model.init_model()

    # init redis metrics
    r.delete('accuracies')
    r.set('annotation_count', 0)
    r.delete('test_labels')
    r.delete('test_scores')
    r.rpush('test_labels', * [-1] * model._test_x.shape[0])
    r.rpush('test_scores', * [-1] * model._test_x.shape[0])

    # first evaluate all test images to provide baseline for untrained model
    for test_id in test_ids:
        run_test(model, r, test_id)

# create shuffled list of test_ids
test_ids = list(range(0, model._test_x.shape[0]))
random.shuffle(test_ids)
test_index = 0

# start with clean model and metrics
reset(r, model, test_ids)

while True:
    message = p.get_message()

    # only pick up real messages (ignore subscribe messages, etc)
    if message and message['type'] == 'message':

        # unpack data from message
        data = json.loads(message['data'])

        # annotation message
        if data['action'] == 'label':

            # perform training cycle
            model.label(data['image_id'], data['class_id'])

            # increase counter for total number of annotations
            r.incr('annotation_count')

            # pick next test image to evaluate
            test_index += 1
            if test_index >= len(test_ids):
                test_index = 0

            # evaluate
            test_id = test_ids[test_index]
            run_test(model, r, test_id)

        # reset message
        if data['action'] == 'reset':
            logging.info("Resetting model and metrics")
            reset(r, model, test_ids)

        # simulate perfect annotations
        if data['action'] == 'simulate':
            for i, x in enumerate(model._train_x):
                class_id = model._train_labels[i]
                data = {
                    'action': 'label',
                    'image_id': int(i),
                    'class_id': int(class_id)
                }
                r.publish('hive_messages', json.dumps(data))
