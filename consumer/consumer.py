import redis
from sentiment_analysis import SentimentAnaysis
import os
import mq
import yaml

CONFIG_PATH = "."

with open(os.path.join(CONFIG_PATH,"config.yml")) as cf:
    variables = yaml.load(cf, Loader=yaml.FullLoader)
    sentiment_model_path =variables['SENTIMENT_MODEL_PATH']
    
sent = SentimentAnaysis(sentiment_model_path)

r = redis.Redis()
sub = r.pubsub(ignore_subscribe_messages=True)
sub.subscribe(['news'])


def process_message(data):
    label, score = sent.predict_sentiment(data)
    return (label, score)

for post in sub.listen():
    data = mq.read_message_data(post)
    sentence = data['sentence']
    date = data['date']
    label, score = process_message(sentence)
    d = {'sentence': sentence, 'score': score, 'label': label, 'date': date}
    print(d)
    serialized_d = mq.serialize_message_data(d)
    r.publish('sentiment_results', serialized_d)
