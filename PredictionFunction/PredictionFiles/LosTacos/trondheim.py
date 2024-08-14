import pandas as pd
import numpy as np
from prophet import Prophet
from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    cruise_ship_arrivals,
    twelfth_working_days,
    last_working_day,
)
import logging
from PredictionFunction.utils.utils import calculate_days_30, calculate_days_15,custom_regressor
from PredictionFunction.Datasets.OpeningHours.lostacos_opening_hours import restaurant_opening_hours
from PredictionFunction.Datasets.Seasonalities.LosTacos.weekly_seasonality import weekly_seasonalities
from PredictionFunction.Datasets.Regressors.general_regressors import (
    is_fellesferie,
    is_may,
    is_covid_restriction_christmas,
    is_fall_start,
    is_covid_loose_fall21,
    is_christmas_shopping,
)
from PredictionFunction.Datasets.Regressors.event_weather_regressors import (
    is_event_with_bad_weather,
    is_event_with_good_weather,
    is_event_with_normal_weather
)
from PredictionFunction.Datasets.Holidays.LosTacos.Restaurants.stavanger_holidays import (
    fadder_week,
    fjoge,
    military_excercise,
    outliers,
    closed_days,
)

from PredictionFunction.Datasets.Holidays.LosTacos.common_holidays import (
    first_may,
    firstweek_jan,
    pinse,
    himmelfart,
    hostferie_sor_ostlandet_weekdend,
    vinterferie_vestlandet_weekend,
    vinterferie_vestlandet_weekend_before,
    first_weekend_christmas_school_vacation,
    seventeenth_may,
    easter,
    christmas_day,
    new_year_romjul,
    new_years_day
)

from PredictionFunction.Datasets.Regressors.weather_regressors import(
    warm_dry_weather_spring_fss,
    # warm_dry_weather_spring,
    # warm_and_dry_future,
    # heavy_rain_fall_weekday,
    # heavy_rain_fall_weekday_future,
    heavy_rain_fall_weekend,
    heavy_rain_fall_weekend_future,
    heavy_rain_winter_weekday,
    heavy_rain_winter_weekday_future,
    heavy_rain_winter_weekend,
    heavy_rain_winter_weekend_future,
    # heavy_rain_spring_weekday,
    # heavy_rain_spring_weekday_future,
    # heavy_rain_spring_weekend,
    # heavy_rain_spring_weekend_future,
    non_heavy_rain_fall_weekend,
    non_heavy_rain_fall_weekend_future,

)
from PredictionFunction.Datasets.Regressors.event_weather_regressors import (
    is_event_with_bad_weather,
    is_event_with_good_weather,
    is_event_with_normal_weather
)
from PredictionFunction.utils.openinghours import add_opening_hours
from PredictionFunction.utils.fetch_events import fetch_events


