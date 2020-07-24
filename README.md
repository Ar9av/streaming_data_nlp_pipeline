# Real Time Streaming Data Sentiment Analysis 

Real Time Company Sentiment Analysis and Forecasting -  Day by day sentiment(positive/negative/neutral) of the company (or query). 

### Installation
- Clone this repo to your local machine using
```shell
$ git clone https://github.com/Ar9av/streaming_data_nlp_pipeline.git
```
change the working directory

```shell
$ cd streaming_data_nlp_pipeline
```

### Setup / Requirements

- Install the requirements using the following commands

```shell
$ pip install -r requirements.txt
```

- Make sure you have Redis

In case not , Run the following to install and start redis-server

#### Redis Installation

```shell
$ cd
$ wget http://download.redis.io/releases/redis-6.0.6.tar.gz
$ tar xzf redis-6.0.6.tar.gz
$ cd redis-6.0.6
$ make
```

#### Redis Server Start

```shell
$ src/redis-server
```


Once the redis server is started 

### Configuring the Parameter

Cange the parameters in ``config.yml`` and change the ``COMPANY_NAME`` to the desired query and run the following command.


- Now in different terminal windows run the following:

```shell
$ python consumer/consumer.py
```

```shell
$ python time_series_analytics/time_series.py
```

```shell
$ python producer/prod.py
```

If the above throws error , probably you have different versions of python installed in your system.
Replace ``python`` with ``python3``

NOTE: Maintain the order of run to get the result instantenously as new results take time.

The windows should look something like this producing the necessary output.

![3-terminals](https://github.com/Ar9av/streaming_data_nlp_pipeline/blob/master/resources/terminals.png)


3 tasks : <br />
    1) Scraping Data (``prod.py``) <br />
    2) Sentiment Analysis (``consumer.py``) <br />
    3) Time Series Forecasting (``time_series.py``) <br />

Run in async matter but waits for the response from others through 3 redis channels which is used for publishing and listening.


