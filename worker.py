import redis
import json
from server.HiveModel import HiveModel

# setup model
model = HiveModel(path='data/128x128')

# listen for labels
r = redis.StrictRedis(host='localhost', port=6379)
p = r.pubsub()
p.subscribe('labels')

test_id = 0
r.delete('sample_label')
r.delete('sample_accuracy')

r.rpush('test_labels', * [-1] * model._test_x.shape[0])
r.rpush('test_scores', * [-1] * model._test_x.shape[0])

print("Listening for new labels")
for message in p.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        model.label(data['image_id'], data['class_id'])

        acc, label = model.evaluate(test_id)

        test_id = test_id + 1
        if test_id > model._test_x.shape[0] - 1:
            test_id = 0

        # push to accuracy history
        r.lpush('accuracies', acc)

        # trim list to last n entries
        r.ltrim('accuracies', 0, 64)

        # save result
        r.lset('test_labels', test_id, label)
        r.lset('test_scores', test_id, acc)


