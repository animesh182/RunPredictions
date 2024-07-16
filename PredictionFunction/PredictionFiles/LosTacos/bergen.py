import pandas as pd
from prophet import Prophet
from PredictionFunction.Datasets.OpeningHours.lostacos_opening_hours import restaurant_opening_hours
from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    last_working_day,
    fifteenth_working_days,
)
import logging
from PredictionFunction.Datasets.Regressors.general_regressors import( 
    is_fall_start,
    is_fellesferie,
    is_first_two_weeks_january_21,
    is_specific_month
    )
from PredictionFunction.utils.utils import calculate_days_30, early_semester, calculate_days_15, custom_regressor

from PredictionFunction.Datasets.Holidays.LosTacos.Restaurants.bergen_holidays import (
    # pre_christmas,
    pre_christmas_covid21,
    weekendmiddec_21covid,
    # firstweek_jan,
    # new_years_day,
    fadder_week,
    # pinse,
    # himmelfart,
    military_excercise,
    helg_før_fellesferie,
    closed,
    july_closed,
    unknown_outliers,
    covid_christmas21_startjan22,
    bergen_pride
)
from PredictionFunction.Datasets.Holidays.LosTacos.common_holidays import (
    first_may,
    firstweek_jan,
    new_years_day,
    pinse,
    himmelfart,
    christmas,
    new_year_romjul,
    seventeenth_may,
    easter,
)
from PredictionFunction.Datasets.Regressors.weather_regressors import(
    warm_dry_weather_spring,
    warm_and_dry_future,
    # heavy_rain_fall_weekday, does not have significant effect value : -481.92
    # heavy_rain_fall_weekday_future,
    # heavy_rain_fall_weekend, value : 774.36
    # heavy_rain_fall_weekend_future,
    # heavy_rain_winter_weekday, -905.903
    # heavy_rain_winter_weekday_future,
    heavy_rain_winter_weekend,
    heavy_rain_winter_weekend_future,
    # heavy_rain_spring_weekday, value -1107.74
    # heavy_rain_spring_weekday_future,
    heavy_rain_spring_weekend,
    heavy_rain_spring_weekend_future,
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


def bergen(prediction_category,restaurant,merged_data,historical_data,future_data):
    # Group data in dataset by date to prepare it
    event_holidays=pd.DataFrame()
    sales_data_df = historical_data

    sales_data_df["date"] = pd.to_datetime(sales_data_df["date"])
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
    df = warm_dry_weather_spring(df)
    #df = heavy_rain_fall_weekday(df)
    #df = heavy_rain_fall_weekend(df)
    #df = heavy_rain_winter_weekday(df)
    df = heavy_rain_winter_weekend(df)
    #df = heavy_rain_spring_weekday(df)
    df = heavy_rain_spring_weekend(df)
    df = non_heavy_rain_fall_weekend(df)
    df = add_opening_hours(df, "Bergen",12, 17)

    m = Prophet()

    ### Holidays and other repeating outliers
    m.add_country_holidays(country_name="NO")

    holidays = pd.concat(
        (   
            christmas,
            # pre_christmas,
            new_year_romjul,
            pre_christmas_covid21,
            covid_christmas21_startjan22,
            weekendmiddec_21covid,
            new_years_day,
            firstweek_jan,
            fadder_week,
            first_may,
            easter,
            seventeenth_may,
            pinse,
            military_excercise,
            helg_før_fellesferie,
            himmelfart,
            closed,
            unknown_outliers,
            july_closed,
            bergen_pride
        )
    )

    # Different weekly seasonality for 2 weeks in august related to starting fall semester/work
    # FALL_START_DATES = {
    #     2022: {"start": "2022-08-08", "end": "2022-08-21"},
    #     2023: {"start": "2023-08-07", "end": "2023-08-20"},
    #     # Add more years and their respective dates as needed
    # }


    df["fall_start"] = df["ds"].apply(is_fall_start)
    df["is_fellesferie"] = df["ds"].apply(is_fellesferie)
    df["is_specific_month"] = df["ds"].apply(is_specific_month)

    bergen_venues = {
        "Det Akademiske Kvarter","Ole Bull Scene, Bergen","USF Verftet","Forum Scene","Lille Ole Bull","Norges Handelshøyskoles","Bergenhus Festning","Bergen","Grieghallen","Ricks Theatre",
    }
    
    venue_list = bergen_venues
    regressors_to_add = []
    for venue in bergen_venues:
        venue_df = fetch_events("Bergen", venue)  # Assuming you have a function Events_dict()
        event_holidays = pd.concat(objs=[event_holidays, venue_df], ignore_index=True)
        # print(f'{venue}: {venue_df.columns}')
        if 'name' in venue_df.columns:
            venue_df = venue_df.drop_duplicates('date')
            venue_df["date"] = pd.to_datetime(venue_df["date"])
            venue_df = venue_df.rename(columns={"date": "ds"})
            venue_df["ds"] = pd.to_datetime(venue_df["ds"])
            venue_df = venue_df[["ds", "name"]]
            venue_df.columns = ["ds", "event"]
            dataframe_name = venue.lower().replace(" ", "_").replace(",", "")
            venue_df[dataframe_name] = 1
            df = pd.merge(df, venue_df, how="left", on="ds", suffixes=('', '_venue'))
            df = is_event_with_good_weather(df,dataframe_name)
            df = is_event_with_bad_weather(df,dataframe_name)
            df = is_event_with_normal_weather(df,dataframe_name)
            df[dataframe_name].fillna(0, inplace=True)
            regressors_to_add.append((venue_df, dataframe_name))  # Append venue_df along with venue name for regressor addition
        else:
            holidays = pd.concat(objs=[holidays, venue_df], ignore_index=True)

    event_holidays= pd.concat(objs=[event_holidays, holidays], ignore_index=True)
    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
    # df = calculate_days_30(df, fifteenth_working_days)

    # def calculate_days_15(df, fifteenth_working_days):
    #     # Convert 'ds' column to datetime if it's not already
    #     df["ds"] = pd.to_datetime(df["ds"])

    #     # Convert last_working_day list to datetime
    #     fifteenth_working_days = pd.to_datetime(pd.Series(fifteenth_working_days))

    #     df["days_since_last_15"] = df["ds"].apply(
    #         lambda x: min([abs(x - y).days for y in fifteenth_working_days if x >= y])
    #     )
    #     df["days_until_next_15"] = df["ds"].apply(
    #         lambda x: min(
    #             [abs(x - y).days for y in fifteenth_working_days if x <= y],
    #             default=None,  # Set a default value in case the list is empty
    #         )
    #     )

    #     # Set 'days_since_last' and 'days_until_next' to 0 for days that are not within the -5 to +5 range
    #     df.loc[df["days_since_last_15"] > 5, "days_since_last_15"] = 0
    #     df.loc[df["days_until_next_15"] > 5, "days_until_next_15"] = 0

    #     return df

    # The training DataFrame (df) should also include 'days_since_last' and 'days_until_next' columns.
   
   
    #df = calculate_days_15(df, fifteenth_working_days)

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
            yearly_seasonality=True,
            daily_seasonality=False,
            changepoint_prior_scale=0.1,
        )

    # Add the payday columns as regressors
    # m.add_regressor("days_since_last_30")
    # m.add_regressor("days_until_next_30")

    # m.add_regressor("days_since_last_15")
    # m.add_regressor("days_until_next_15")

    # Add weather parameters as regressors
    # print(parameter)
    # for parameter in weather_parameters.keys():
    #    m.add_regressor(parameter)

    # Add high sales from after fadderuke in august until october 20th (appr). This represents that students go out
    # partying in the beginning of the semester but that this trend is decreasing from a maximum point

    # setting the dates for early semester students going out trend - 2022
    start_date_early_semester = pd.to_datetime("2022-08-21")
    end_date_early_semester = pd.to_datetime("2022-10-20")
    max_value = 100

    params = (max_value, start_date_early_semester, end_date_early_semester)
    df["students_early_semester"] = df["ds"].apply(lambda x: early_semester(x, params))
    m.add_regressor("students_early_semester")
    m.add_regressor("warm_and_dry")
    #m.add_regressor("heavy_rain_fall_weekday")
    #m.add_regressor("heavy_rain_fall_weekend")
    #m.add_regressor("heavy_rain_winter_weekday")
    m.add_regressor("heavy_rain_winter_weekend")
    #m.add_regressor("heavy_rain_spring_weekday")
    m.add_regressor("heavy_rain_spring_weekend")
    m.add_regressor("non_heavy_rain_fall_weekend")
    m.add_regressor("sunshine_amount", standardize=False)
    m.add_regressor("opening_duration")

    for event_df, regressor_name in regressors_to_add:
        if 'event' in event_df.columns:
            # m.add_regressor(regressor_name)
            m.add_regressor(regressor_name + '_good_weather')
            m.add_regressor(regressor_name + '_bad_weather')
            m.add_regressor(regressor_name + '_normal_weather')


    # setting the dates for early semester students goinf out trend/cutting covid restrictions at the same time - 2021
    # start_date_early_semester_21 = pd.to_datetime('2021-09-26')
    # end_date_early_semester_21 = pd.to_datetime('2021-11-21')
    # max_value_21 = 100
    #
    # def early_semester_21(ds, params):
    #     max_value_21, start_date_early_semester_21, end_date_early_semester_21 = params
    #     date = pd.to_datetime(ds)
    #     if start_date_early_semester_21 <= date <= end_date_early_semester_21:
    #         duration = (end_date_early_semester_21 - start_date_early_semester_21).days
    #         elapsed_days = (date - start_date_early_semester_21).days
    #         return max_value * (1 - (elapsed_days / duration))
    #     else:
    #         return 0
    #
    # params_21 = (max_value_21, start_date_early_semester_21, end_date_early_semester_21)
    # df['students_early_semester_21'] = df['ds'].apply(lambda x: early_semester_21(x, params_21))
    # m.add_regressor('students_early_semester_21')

    ### Conditional seasonality - weekly

    # df["fellesferie"] = df["ds"].apply(is_fellesferie)
    # df['not_fellesferie'] = ~df['ds'].apply(is_fellesferie)

    # m.add_seasonality(name='weekly_not_fellesferie', period=7, fourier_order=3, condition_name='not_fellesferie')

    m.add_seasonality(
        name="weekly_fall_start", period=7, fourier_order=3, condition_name="fall_start"
    )


    m.add_seasonality(
        name="is_fellesferie", period=30.5, fourier_order=5, condition_name="is_fellesferie"
    )
    m.add_seasonality(
        name="is_specific_month", period=30.5, fourier_order=5, condition_name="is_specific_month"
    )

    m.add_seasonality(name='monthly', period=30.5, fourier_order=5)

    # add function for is_first_two_weeks_january

    # df["first_two_weeks_january_21"] = df["ds"].apply(is_first_two_weeks_january_21)
    # df['not_first_two_weeks_january_21'] = ~df['ds'].apply(is_first_two_weeks_january_21)

    # m.add_seasonality(
    #     name="weekly_first_two_weeks_january_21",
    #     period=7,
    #     fourier_order=3,
    #     condition_name="first_two_weeks_january_21",
    # )
    # m.add_seasonality(name='weekly_not_first_two_weeks_january_21', period=7, fourier_order=3, condition_name='not_first_two_weeks_january_21')
    m.fit(df)


    future = m.make_future_dataframe(periods=60, freq="D")


    # add the last working day and the +/- 5 days
    #future = calculate_days_30(future, last_working_day)
    
    
    #future = calculate_days_15(future, fifteenth_working_days)

    params = (max_value, start_date_early_semester, end_date_early_semester)
    future["students_early_semester"] = future["ds"].apply(
        lambda x: early_semester(x, params)
    )
    ## Add conditional seasonality
    future["fall_start"] = future["ds"].apply(is_fall_start)
    future["is_fellesferie"] = future["ds"].apply(is_fellesferie)
    future["is_specific_month"] = future["ds"].apply(is_specific_month)
    # future['not_fellesferie'] = ~future['ds'].apply(is_fellesferie)
    future["early_semester_week"] = future["ds"].apply(
        lambda x: early_semester(x, params)
    )
    # future["first_two_weeks_january_21"] = future["ds"].apply(
    #     is_first_two_weeks_january_21
    # )
    # # future['not_first_two_weeks_january_21'] = ~future['ds'].apply(is_first_two_weeks_january_21)
    # future["first_two_weeks_january_21"] = future["ds"].apply(
    #     is_first_two_weeks_january_21
    # )
    # Add relevant weather columns to the future df
    future["rain_sum"] = merged_data["rain_sum"]
    future["sunshine_amount"] = merged_data["sunshine_amount"]
    future["windspeed"] = merged_data["windspeed"]
    future["air_temperature"] = merged_data["air_temperature"]
    
    future["fall_start"] = future["ds"].apply(is_fall_start)
    for event_df, event_column in regressors_to_add:
        if 'event' in event_df.columns:
            event_df= event_df.drop_duplicates('ds')
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

    if prediction_category != "hour":
        future["ds"] = future["ds"].dt.date

    future.fillna(
            {"sunshine_amount": 0, "rain_sum": 0, "windspeed": 0, "air_temperature": 0},
            inplace=True,
        )
    future = add_opening_hours(future, "Bergen", 12,17)
    future = warm_and_dry_future(future)
    #future = heavy_rain_fall_weekday_future(future)
    #future = heavy_rain_fall_weekend_future(future)
    #future = heavy_rain_winter_weekday_future(future)
    future = heavy_rain_winter_weekend_future(future)
    #future = heavy_rain_spring_weekday_future(future)
    future = heavy_rain_spring_weekend_future(future)
    future = non_heavy_rain_fall_weekend_future(future)
    future.fillna(0, inplace=True)
    return m, future, df,event_holidays, venue_list


def location_function(prediction_category,restaurant,merged_data,historical_data,future_data):
    return bergen(prediction_category,restaurant,merged_data,historical_data,future_data)