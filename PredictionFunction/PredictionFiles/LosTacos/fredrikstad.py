import pandas as pd
import numpy as np
from prophet import Prophet
from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    last_working_day,
    fifteenth_working_days,
)
from PredictionFunction.utils.utils import (
    calculate_days_30,
    calculate_days_15,
    custom_regressor,
    is_closed,
)
from PredictionFunction.Datasets.Regressors.general_regressors import (
    is_specific_month,
    is_covid_restriction_christmas,
    is_fall_start,
    is_christmas_shopping,
    is_fellesferie,
)

from PredictionFunction.Datasets.OpeningHours.lostacos_opening_hours import (
    restaurant_opening_hours,
)
from PredictionFunction.Datasets.Regressors.weather_regressors import (
    # warm_dry_weather_spring,
    warm_and_dry_future,
    heavy_rain_fall_weekday,
    heavy_rain_fall_weekday_future,
    heavy_rain_fall_weekend,
    heavy_rain_fall_weekend_future,
    # heavy_rain_winter_weekday,
    # heavy_rain_winter_weekday_future,
    # heavy_rain_winter_weekend,
    # heavy_rain_winter_weekend_future,
    heavy_rain_spring_weekday,
    heavy_rain_spring_weekday_future,
    heavy_rain_spring_weekend,
    heavy_rain_spring_weekend_future,
    warm_dry_weather_spring,
    # non_heavy_rain_fall_weekend,
    # non_heavy_rain_fall_weekend_future,
)
from PredictionFunction.Datasets.Regressors.event_weather_regressors import (
    is_event_with_bad_weather,
    is_event_with_good_weather,
    is_event_with_normal_weather
)
from PredictionFunction.Datasets.Holidays.LosTacos.Restaurants.fredrikstad_holidays import (
    fadder_week,
    idyll,
    closed_days,
    black_friday,
    feb_closed
)

from PredictionFunction.Datasets.Holidays.LosTacos.common_holidays import (
    first_may,
    firstweek_jan,
    new_years_day,
    pinse,
    himmelfart,
    hostferie_sor_ostlandet_weekdays,
    hostferie_sor_ostlandet_weekdend,
    christmas_day,
    seventeenth_may,
    easter,
    new_year_romjul
)
from PredictionFunction.utils.openinghours import add_opening_hours
from PredictionFunction.utils.fetch_events import fetch_events


