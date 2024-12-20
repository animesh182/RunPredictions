import pandas as pd
import logging
from prophet import Prophet
from PredictionFunction.Datasets.OpeningHours.lostacos_opening_hours import (
    restaurant_opening_hours,
)
import numpy as np
from PredictionFunction.Datasets.Regressors.general_regressors import (
    is_specific_month,
    is_covid_restriction_christmas,
    is_closed,
    is_fall_start,
    is_christmas_shopping,
    is_campaign_active,
    is_high_weekends,
    is_fellesferie,
    is_high_weekend_spring
)
from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    last_working_day,
    fifteenth_working_days,
    fornebu_large_concerts,
    ullevaal_big_football_games,
)
from PredictionFunction.Datasets.Concerts.concerts import (
    oslo_spektrum,
    sentrum_scene_oslo,
)
from PredictionFunction.utils.fetch_events import fetch_events
from PredictionFunction.Datasets.Regressors.weather_regressors import (
    warm_dry_weather_spring,
    # warm_and_dry_future,
    heavy_rain_fall_weekday,
    heavy_rain_fall_weekend,
    heavy_rain_spring_weekday,
    heavy_rain_spring_weekend,
    # heavy_rain_winter_weekday,
    ## there hasnt been any instances of heavy rain winter weekend for torggata yet. Test later
    # heavy_rain_winter_weekend,
    heavy_rain_fall_weekday_future,
    heavy_rain_fall_weekend_future,
    heavy_rain_spring_weekday_future,
    heavy_rain_spring_weekend_future,
    # heavy_rain_winter_weekday_future,
    # heavy_rain_winter_weekend_future,
    # warm_dry_weekday_spring,
    # warm_dry_weekend_spring,
    # warm_dry_weekend_fall,
    # warm_dry_weather_spring,
    # warm_dry_weekday_spring_future,
    # warm_dry_weekend_spring_future,
    # warm_dry_weekend_fall_future,
)
from PredictionFunction.Datasets.Regressors.event_weather_regressors import (
    is_event_with_bad_weather,
    is_event_with_good_weather,
    is_event_with_normal_weather
)
from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    last_working_day,
    fifteenth_working_days,
)
from PredictionFunction.Datasets.Holidays.LosTacos.Restaurants.karl_johan_holidays import (
    closed_days,
    black_friday,
)
from PredictionFunction.Datasets.Holidays.LosTacos.common_oslo_holidays import (
    firstweek_jan,
    lockdown,
    oslo_pride,
    musikkfestival,
    oslo_marathon,
    kk_mila
)

from PredictionFunction.Datasets.Holidays.LosTacos.common_holidays import (
    hostferie_sor_ostlandet_weekdend,
    first_weekend_christmas_school_vacation,
    seventeenth_may,
    easter,
    new_years_day,
    first_may,
    pinse,
    himmelfart,
    christmas_day,
    new_year_romjul,
)

from PredictionFunction.utils.utils import (
    calculate_days_30,
    calculate_days_15,
    custom_regressor,
)
import xgboost as xgb
from datetime import date
from PredictionFunction.utils.openinghours import add_opening_hours