def trondheim(prediction_category,restaurant,merged_data,historical_data,future_data):
    event_holidays=pd.DataFrame(columns=['event_names', 'name'])
    sales_data_df = historical_data
    sales_data_df = sales_data_df.rename(columns={"date": "ds"})
    sales_data_df["ds"] = pd.to_datetime(sales_data_df["ds"])

    future_data = future_data.rename(columns={"date": "ds"})
    future_data["ds"] = pd.to_datetime(future_data["ds"])

    merged_data = merged_data.rename(columns={"date": "ds"})
    merged_data["ds"] = pd.to_datetime(merged_data["ds"])


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


    df = heavy_rain_fall_weekend(df)
    df = heavy_rain_winter_weekday(df)
    df = heavy_rain_winter_weekend(df)
    # df = heavy_rain_spring_weekday(df)
    # df = heavy_rain_spring_weekend(df)
    df = non_heavy_rain_fall_weekend(df)
    df = warm_dry_weather_spring_fss(df)
    m = Prophet()

    ### Holidays and other repeating outliers
    m.add_country_holidays(country_name="NO")

    ONS = pd.DataFrame(
        {
            "holiday": "ONS",
            "ds": pd.to_datetime(["2022-08-31"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

    musikkfestrogaland = pd.DataFrame(
        {
            "holiday": "Musikkfest Rogaland",
            "ds": pd.to_datetime([""]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

    holidays = pd.concat(
        (
            christmas_day,
            firstweek_jan,
            fadder_week,
            first_may,
            easter,
            seventeenth_may,
            pinse,
            # fjoge,
            himmelfart,
            outliers,
            closed_days,
            military_excercise,
            hostferie_sor_ostlandet_weekdend,
            vinterferie_vestlandet_weekend_before,
            vinterferie_vestlandet_weekend,
            first_weekend_christmas_school_vacation,
            new_year_romjul,
            new_years_day
        )
    )

    df["fellesferie"] = df["ds"].apply(is_fellesferie)

    df["is_may"] = df["ds"].apply(is_may)

    # Define a function to check if the date is within the period of heavy COVID restrictions

    # Add new columns in your dataframe to indicate if a date is within or outside the restrictions period
    df["covid_restriction_christmas"] = df["ds"].apply(is_covid_restriction_christmas)

    # Some weeks have the same weekly seasonality but more extreme and just higher. Add that here
    # Convert 'ds' column to datetime if it is not already
    df["ds"] = pd.to_datetime(df["ds"])
    # Calculate the week number for each date
    df["week_number"] = df["ds"].dt.isocalendar().week

    # Convert 'ds' column to datetime if it is not already
    df["ds"] = pd.to_datetime(df["ds"])

    # Define the start and end dates for the specific date interval
    start_date = "2022-08-22"
    end_date = "2022-09-11"
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

    # Different weekly seasonality for 2 weeks in august related to starting fall semester/work
    df["fall_start"] = df["ds"].apply(is_fall_start)
    df["covid_loose_fall21"] = df["ds"].apply(is_covid_loose_fall21)
    df["christmas_shopping"] = df["ds"].apply(is_christmas_shopping)
    df= add_opening_hours(df,"Trondheim",12,17)

    trondheim_venues = {
            "Olavshallen Store Sal", "Studentersamfundet", "Litteraturhuset i Trondheim", "ISAK Kulturhus", "Lokal Bar",
            "Dokkhuset Scene", "Uka i Trondheim", "Byscenen", "Bar Moskus", "Kunsthallen",
            "Verkstedhallen", "Tapperiet Paa Dahls", "Lerkendal stadion", "Krigsseilerplassen", "Kafe Skuret",
            "Havet, Djupet", "Trondheim", "Trondheim Spektrum", "Havet, Langhuset", "Tapperiet EC Dahls Arena",
            "Havet, Heim, Trondheim"
    }
    data = {"name": [], "effect": []}
    city='Trondheim'
    venue_list = trondheim_venues
    regressors_to_add = []
    for venue in trondheim_venues:
        # for venue in karl_johan_venues:
        venue_df = fetch_events("Trondheim", venue,city)
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

    def calculate_days(df, last_working_day):
        # Convert 'ds' column to datetime if it's not already
        df["ds"] = pd.to_datetime(df["ds"])

        # Convert last_working_day list to datetime
        last_working_day = pd.to_datetime(pd.Series(last_working_day))

        df["days_since_last"] = df["ds"].apply(
            lambda x: min([abs(x - y).days for y in last_working_day if x >= y],default=0)
        )
        df["days_until_next"] = df["ds"].apply(
            lambda x: min([abs(x - y).days for y in last_working_day if x <= y],default=0)
        )

        # Set 'days_since_last' and 'days_until_next' to 0 for days that are not within the -5 to +5 range
        df.loc[df["days_since_last"] > 5, "days_since_last"] = 0

        return df

    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
    df = calculate_days(df, last_working_day)

    # create daily seasonality column setting a number for each day of the week, to be used later
    # Create a Boolean column for each weekday
    for weekday in range(7):
        df[f"weekday_{weekday}"] = df["ds"].dt.weekday == weekday


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
            yearly_seasonality=5,
            daily_seasonality=False,
            changepoint_prior_scale=0.5,
            seasonality_prior_scale=0.4,# changepoint_prior_scale=0.5,
            # seasonality_prior_scale=0.4,
        )
    for event_df, regressor_name in regressors_to_add:
        if "event" in event_df.columns:
            # m.add_regressor(regressor_name)
            m.add_regressor(regressor_name + '_good_weather')
            m.add_regressor(regressor_name + '_bad_weather')
            m.add_regressor(regressor_name + '_normal_weather')
    
    m.add_regressor("custom_regressor")
    m.add_seasonality(
        name="covid_restriction_christmas",
        period=7,
        fourier_order=1000,
        condition_name="covid_restriction_christmas",
    )
    m.add_seasonality(
        name="covid_loose_fall21",
        period=7,
        fourier_order=3,
        condition_name="covid_loose_fall21",
    )

    m.add_seasonality(
        name="christmas_shopping",
        period=7,
        fourier_order=3,
        condition_name="christmas_shopping",
    )

    m.add_regressor("sunshine_amount", standardize=False)
    # m.add_regressor("rain_sum", standardize=False)
    m.add_regressor("warm_and_dry")
    m.add_regressor("opening_duration")
    m.add_regressor("heavy_rain_fall_weekend")
    m.add_regressor("heavy_rain_winter_weekday")
    m.add_regressor("heavy_rain_winter_weekend")
    m.add_regressor("non_heavy_rain_fall_weekend")

    clusters = weekly_seasonalities(df)

    # venue_list = {}

    for cluster_label, weeks in clusters.items():
        # Here, you would define the custom seasonality parameters for each cluster
        # You might want to define a custom seasonality function, or apply different parameters based on the cluster label
        seasonality_params = {
            "name": f"weekly_{cluster_label}",
            "period": 7,
            "fourier_order": 10,  # Adjust as needed
            # Other parameters may go here as needed
        }

        # Add the custom seasonality to the model
        m.add_seasonality(**seasonality_params)
    
    m.fit(df)
    future = m.make_future_dataframe(periods=60, freq="D")

    # Apply the mapping function to the dates in the future DataFrame
    def get_cluster_label(date):
        week_number = date.isocalendar().week
        for cluster_label, weeks in clusters.items():
            if week_number in weeks:
                return cluster_label
        return None  # Default if week number not found in clusters

    future["cluster_label"] = future["ds"].apply(get_cluster_label)
    future.dropna(inplace=True)

    future["sunshine_amount"] = merged_data["sunshine_amount"]
    future["fellesferie"] = future["ds"].apply(is_fellesferie)
    future["is_may"] = future["ds"].apply(is_may)
    future["covid_restriction_christmas"] = future["ds"].apply(
        is_covid_restriction_christmas
    )
    future["fall_start"] = future["ds"].apply(is_fall_start)
    future["covid_loose_fall21"] = future["ds"].apply(is_covid_loose_fall21)
    future["christmas_shopping"] = future["ds"].apply(is_christmas_shopping)
    future["christmas_shopping"] = future["ds"].apply(is_christmas_shopping)
    future = add_opening_hours(future,"Trondheim",12,17)

    future["rain_sum"] = merged_data["rain_sum"]
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

    future = warm_dry_weather_spring_fss(future)
    future = heavy_rain_fall_weekend_future(future)
    future = heavy_rain_winter_weekday_future(future)
    future = heavy_rain_winter_weekend_future(future)
    future = non_heavy_rain_fall_weekend_future(future)
    
    future["ds"] = pd.to_datetime(future["ds"])
    future_date_mask = (future["ds"] >= start_date) & (future["ds"] <= end_date)
    future["week_number"] = future["ds"].dt.isocalendar().week
    future.loc[future_date_mask, "custom_regressor"] = future.loc[
        future_date_mask, "week_number"
    ].apply(custom_regressor)
    future.loc[~future_date_mask, "custom_regressor"] = 0

    if prediction_category != "hour":
        future["ds"] = future["ds"].dt.date
    future.fillna(0, inplace=True)
    event_holidays= pd.concat(objs=[event_holidays, holidays], ignore_index=True)
    return m, future, df,event_holidays, venue_list

def location_function(prediction_category,restaurant,merged_data,historical_data,future_data):
    return trondheim(prediction_category,restaurant,merged_data,historical_data,future_data)
