import redis
import mq
import traces
from time_series_model import TimeSeriesAnalysis
import pandas as pd
from datetime import datetime, timedelta

model = TimeSeriesAnalysis()

r = redis.Redis()
BATCH = 50



sub = r.pubsub(ignore_subscribe_messages=True)
sub.subscribe(['sentiment_results'])

def build_model(data_list, flag):
    if flag == True:
        prediction = model.update_model(data_list)
    elif flag == "train":
        prediction = model.train_model()
    else:
        prediction = model.build_model(data_list)
    return prediction

def convert_to_df(dataset):
    df = pd.DataFrame()
    Date = [i['date'] for i in dataset]
    Score = [i['score'] for i in dataset]
    df['Date'] = Date
    df['Score'] = Score
    return df

def normalize(df):
    date = [i[:10] for i in df['Date']]
    df['Date'] = date
    dff = df.groupby('Date', as_index=False).mean()
    dates = [datetime.strptime(d, '%Y-%m-%d') for d in dff['Date']]
    min_date = min(dates)
    max_date = max(dates)
    t = zip(dates, dff['Score'])
    ts = traces.TimeSeries(t)
    samples = ts.sample(
                        sampling_period=timedelta(days = 1),
                        start=min_date,
                        end=max_date,
                        interpolate='linear',
                    )
    sampled_dates = [d[0] for d in samples]
    sampled_scores = [d[1] for d in samples]
    sampled_df = pd.DataFrame()
    sampled_df['Date'] = sampled_dates
    sampled_df['Score'] = sampled_scores
    print(f"Overall Sentiment across {str(min_date)} to {str(max_date)} : {sum(l) / len(l)}")
    return dff

data_list = []
flag = False
epochs = 0
for post in sub.listen():
    epochs += 1
    data = mq.read_message_data(post)
    data_list.append(data)
    if len(data_list) == BATCH:
        df = convert_to_df(data_list)
        df = normalize(df)
        tomorrows_prediction = build_model(df, flag)
        flag = True
        serialized_prediction = mq.serialize_message_data(tomorrows_prediction.tolist())
        r.publish('results', serialized_prediction)
    if epochs == 1000:
        tomorrows_prediction = build_model(df, flag= "train")
        print("Training Model Again as 1000 data points recieved")
        serialized_prediction = mq.serialize_message_data(tomorrows_prediction.tolist())
        r.publish('results', serialized_prediction)
        

    
