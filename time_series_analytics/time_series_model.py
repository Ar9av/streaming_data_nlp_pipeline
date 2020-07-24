from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import mean_squared_error
import numpy
from math import sqrt
import os
import yaml

CONFIG_PATH = "."

with open(os.path.join(CONFIG_PATH,"config.yml")) as cf:
    variables = yaml.load(cf, Loader=yaml.FullLoader)
    MODEL = variables['MODEL_PATH']

class TimeSeriesAnalysis:

    def __init__(self):
        self.model_fit = None
        pass

    def build_model(self, df):
        print(df)
        series = df['Score']
        X = self.difference(df['Score'])
        size = int(len(X) * 0.9)
        train, test = X[0:size], X[size:]
        model = AutoReg(train, lags=1)
        self.model_fit = model.fit()
        self.save_model(X, series)
        coef = self.model_fit.params
        history = [train[i] for i in range(len(train))]
        predictions = list()
        for t in range(len(test)):
            yhat = self.predict(coef, history)
            obs = test[t]
            predictions.append(yhat)
            history.append(obs)
        rmse = sqrt(mean_squared_error(test, predictions))
        print('Test RMSE: %.3f' % rmse)
        tomorrows_prediction = self.model_predict()
        return tomorrows_prediction

    def save_model(self, X, series):
        self.model_fit.save(os.path.join(MODEL,'ar_model.pkl'))
        numpy.save(os.path.join(MODEL,'ar_data.npy'), X)
        numpy.save(os.path.join(MODEL, 'ar_obs.npy'), [series.values[-1]])
    
    def predict(self, coef, history):
        yhat = coef[0]
        for i in range(1, len(coef)):
            yhat += coef[i] * history[-i]
        return yhat
        
    def difference(self, dataset):
        diff = list()
        for i in range(1, len(dataset)):
            value = dataset[i] - dataset[i - 1]
            diff.append(value)
        return numpy.array(diff)
    
    def model_predict(self):
        data = numpy.load(os.path.join(MODEL,'ar_data.npy'))
        last_ob = numpy.load(os.path.join(MODEL,'ar_obs.npy'))
        predictions = self.model_fit.predict(start=len(data), end=len(data))
        yhat = predictions[0] + last_ob
        print('Tomorrow\'s expected sentiment score prediction: %f' % yhat)
        return yhat

    def update_model(self, dataset):
        data = numpy.load('ar_data.npy')
        last_ob = numpy.load('ar_obs.npy')
            
        for i in dataset['Score']:
            observation = i
            diffed = observation - last_ob[0]
            data = numpy.append(data, [diffed], axis=0)
            last_ob[0] = observation
        numpy.save('ar_data.npy', data)
        numpy.save('ar_obs.npy', last_ob)
        print("Model Updated")
        self.model_fit = model.fit()
        self.save_model(X, last_ob)
        coef = self.model_fit.params
        history = [train[i] for i in range(len(train))]
        predictions = list()
        for t in range(len(test)):
            yhat = self.predict(coef, history)
            obs = test[t]
            predictions.append(yhat)
            history.append(obs)
        rmse = sqrt(mean_squared_error(test, predictions))
        print('Test RMSE: %.3f' % rmse)   
        tomorrows_prediction = self.model_predict()
        return tomorrows_prediction  

    def train_model(self):
        X = numpy.load('ar_data.npy')
        last_ob = numpy.load('ar_obs.npy')
        size = int(len(X) * 0.9)
        train, test = X[0:size], X[size:]
        model = AutoReg(train, lags=1)
        self.model_fit = model.fit()
        self.save_model(X, last_ob)
        coef = self.model_fit.params
        history = [train[i] for i in range(len(train))]
        predictions = list()
        for t in range(len(test)):
            yhat = self.predict(coef, history)
            obs = test[t]
            predictions.append(yhat)
            history.append(obs)
        rmse = sqrt(mean_squared_error(test, predictions))
        print('Test RMSE: %.3f' % rmse)   
        tomorrows_prediction = self.model_predict()
        return tomorrows_prediction   
        