def karl_johan(
    prediction_category, restaurant, merged_data, historical_data, future_data
):
    event_holidays = pd.DataFrame()
    sales_data_df = historical_data
    sales_data_df = sales_data_df.rename(columns={"date": "ds"})

    future_data = future_data.rename(columns={"date": "ds"})

    merged_data = merged_data.rename(columns={"date": "ds"})
    sales_data_df["ds"] = pd.to_datetime(sales_data_df["ds"])

    # Add weather parameters to df
    # df = add_weather_parameters(sales_data_df, prediction_category)

    if prediction_category == "day":
        df = (
            sales_data_df.groupby(["ds"])
            .agg(
                {
                    "total_net": "sum",
                    "sunshine_amount": "sum",
                    "rain_sum": "sum",
                    "windspeed": "mean",
                    "air_temperature": "mean",
                }
            )
            .reset_index()
        )
        df.fillna(
            {"sunshine_amount": 0, "rain_sum": 0, "windspeed": 0, "air_temperature": 0},
            inplace=True,
        )
        df.columns = [
            "ds",
            "y",
            "sunshine_amount",
            "rain_sum",
            "windspeed",
            "air_temperature",
        ]

    elif prediction_category == "hour":
        df = (
            sales_data_df.groupby(["ds", "hour"])
            .agg(
                {
                    "total_net": "sum",
                    "sunshine_amount": "sum",
                    "rain_sum": "sum",
                    "windspeed": "mean",
                    "air_temperature": "mean",
                }
            )
            .reset_index()
        )
        df.fillna(
            {"sunshine_amount": 0, "rain_sum": 0, "windspeed": 0, "air_temperature": 0},
            inplace=True,
        )
        df.columns = [
            "ds",
            "hour",
            "y",
            "sunshine_amount",
            "rain_sum",
            "windspeed",
            "air_temperature",
        ]

    elif prediction_category in ["type", "product"]:
        df = (
            sales_data_df.groupby(["ds"])
            .agg(
                {
                    "percentage": "max",
                    "sunshine_amount": "sum",
                    "rain_sum": "sum",
                    "windspeed": "mean",
                    "air_temperature": "mean",
                }
            )
            .reset_index()
        )
        df.fillna(
            {"sunshine_amount": 0, "rain_sum": 0, "windspeed": 0, "air_temperature": 0},
            inplace=True,
        )
        df.columns = [
            "ds",
            "y",
            "sunshine_amount",
            "rain_sum",
            "windspeed",
            "air_temperature",
        ]
    # df['y'] = np.log(df['y'])
    else:
        raise ValueError(f"Unexpected prediction_category value: {prediction_category}")
    # fig = px.histogram(df, x="y")
    # fig.show()
    df = heavy_rain_spring_weekend(df)
    df = heavy_rain_spring_weekday(df)
    df = heavy_rain_fall_weekend(df)
    df = heavy_rain_fall_weekday(df)
    df = warm_dry_weather_spring(df)
    df = calculate_days_15(df, fifteenth_working_days)
    df = add_opening_hours(df, "Karl Johan", [12], [17])

    m = Prophet()

    ### Holidays and other repeating outliers
    m.add_country_holidays(country_name="NO")

    holidays = pd.concat(
        (
            christmas_day,
            firstweek_jan,
            easter,
            first_may,
            new_years_day,
            seventeenth_may,
            pinse,
            himmelfart,
            lockdown,
            closed_days,
            black_friday,
            hostferie_sor_ostlandet_weekdend,
            first_weekend_christmas_school_vacation,
            oslo_pride,
            musikkfestival,
            christmas_day,
            new_year_romjul,
            oslo_marathon,
            kk_mila
        )
    )
    # Didnt use, because the effect was too small or looked incorrect: piknik_i_parken,inferno

    df["specific_month"] = df["ds"].apply(is_specific_month)

    # Add new columns in your dataframe to indicate if a date is within or outside the restrictions period
    df["covid_restriction_christmas"] = df["ds"].apply(is_covid_restriction_christmas)

    df["closed_jan"] = df["ds"].apply(is_closed)

    # Some weeks have the same weekly seasonality but more extreme and just higher. Add that here
    # Convert 'ds' column to datetime if it is not already
    df["ds"] = pd.to_datetime(df["ds"])
    # Calculate the week number for each date
    df["week_number"] = df["ds"].dt.isocalendar().week

    # pattern august-sept
    # Convert 'ds' column to datetime if it is not already
    df["ds"] = pd.to_datetime(df["ds"])

    # Define the start and end dates for the specific date interval
    start_date = "2022-08-15"
    end_date = "2022-09-18"
    # make start_date and end:date datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Create a mask for the specific date interval
    date_mask = (df["ds"] >= start_date) & (df["ds"] <= end_date)

    # Calculate the week number for the start and end dates
    start_week = pd.to_datetime(start_date).week
    end_week = pd.to_datetime(end_date).week

    # Calculate the week number for each date
    df["week_number"] = df["ds"].dt.isocalendar().week

    # Calculate the custom regressor values for the specific date interval
    df.loc[date_mask, "custom_regressor"] = df.loc[date_mask, "week_number"].apply(
        custom_regressor
    )
    # Fill the custom regressor with zeros for the rows outside the specific date interval
    df.loc[~date_mask, "custom_regressor"] = 0
    df["fall_start"] = df["ds"].apply(is_fall_start)
    df["christmas_shopping"] = df["ds"].apply(is_christmas_shopping)
    df["is_fellesferie"] = df["ds"].apply(is_fellesferie)
    df["high_weekend_spring"] = df["ds"].apply(is_high_weekend_spring)

    karl_johan_venues = {
        "Oslo Spektrum",
        "Sentrum Scene",
        "Fornebu",
        "Ulleval",
        "Rockefeller",
        "Cosmopolite, Oslo",
        "Oslo City",
        "Oslo Konserthus",
        "Nordic Black Theatre",
        "Oslo Concert Hall",
        "Salt Langhuset",
        "Tons of Rock"
    }

    data = {"name": [], "effect": []}
    city='Oslo'
    venue_list = karl_johan_venues
    regressors_to_add = []
    for venue in karl_johan_venues:
        # for venue in karl_johan_venues:
        venue_df = fetch_events("Oslo Torggata", venue,city)
        event_holidays = pd.concat(objs=[event_holidays, venue_df], ignore_index=True)
        if "name" in venue_df.columns:
            venue_df = venue_df.drop_duplicates("date")
            venue_df["date"] = pd.to_datetime(venue_df["date"])
            venue_df = venue_df.rename(columns={"date": "ds"})
            venue_df["ds"] = pd.to_datetime(venue_df["ds"])
            venue_df = venue_df[["ds", "name"]]
            venue_df.columns = ["ds", "event"]
            dataframe_name = venue.lower().replace(" ", "_").replace(",", "")
            venue_df[dataframe_name] = 1
            df = pd.merge(df, venue_df, how="left", on="ds", suffixes=("", "_venue"))
            df = is_event_with_good_weather(df,dataframe_name)
            df = is_event_with_bad_weather(df,dataframe_name)
            df = is_event_with_normal_weather(df,dataframe_name)
            df[dataframe_name].fillna(0, inplace=True)
            regressors_to_add.append(
                (venue_df, dataframe_name)
            )  # Append venue_df along with venue name for regressor addition
        else:
            holidays = pd.concat(objs=[holidays, venue_df], ignore_index=True)
    event_holidays= pd.concat(objs=[event_holidays, holidays], ignore_index=True)
    
    df["high_weekend"] = df["ds"].apply(is_high_weekends)
    df["low_weekend"] = ~df["ds"].apply(is_high_weekends)

    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
    df = calculate_days_30(df, last_working_day)

    # create daily seasonality column setting a number for each day of the week, to be used later
    # Create a Boolean column for each weekday
    for weekday in range(7):
        df[f"weekday_{weekday}"] = df["ds"].dt.weekday == weekday

    # Add the custom regressor and seasonalities before fitting the model
    if prediction_category == "hour":
        m = Prophet(
            holidays=holidays,
            weekly_seasonality=False,
            yearly_seasonality=True,
            daily_seasonality=True,
            changepoint_prior_scale=0.1,
        )

        # Add a conditional seasonality for each weekday
        for weekday in range(7):
            m.add_seasonality(
                name=f"hourly_weekday_{weekday}",
                period=1,
                fourier_order=10,
                condition_name=f"weekday_{weekday}",
            )

    else:
        m = Prophet(
            holidays=holidays,
            # yearly_seasonality=10,
            daily_seasonality=False,
            changepoint_prior_scale=5,
            # changepoint_range=0.8
        )


    for event_df, regressor_name in regressors_to_add:
        if "event" in event_df.columns:
            # m.add_regressor(regressor_name)
            m.add_regressor(regressor_name + '_good_weather')
            m.add_regressor(regressor_name + '_bad_weather')
            m.add_regressor(regressor_name + '_normal_weather')

    # Weather regressors
    m.add_regressor("heavy_rain_fall_weekday")
    m.add_regressor("heavy_rain_fall_weekend")
    m.add_regressor("heavy_rain_spring_weekday")
    m.add_regressor("heavy_rain_spring_weekend")
    m.add_regressor('warm_and_dry')
    # Add the payday columns as regressors
    m.add_regressor("days_since_last_30")
    m.add_regressor("days_until_next_30")
    m.add_regressor("sunshine_amount")
    m.add_regressor("rain_sum")
    m.add_regressor("opening_duration")
    m.add_regressor("custom_regressor")
    m.add_regressor("closed_jan")
    m.add_regressor("high_weekend_spring",mode='multiplicative')

    m.add_seasonality(name="monthly", period=30.5, fourier_order=5)

    m.add_seasonality(
        name="covid_restriction_christmas",
        period=7,
        fourier_order=1000,
        condition_name="covid_restriction_christmas",
    )

    m.add_seasonality(
        name="weekly_fall_start", period=7, fourier_order=3, condition_name="fall_start"
    )

    m.add_seasonality(
        name="is_fellesferie",
        period=30.5,
        fourier_order=5,
        condition_name="is_fellesferie",
    )

    m.add_seasonality(
        name="christmas_shopping",
        period=7,
        fourier_order=3,
        condition_name="christmas_shopping",
    )

    m.add_seasonality(
        name="high_weekend", period=7, fourier_order=5, condition_name="high_weekend"
    )
    m.fit(df)

    future = m.make_future_dataframe(periods=60, freq="D")

    # Add weather future df

    # Add relevant columns to the future df
    future["rain_sum"] = merged_data["rain_sum"]
    future["sunshine_amount"] = merged_data["sunshine_amount"]
    future["windspeed"] = merged_data["windspeed"]
    future["air_temperature"] = merged_data["air_temperature"]

    future.fillna(
        {"sunshine_amount": 0, "rain_sum": 0, "windspeed": 0, "air_temperature": 0},
        inplace=True,
    )

    for event_df, event_column in regressors_to_add:
        if "event" in event_df.columns:
            event_df = event_df.drop_duplicates("ds")
            future = pd.merge(
                future,
                event_df[["ds", event_column]],
                how="left",
                on="ds",
            )
            future[event_column].fillna(0, inplace=True)
            future = is_event_with_good_weather(future,event_column)
            future = is_event_with_bad_weather(future,event_column)
            future = is_event_with_normal_weather(future,event_column)

    # Apply the future functions for weather regressions here
    future = heavy_rain_spring_weekend_future(future)
    future = heavy_rain_spring_weekday_future(future)
    future = heavy_rain_fall_weekend_future(future)
    future = heavy_rain_fall_weekday_future(future)
    future = warm_dry_weather_spring(future)
    # add the last working day and the +/- 5 days
    future = calculate_days_30(future, last_working_day)
    future["high_weekend"] = future["ds"].apply(is_high_weekends)
    future["is_fellesferie"] = future["ds"].apply(is_fellesferie)
    merged_data["ds"] = pd.to_datetime(merged_data["ds"], format="%Y", errors="coerce")

    future["covid_restriction_christmas"] = future["ds"].apply(
        is_covid_restriction_christmas
    )

    future["fall_start"] = future["ds"].apply(is_fall_start)

    future["christmas_shopping"] = future["ds"].apply(is_christmas_shopping)

    future["specific_month"] = future["ds"].apply(is_specific_month)
    future["high_weekend_spring"] = future["ds"].apply(is_high_weekend_spring)
    # Calculate the custom regressor values for the future dates
    future["ds"] = pd.to_datetime(future["ds"])
    future_date_mask = (future["ds"] >= start_date) & (future["ds"] <= end_date)
    future["week_number"] = future["ds"].dt.isocalendar().week
    future.loc[future_date_mask, "custom_regressor"] = future.loc[
        future_date_mask, "week_number"
    ].apply(custom_regressor)
    future.loc[~future_date_mask, "custom_regressor"] = 0
    future["closed_jan"] = future["ds"].apply(is_closed)

    # Add the 'sunshine_amount' column to the future dataframe
    if prediction_category != "hour":
        future["ds"] = future["ds"].dt.date
    future.fillna(0, inplace=True)
    future = add_opening_hours(future, "Karl Johan", [12], [17])

    return m, future, df, event_holidays, venue_list


def location_function(
    prediction_category, restaurant, merged_data, historical_data, future_data
):
    return karl_johan(
        prediction_category, restaurant, merged_data, historical_data, future_data
    )
