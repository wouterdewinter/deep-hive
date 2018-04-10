import redis
import json
from server.HiveModel import HiveModel

# setup model
model = HiveModel(path='data/128x128')

# listen for labels
r = redis.StrictRedis(host='localhost', port=6379)
p = r.pubsub()
p.subscribe('labels')

print("Listening for new labels")
for message in p.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        model.label(data['image_id'], data['class_id'])
        acc = model.evaluate()
        r.lpush('accuracies', acc)

        # only keep last 10
        r.ltrim('accuracies', 0, 10)