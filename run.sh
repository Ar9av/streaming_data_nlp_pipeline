#!/bin/bash
python3 consumer/consumer.py &
python3 time_series_analytics/time_series.py &
python3 producer/prod.py