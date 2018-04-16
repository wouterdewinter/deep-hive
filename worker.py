import redis
import json, random
from server.HiveModel import HiveModel

# connect redis
r = redis.StrictRedis(host='localhost', port=6379)

# setup model
model = HiveModel(path='data/128x128')

#r.delete('sample_label')
#r.delete('sample_accuracy')

# create initial list for all test images
r.rpush('test_labels', * [-1] * model._test_x.shape[0])
r.rpush('test_scores', * [-1] * model._test_x.shape[0])

# listen for labels
print("Listening for new labels")
p = r.pubsub()
p.subscribe('labels')
for message in p.listen():

    # only pick up real messages (ignore subscribe messages, etc)
    if message['type'] == 'message':
        data = json.loads(message['data'])

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


