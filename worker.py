import redis
import json, random
from server.HiveModel import HiveModel
from server.Config import Config

import logging, sys

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

def init_hive(r, model):
    # init (or reset) model
    model.init_model()

    # init redis metrics
    r.delete('accuracies')
    r.set('annotation_count', 0)
    r.delete('test_labels')
    r.delete('test_scores')
    r.rpush('test_labels', * [-1] * model._test_x.shape[0])
    r.rpush('test_scores', * [-1] * model._test_x.shape[0])

init_hive(r, model)

# for message in p.listen():
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

            # pick random test image to evaluate
            test_id = random.randint(0, model._test_x.shape[0] - 1)
            acc, label = model.evaluate(test_id)

            # push to accuracy history and trim list to last n entries
            r.lpush('accuracies', acc)
            r.ltrim('accuracies', 0, 64)

            # save result
            r.lset('test_labels', test_id, label)
            r.lset('test_scores', test_id, acc)

        # reset message
        if data['action'] == 'reset':
            logging.info("Resetting model and metrics")
            init_hive(r, model)

