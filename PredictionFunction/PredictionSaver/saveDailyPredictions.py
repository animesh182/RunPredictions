import psycopg2
import logging
import pandas as pd
import uuid
from datetime import timedelta,datetime
# Define your database parameters here
from PredictionFunction.utils.params import params


def save_daily_predictions(data):
    # Define the query
    raw_query = """    INSERT INTO public."Predictions_predictions"(
	id, date, restaurant, total_gross, created_at, company)
	VALUES %s"""
    try:
        with psycopg2.connect(**params) as conn:
            # Use Pandas to directly read the SQL query into a DataFrame
            df = pd.read_sql_query(raw_query, conn, params=[company,restaurant,start_date,end_date])
            return df
    except Exception as e:
        logging.error(f"Exception: {e}")
        return None
