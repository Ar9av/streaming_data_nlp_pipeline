from fasttext_sentiment_analysis import FastTextSentiment

class SentimentAnaysis:

    def __init__(self, model_path):
        self.g = FastTextSentiment(model_path)

    def predict_sentiment(self, msg):
        msg = self.preprocess(msg)
        label, score = self.g.score(msg)
        if label[0][-1] == '1':
            label = 'negative'
        elif label[0][-1] == '2':
            label = 'neutral'
        elif label[0][-1] == '3':
            label = 'neutral'
        elif label[0][-1] == '4':
            label = 'positive'
        score = score.tolist()[0]
        return label, score

    def preprocess(self, msg):
        return msg
