import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import logging
from PredictionFunction.utils.fetch_sales_data import fetch_salesdata
from PredictionFunction.PredictionTypes.daily_data_prep import prepare_data
from PredictionFunction.utils.utils import tourist_data


def predict(m, future):
    if future.empty:
        raise ValueError("The future DataFrame is empty.")
    forecast = m.predict(future)
    forecast = pd.DataFrame(forecast)
    return forecast
