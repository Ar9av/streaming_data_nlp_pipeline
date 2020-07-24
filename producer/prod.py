import mq
import redis
import time
from gnewsclient import gnewsclient
import yaml
import os

r = redis.Redis()

CONFIG_PATH = "."

with open(os.path.join(CONFIG_PATH,"config.yml")) as cf:
    variables = yaml.load(cf, Loader=yaml.FullLoader)
    COMPANY_NAME =variables['COMPANY_NAME']

g = gnewsclient(query = COMPANY_NAME)


def process(news):
    news_as_set = []
    for i in news:
        news_as_set.append(i['title'] + "#$#$#$" + i['releasedAt'])
    return set(news_as_set)

setA = set()
while True:
    news = g.get_news()
    setB = process(news)
    new_news = setB - setA
    print(f"Retrieved {len(new_news)} new articles")
    for i in new_news:
        sentence, date = tuple(i.split("#$#$#$"))
        data = {"sentence": sentence, "date": date}
        msg = mq.serialize_message_data(data)
        r.publish('news', msg)
    setA = setA.union(setB)
    time.sleep(60)
    print("Checking for new news update")

