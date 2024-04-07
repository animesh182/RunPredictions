from datetime import datetime, timezone
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


async def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
    start_date = "2021-09-01"
    # end_date = datetime.now().strftime("%Y-%m-%d")
    end_date = "2024-03-24"
    prediction_category = "day"
    # prediction category is either hour, type, alcohol or day
    company = "Los Tacos"
    if mytimer.past_due:
        logging.info("The timer is past due!")

    for instance in data:
        restaurant = instance["Restaurant"]
        city = instance["City"]
        company = instance["Company"]
        restaurant_func = location_specific_dictionary[restaurant]
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
        logging.info(f"Running predictions for {restaurant}")
        model, future_df, current_df, event_holidays = restaurant_func(
            prediction_category, restaurant, merged_data, historical_data, future_data
        )
        forecast = predict(
            model,
            future_df,
            current_df,
            company,
            restaurant,
            start_date,
            end_date,
            prediction_category,
        )
        new_df = current_df[["ds", "y"]].rename(
            columns={"ds": "ds", "y": "historical_sale"}
        )
        forecast = pd.merge(
            forecast, new_df[["ds", "historical_sale"]], on="ds", how="left"
        )
        forecast["historical_sale"].fillna(0, inplace=True)
        forecast["historical_sale"] = forecast["historical_sale"].astype(int)
        save_to_db(forecast, company, restaurant, prediction_category, event_holidays)
