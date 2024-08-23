from datetime import datetime, timezone, date
import logging
import azure.functions as func
import pandas as pd
from PredictionFunction.meta_tables import (
    data,
    location_specific_dictionary,
    weather_locations,
)
from PredictionFunction.PredictionTypes.daily_data_prep import (
    prepare_data as prepare_daily_data,
)
from PredictionFunction.PredictionTypes.alcohol_mix_data_prep import (
    product_mix_predictions as prepare_alcohol_data,
)
from PredictionFunction.PredictionTypes.hourly_data_prep import (
    hourly_sales as prepare_hourly_data,
)
from PredictionFunction.PredictionTypes.take_out_data_prep import (
    type_predictor as prepare_takeout_data,
)
from PredictionFunction.predict import predict
from PredictionFunction.save_to_db import save_to_db
from datetime import timedelta
from PredictionFunction.utils.create_temp_json import (
    fetch_or_initialize_json,
    update_execution_count,
    save_json_file,
    select_minimum_restaurant,
)
import psycopg2
from PredictionFunction.utils.params import prod_params


async def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    start_date = "2021-09-01"
    prediction_category = "day"

    data = fetch_or_initialize_json()
    company, restaurant = select_minimum_restaurant(data)
    # city = instance["City"]

    if company == "Fisketorget":
        start_date = date(2021, 9, 1)
        end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    if restaurant == "Oslo Torggata":
        start_date = date(2022, 5, 10)
    elif restaurant == "Sandnes":
        start_date = date(2023, 4, 18)
    elif restaurant == "Alexander Kielland":
        start_date = date(2024, 4, 10)
    elif restaurant == "Bjørvika":
        start_date = date(2024, 4, 19)
        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    # elif restaurant == "Restaurantdrift AS":
    #     start_date = date(2023, 9, 1)
    #     end_date = date(2024,7,7)
    else:
        start_date = date(2021, 9, 1)
    # end_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")
    with psycopg2.connect(**prod_params) as conn:
        with conn.cursor() as cursor:
            end_date_query = '''
            SELECT MAX(gastronomic_day)
            FROM public."SalesData"
            WHERE restaurant = %s
        '''
            cursor.execute(end_date_query,(restaurant,))
            latest_gastronomic_day = cursor.fetchone()[0]
            if latest_gastronomic_day:
                latest_date = latest_gastronomic_day - timedelta(days=1)
                end_date= latest_date.strftime("%Y-%m-%d")
    conn.close()
    # end_date = date(2024,4,27)
    logging.info(end_date)
    restaurant_func = location_specific_dictionary[restaurant]
    logging.info(f"Running predictions for now {restaurant}")
    if prediction_category == "hour":
        merged_data, historical_data, future_data = prepare_hourly_data(
            company, restaurant, start_date, end_date
        )
    elif prediction_category == "type":
        merged_data, historical_data, future_data = prepare_takeout_data(
            company, restaurant, start_date, end_date
        )
    elif prediction_category == "alcohol":
        merged_data, historical_data, future_data = prepare_alcohol_data(
            company, restaurant, start_date, end_date
        )
    elif prediction_category == "day":
        merged_data, historical_data, future_data = prepare_daily_data(
            company, restaurant, start_date, end_date
        )
    logging.info(f"Running predictions for now {restaurant}")
    model, future_df, current_df, event_holidays, venues_list = restaurant_func(
        prediction_category, restaurant, merged_data, historical_data, future_data
    )
    logging.info(f"done")
    forecast = predict(
        model,
        future_df,
    )
    new_df = current_df[["ds", "y"]].rename(
        columns={"ds": "ds", "y": "historical_sale"}
    )
    forecast = pd.merge(
        forecast, new_df[["ds", "historical_sale"]], on="ds", how="left"
    )
    forecast["historical_sale"].fillna(0, inplace=True)
    forecast["historical_sale"] = forecast["historical_sale"].astype(int)
    logging.info(f"done")
    save_to_db(
        forecast, company, restaurant, prediction_category, event_holidays, end_date, venues_list
    )
    data = update_execution_count(data, company, restaurant)

    # Save the updated JSON data back to Azure Blob Storage
    save_json_file(data)
