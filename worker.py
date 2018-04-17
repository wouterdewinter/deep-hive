import redis
import json, random
from server.HiveModel import HiveModel
import logging, sys

# setup logging
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# connect redis
r = redis.StrictRedis(host='redis', port=6379, charset="utf-8", decode_responses=True)

# setup model
model = HiveModel(path='data/128x128')
model.init_model()

# create initial list for all test images
r.delete('accuracies')
r.set('annotation_count', 0)
r.delete('test_labels')
r.delete('test_scores')
r.rpush('test_labels', * [-1] * model._test_x.shape[0])
r.rpush('test_scores', * [-1] * model._test_x.shape[0])

# listen for labels
logging.info("Listening for new labels")
p = r.pubsub()
p.subscribe('hive_messages')

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