def fredrikstad(
    prediction_category, restaurant, merged_data, historical_data, future_data
):
    event_holidays = pd.DataFrame()
    sales_data_df = historical_data
    sales_data_df = sales_data_df.rename(columns={"date": "ds"})

    future_data = future_data.rename(columns={"date": "ds"})

    merged_data = merged_data.rename(columns={"date": "ds"})
    sales_data_df["ds"] = pd.to_datetime(sales_data_df["ds"])
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
    df = warm_dry_weather_spring(df)
    df = heavy_rain_fall_weekday(df)
    df = heavy_rain_fall_weekend(df)
    # df = heavy_rain_winter_weekday(df)
    # df = heavy_rain_winter_weekend(df)
    df = heavy_rain_spring_weekday(df)
    df = heavy_rain_spring_weekend(df)
    df = add_opening_hours(df, "Fredrikstad", 11, 16)
    # df = non_heavy_rain_fall_weekend(df)

    m = Prophet()

    ### Holidays and other repeating outliers
    m.add_country_holidays(country_name="NO")


    holidays = pd.concat(
        (
            christmas_day,
            new_year_romjul,
            new_years_day,
            firstweek_jan,
            fadder_week,
            first_may,
            easter,
            seventeenth_may,
            pinse,
            himmelfart,
            closed_days,
            idyll,
            black_friday,
            hostferie_sor_ostlandet_weekdend,
            hostferie_sor_ostlandet_weekdays,
            feb_closed
        )
    )

    # Add regressor that captures payday effect before and after the payday
    # Let's create additional regressors for the days before, on and after payday
    df["before_payday"] = 0
    df["on_payday"] = 0
    df["after_payday"] = 0

    # Define number of days before payday to start linear decrease and after payday to end exponential decrease
    n_days_before = 4
    n_days_after = 4

    # Update regressor columns
    for i in range(len(df)):
        for pay_day in last_working_day:
            pay_day = pd.to_datetime(pay_day)  # Convert pay_day to datetime
            # Check if date is in the window before payday
            if (
                df.loc[i, "ds"] > (pay_day - pd.Timedelta(days=n_days_before))
                and df.loc[i, "ds"] < pay_day
            ):
                df.loc[i, "before_payday"] = (
                    pay_day - df.loc[i, "ds"]
                ).days / n_days_before
            # Check if date is on payday
            elif df.loc[i, "ds"] == pay_day:
                df.loc[i, "on_payday"] = 1
            # Check if date is in the window after payday
            elif df.loc[i, "ds"] > pay_day and df.loc[i, "ds"] < (
                pay_day + pd.Timedelta(days=n_days_after)
            ):
                df.loc[i, "after_payday"] = np.exp(
                    -(df.loc[i, "ds"] - pay_day).days
                )  # exponential decay

    ### Add weather parameters

    # m.add_regressor('precipitation_hours', mode='additive')
    # m.add_regressor('apparent_temperature_mean')
    # m.add_regressor('rain_sum')
    # m.add_regressor('snowfall_sum')
    # m.add_regressor('windspeed_10m_max')

    # Add custom monthly seasonalities for a specific month

    df["is_specific_month"] = df["ds"].apply(is_specific_month)
    df["is_fellesferie"] = df["ds"].apply(is_fellesferie)
    fredrikstad_venues = {  
                            "Tollbodplassen"
                            "Fredrikstad domkirke"
                            "City scene"
                            "Fredrikstad Stadion"
                            "Alibi Fredrikstad"
                            "Kulturkirken Gamle Fredrikstad"
                            "City Scene Fredrikstad"
                            }
    venue_list = fredrikstad_venues
    city='Fredrikstad'
    data = {"name": [], "effect": []}
    regressors_to_add = []
    for venue in fredrikstad_venues:
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
    # Define a function to check if the date is within the period of heavy COVID restrictions

    # Add new columns in your dataframe to indicate if a date is within or outside the restrictions period
    df["covid_restriction_christmas"] = df["ds"].apply(is_covid_restriction_christmas)
    df["no_covid_restriction_christmas"] = ~df["ds"].apply(
        is_covid_restriction_christmas
    )

    # was closed for the following date interval

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

    # Define a function to calculate the custom regressor value based on the week number

    # Calculate the custom regressor values for the specific date interval
    df.loc[date_mask, "custom_regressor"] = df.loc[date_mask, "week_number"].apply(
        custom_regressor
    )

    # Fill the custom regressor with zeros for the rows outside the specific date interval
    df.loc[~date_mask, "custom_regressor"] = 0

    # Different weekly seasonality for 2 weeks in august related to starting fall semester/work
    FALL_START_DATES = {
        2022: {"start": "2022-08-08", "end": "2022-08-21"},
        2023: {"start": "2023-08-07", "end": "2023-08-20"},
        # Add more years and their respective dates as needed
    }

    df["fall_start"] = df["ds"].apply(is_fall_start)
    # df['not_fall_start'] = ~df['ds'].apply(is_fall_start)

    df["christmas_shopping"] = df["ds"].apply(is_christmas_shopping)
    # df['not_christmas_shopping'] = ~df['ds'].apply(is_christmas_shopping)

    ## calculating the paydays and the days before and after. Used in regressions

    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
    # df = calculate_days_30(df, fifteenth_working_days)

    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
    # df = calculate_days_15(df, fifteenth_working_days)

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
            yearly_seasonality=5,
            daily_seasonality=False,
            changepoint_prior_scale=0.1,
        )
    for event_df, regressor_name in regressors_to_add:
        if "event" in event_df.columns:
            # m.add_regressor(regressor_name)
            m.add_regressor(regressor_name + '_good_weather')
            m.add_regressor(regressor_name + '_bad_weather')
            m.add_regressor(regressor_name + '_normal_weather')

    # Add the payday columns as regressors
    # m.add_regressor("days_since_last_30")

    # m.add_regressor("days_since_last_15")
    # m.add_regressor("days_until_next_15")

    # m.add_regressor("warm_and_dry")
    m.add_regressor("heavy_rain_fall_weekday")
    m.add_regressor("heavy_rain_fall_weekend")
    # m.add_regressor("heavy_rain_winter_weekday")
    # m.add_regressor("heavy_rain_winter_weekend")
    m.add_regressor("heavy_rain_spring_weekday")
    m.add_regressor("heavy_rain_spring_weekend")
    # m.add_regressor("non_heavy_rain_fall_weekend")
    m.add_regressor("custom_regressor")
    # m.add_regressor('covid_restriction')
    m.add_regressor("closed_jan")
    m.add_regressor("opening_duration")
    m.add_regressor("sunshine_amount")
    m.add_regressor("rain_sum")

    m.add_seasonality(name="monthly", period=30.5, fourier_order=5)
    m.add_seasonality(
        name="is_specific_month",
        period=30.5,
        fourier_order=5,
        condition_name="is_specific_month",
    )
    m.add_seasonality(
        name="covid_restriction_christmas",
        period=7,
        fourier_order=1000,
        condition_name="covid_restriction_christmas",
    )
    # m.add_seasonality(name='no_covid_restriction_christmas', period=7, fourier_order=3,
    #                  condition_name='no_covid_restriction_christmas')

    m.add_seasonality(
        name="weekly_fall_start", period=7, fourier_order=3, condition_name="fall_start"
    )
    # m.add_seasonality(name='weekly_not_fall_start', period=7, fourier_order=3,
    #                  condition_name='not_fall_start')
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
    m.fit(df)
    # m.add_seasonality(name='not_christmas_shopping', period=7, fourier_order=3,
    #                  condition_name='not_christmas_shopping')

    # Add the conditional regressor to the model

    future = m.make_future_dataframe(periods=60, freq="D")

    # add the last working day and the +/- 5 days
    # future = calculate_days_30(future, last_working_day)
    # future = calculate_days_15(future, fifteenth_working_days)

    future["sunshine_amount"] = merged_data["sunshine_amount"]

    future["covid_restriction_christmas"] = future["ds"].apply(
        is_covid_restriction_christmas
    )
    # future['no_covid_restriction_christmas'] = ~future['ds'].apply(is_covid_restriction_christmas)

    future["fall_start"] = future["ds"].apply(is_fall_start)
    # future['not_fall_start'] = ~future['ds'].apply(is_fall_start)

    future["christmas_shopping"] = future["ds"].apply(is_christmas_shopping)
    future["is_fellesferie"] = future["ds"].apply(is_fellesferie)
    # future['not_christmas_shopping'] = ~future['ds'].apply(is_christmas_shopping)

    future["is_specific_month"] = future["ds"].apply(is_specific_month)
    # Calculate the custom regressor values for the future dates
    future["ds"] = pd.to_datetime(future["ds"])
    future_date_mask = (future["ds"] >= start_date) & (future["ds"] <= end_date)
    future["week_number"] = future["ds"].dt.isocalendar().week
    future.loc[future_date_mask, "custom_regressor"] = future.loc[
        future_date_mask, "week_number"
    ].apply(custom_regressor)
    future.loc[~future_date_mask, "custom_regressor"] = 0
    future["closed_jan"] = future["ds"].apply(is_closed)
    if prediction_category != "hour":
        future["ds"] = future["ds"].dt.date
    # Add relevant weather columns to the future df
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
    future = warm_and_dry_future(future)
    future = heavy_rain_fall_weekday_future(future)
    future = heavy_rain_fall_weekend_future(future)
    # future = heavy_rain_winter_weekday_future(future)
    # future = heavy_rain_winter_weekend_future(future)
    future = heavy_rain_spring_weekday_future(future)
    future = heavy_rain_spring_weekend_future(future)
    future = add_opening_hours(future, "Fredrikstad", 11, 16)
    # future = non_heavy_rain_fall_weekend_future(future)

    return m, future, df, event_holidays, venue_list


def location_function(
    prediction_category, restaurant, merged_data, historical_data, future_data
):
    return fredrikstad(
        prediction_category, restaurant, merged_data, historical_data, future_data
    )
