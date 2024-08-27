# import datetime
import uuid
import logging
import pandas as pd
from PredictionFunction.PredictionSaver.saveDailyPredictions import (
    save_daily_predictions,
)
from PredictionFunction.PredictionSaver.saveHolidayParams import save_holiday_params
from PredictionFunction.utils.fetch_events import fetch_events
from PredictionFunction.utils.constants import opening_hours_dict
import psycopg2
from PredictionFunction.utils.params import params, prod_params
from datetime import datetime
from PredictionFunction.meta_tables import data
import numpy as np
from PredictionFunction.utils.constants import holiday_parameter_type_categorization,holiday_names_negative
from PredictionFunction.utils.trondheim_events import trondheim_events
from PredictionFunction.utils.openinghours import get_opening_closing_hours


def save_to_db(
    forecast_df, company, restaurant, prediction_category, event_holidays, end_date , venues_list
):
    # end_date = datetime.now().strftime("%Y-%m-%d")
    logging.info(f"started for {restaurant} in save_to_db")
    # forecast_df.to_csv("forecast.csv")
    # end_date = "2024-04-27"

    unwanted_columns = [
        "_lower",
        "_upper",
        "Unnamed",
        "custom_regressor",
        "extra_regressors_additive",
        "trend",
        "additive_terms",
        "yearly",
        "index",
        "0",
        "holidays",
        "weekly_1",
        "weekly_2",
        "weekly_3",
        "weekly_4",
        "weekly_5",
        "weekly_6",
        "weekly",
        "monthly",
    ]
    filtered_columns = [
        col
        for col in forecast_df.columns
        if not any(unwanted in col for unwanted in unwanted_columns)
    ]
    filtered_df = forecast_df[filtered_columns]
    filtered_df.loc[filtered_df["yhat"] < 0, "yhat"] = 0
    # filtered_df = forecast_df

    if prediction_category == "day":
        restaurant_name = restaurant
        with psycopg2.connect(**prod_params) as conn:
            with conn.cursor() as cursor:
                cursor.execute(""" select id from public."accounts_restaurant" where name=%s """,[restaurant_name])
                restaurant_id= cursor.fetchone()[0]
                logging.info(f'restaurant id is : {restaurant_id}')
                opening_hour_query = """
                        SELECT *
                        FROM public."accounts_openinghours"
                        WHERE restaurant_id = %s
                    """
                opening_hours_df = pd.read_sql_query(opening_hour_query,conn,params=[restaurant_id])
  
        for index, row in filtered_df.iterrows():
            # date_obj = datetime.strptime(row["ds"], "%Y-%m-%d")
            date_obj = pd.to_datetime(row['ds'])
            day_type = int(date_obj.strftime("%w"))  # 5 and 6 are Saturday and Sunday
            start,end = get_opening_closing_hours(opening_hours_df,day_type,date_obj)
            if start > end:
                duration = (24 - start) + end
            elif start == end:
                duration = 0
                filtered_df.at[index, "yhat"] = 0
            else:
                duration = end - start
            filtered_df.at[index, "duration"] = duration
            common_duration = filtered_df["duration"].value_counts().idxmax()
            filtered_df.at[index, "common_duration"] = common_duration

        normal_hour = opening_hours_dict[restaurant_name]["normal_hours"]
        normal_hour_2 = opening_hours_dict[restaurant_name]["special_hours"]
        filtered_df["special_opening_hour"] = 0
        filtered_df["new_yhat"] = filtered_df["yhat"]

        for index, row in filtered_df.iterrows():
            if (row['duration'] not in normal_hour) and (row['duration'] not in normal_hour_2):
                duration_scale = (
                    row["duration"] / row["common_duration"]
                )  # Scaling based on common duration and normal hour
                logging.info(duration_scale)
                filtered_df.at[index, "new_yhat"] = row["yhat"] * duration_scale * 0.8
                filtered_df.at[index, "opening_duration"] = 0
                filtered_df["special_opening_hour"] = filtered_df[
                    "special_opening_hour"
                ].fillna(0)
            else:
                filtered_df.at[index, "new_yhat"] = row[
                    "yhat"
                ]  # Keeping yhat as it is for normal or special hours

        filtered_df["new_yhat"] = filtered_df["new_yhat"].fillna(filtered_df["yhat"])
        filtered_df["special_opening_hour"] = (
            filtered_df["new_yhat"] - filtered_df["yhat"]
        )
        filtered_df.drop(["yhat"], axis=1, inplace=True)
        filtered_df["yhat"] = filtered_df["new_yhat"]
        filtered_df.drop(["new_yhat"], axis=1, inplace=True)
        filtered_df.drop(["duration", "common_duration"], axis=1, inplace=True)
        filtered_df["opening_duration"].fillna(0, inplace=True)

    if prediction_category == "day":
        if restaurant not in ["Trondheim"]:
            filtered_df.loc[
                (filtered_df["opening_duration"] < 0)
                & (filtered_df["historical_sale"] <= 0)
                & (pd.to_datetime(filtered_df["ds"]) < pd.to_datetime(end_date)),
                "yhat",
            ] = 0
        filtered_df.loc[
            (filtered_df["historical_sale"] <= 0)
            & (pd.to_datetime(filtered_df["ds"]) < pd.to_datetime(end_date)),
            "yhat",
        ] = 0
        if (
            "opening_duration" in filtered_df.columns
            and "students_early_semester" in filtered_df.columns
        ):
            filtered_df.drop(
                [
                    # "opening_duration",
                    "students_early_semester"
                ],
                axis=1,
                inplace=True,
            )
            # for index, row in event_holidays_trondheim.iterrows():
            #     holiday_params = HolidayParameters.objects.create(
            #         prediction=None,
            #         name=row["event_names"],
            #         date=row["event_date"],
            #         restaurant="Trondheim",
            #         company="Los Tacos",
            #         parent_restaurant=None,
            #         effect = 0
            #     )
        filtered_df = filtered_df[filtered_df["ds"] >= datetime.now()]
        concert_dictionary = {}
        valid_concerts = []
        all_venues = venues_list
        if restaurant_name in [
            "Oslo Storo",
            "Oslo City",
            "Oslo Torggata",
            "Karl Johan",
            "Oslo Lokka",
            "Oslo Steen_Strom",
            "Oslo Smestad",
            "Alexander Kielland",
            "Bjørvika",
            "Restaurantdrift AS"
        ]:  
            event_restaurant= 'Oslo Torggata'
            city= 'Oslo'
        if restaurant_name in [
            "Stavanger",
            "Sandnes",
            "Restaurant",
            "Fisketorget Utsalg",
        ]:
            event_restaurant= 'Stavanger'
            city='Stavanger'
        if restaurant_name in ["Bergen","Åsane Storsenter"]:
            event_restaurant= 'Bergen'
            city='Bergen'
        if restaurant_name in ["Fredrikstad"]:
            event_restaurant= 'Fredrikstad'
            city='Fredrikstad'
        if restaurant_name in ["Trondheim"]:
            event_restaurant= 'Trondheim'
            city='Trondheim'
        # with psycopg2.connect(**prod_params) as conn:
        #     with conn.cursor() as cursor:
        #         cursor.execute(
        #             """ select id from public."accounts_city" where name ='Oslo' """
        #         )
        #         city_uuid = cursor.fetchone()[0]
        #         cursor.execute(
        #             ' select name from public."Predictions_location" where cities_id = %s ',
        #             [city_uuid],
        #         )
        #         oslo_venues = cursor.fetchall()
        for venue in all_venues:
            dataframe_name = venue[0].lower().replace(" ", "_").replace(",", "")
            dataframe = fetch_events(event_restaurant, venue, city)
            concert_dictionary[dataframe_name + '_good_weather'] = dataframe 
            concert_dictionary[dataframe_name + '_bad_weather'] = dataframe 
            concert_dictionary[dataframe_name + '_normal_weather'] = dataframe 

            valid_concerts.append(dataframe_name + '_good_weather')
            valid_concerts.append(dataframe_name + '_bad_weather')
            valid_concerts.append(dataframe_name + '_normal_weather')
            logging.info(venue)
            # concert_dictionary[dataframe_name] = dataframe
            # valid_concerts.append(dataframe_name)
        for venue in all_venues:
            dataframe_name = venue.lower().replace(" ", "_").replace(",", "")
            dataframe = pd.DataFrame(fetch_events(event_restaurant, venue,city))
            concert_dictionary[dataframe_name] = dataframe
            valid_concerts.append(dataframe_name)
        # if restaurant_name in [
        #     "Stavanger",
        #     "Sandnes",
        #     "Restaurant",
        #     "Fisketorget Utsalg",
        # ]:
        #     with psycopg2.connect(**prod_params) as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute(
        #                 """ select id from public."accounts_city" where name ='Stavanger' """
        #             )
        #             city_uuid = cursor.fetchone()[0]
        #             cursor.execute(
        #                 ' select name from public."Predictions_location" where cities_id = %s ',
        #                 [city_uuid],
        #             )
        #             oslo_venues = cursor.fetchall()
        #     for venue in oslo_venues:
        #         dataframe_name = venue[0].lower().replace(" ", "_").replace(",", "")
        #         dataframe = fetch_events("Stavanger", venue)
        #         logging.info(venue)
        #         concert_dictionary[dataframe_name] = dataframe
        #         valid_concerts.append(dataframe_name)

        # if restaurant_name in ["Bergen"]:
        #     with psycopg2.connect(**prod_params) as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute(
        #                 """ select id from public."accounts_city" where name ='Bergen' """
        #             )
        #             city_uuid = cursor.fetchone()[0]
        #             cursor.execute(
        #                 ' select name from public."Predictions_location" where cities_id = %s ',
        #                 [city_uuid],
        #             )
        #             oslo_venues = cursor.fetchall()
        #     for venue in oslo_venues:
        #         dataframe_name = venue[0].lower().replace(" ", "_").replace(",", "")
        #         dataframe = fetch_events("Bergen", venue)
        #         logging.info(venue)
        #         concert_dictionary[dataframe_name] = dataframe
        #         valid_concerts.append(dataframe_name)

        # if restaurant_name in ["Fredrikstad"]:
        #     with psycopg2.connect(**prod_params) as conn:
        #         with conn.cursor() as cursor:
        #             cursor.execute(
        #                 """ select id from public."accounts_city" where name ='Fredrikstad' """
        #             )
        #             city_uuid = cursor.fetchone()[0]
        #             cursor.execute(
        #                 ' select name from public."Predictions_location" where cities_id = %s ',
        #                 [city_uuid],
        #             )
        #             oslo_venues = cursor.fetchall()
        #     for venue in oslo_venues:
        #         dataframe_name = venue[0].lower().replace(" ", "_").replace(",", "")
        #         dataframe = fetch_events("Fredrikstad", venue)
        #         logging.info(venue)
        #         concert_dictionary[dataframe_name] = dataframe
        #         valid_concerts.append(dataframe_name)

        # SAVE DAILY PREDICTIONS
        # prediction_data = filtered_df[['ds', 'yhat']]
        # prediction_data = prediction_data.rename(columns={"ds": "date", "yhat": "total_gross"})
        # prediction_data["date"]=pd.to_datetime(prediction_data["date"]).dt.date
        # prediction_data["company"]=company
        # prediction_data["restaurant"]=restaurant
        # prediction_data['total_gross'] = prediction_data['total_gross'].apply(lambda x: int(round(x / 500) * 500))
        # prediction_data['id'] = [uuid.uuid4() for _ in range(len(prediction_data))]
        # prediction_data['created_at']=datetime.now()
        # prediction_data['created_at'] = prediction_data['created_at'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))
        # prediction_data['total_gross'] = prediction_data['total_gross'].astype(float)
        # prediction_data['id'] = prediction_data['id'].apply(str)

        # save_daily_predictions(prediction_data,restaurant)
        # logging.info("saved daily predictions")

        # Save the holiday parameters for predictions
        # sentrum_scene_events= fetch_events(restaurant,"Sentrum Scene")
        # oslo_spektrum_events= fetch_events(restaurant,"Oslo Spektrum")
        # fornebu_events= fetch_events(restaurant,"Fornebu")
        # ulleval_events= fetch_events(restaurant,"Ulleval")

        # holiday_parameter_data = prediction_data
        # holiday_parameter_data = holiday_parameter_data.rename(columns={"yhat": "total_gross"})
        # id_vars= ['ds']
        # melted_data = pd.melt(filtered_df, id_vars=id_vars, var_name='name', value_name='effect')

        # valid_concerts = ['spektrum', 'sentrum', 'fornebu', 'ulleval']
        # concert_dictionary = {
        #     # 'spektrum': oslo_spektrum_events,
        #     'sentrum': sentrum_scene_events,
        #     # 'fornebu': fornebu_events,
        #     # 'ulleval': ulleval_events
        # }

        # --------------------------------------SAVE HOLIDAY PARAMS----------------------------------------
        restaurant_city_df = pd.DataFrame(data)
        if "Parent Restaurant" in restaurant_city_df.columns:
            parent_restaurant_series = restaurant_city_df.loc[
                restaurant_city_df["Restaurant"] == restaurant, "Parent Restaurant"
            ]
            if not parent_restaurant_series.empty:
                parent_restaurant = parent_restaurant_series.iloc[0]
        else:
            parent_restaurant = None

        # if restaurant == "Trondheim":
        #     event_holidays_trondheim = trondheim_events()
        #     event_holidays_trondheim = event_holidays_trondheim[
        #         pd.to_datetime(event_holidays_trondheim["event_date"]) >= datetime.now()
        #     ]
        #     holiday_param_insert_trondheim = """ INSERT INTO public."Predictions_holidayparameters" (id,prediction_id, name, effect, type, date, restaurant, company, parent_restaurant,created_at)
        #         VALUES (gen_random_uuid(),%s, %s, %s,'event', %s, %s, %s, %s,%s)"""
        #     with psycopg2.connect(**params) as conn:
        #         with conn.cursor() as cursor:
        #             for index, row in event_holidays_trondheim.iterrows():
        #                 prediction_id = None
        #                 event_name = row["event_names"]
        #                 event_date = row["event_date"]
        #                 restaurant = "Trondheim"
        #                 company = "Los Tacos"
        #                 parent_restaurant = parent_restaurant
        #                 effect_value = 0
        #                 created_at = datetime.now()
        #                 cursor.execute(
        #                     holiday_param_insert_trondheim,
        #                     (
        #                         prediction_id,
        #                         event_name,
        #                         effect_value,
        #                         event_date,
        #                         restaurant,
        #                         company,
        #                         parent_restaurant,
        #                         created_at,
        #                     ),
        #                 )
        #             conn.commit()
        # filtered_df.to_csv('filtered_df.csv')
        # else:
        if "holiday" in event_holidays.columns:
            event_holidays["event_names"] = event_holidays["holiday"].fillna(
                event_holidays["name"]
            )
            event_holidays["ds"] = pd.to_datetime(event_holidays["ds"])
            event_holidays["date"] = pd.to_datetime(event_holidays["date"])
            # event_holidays.to_csv("events_before.csv")
            event_holidays["event_date"] = event_holidays["date"].fillna(
                event_holidays["ds"].dt.date
            )
            event_holidays["event_date"] = (
                event_holidays["event_date"].dt.strftime("%Y-%m-%d").astype(str)
            )
        else:
            event_holidays["event_names"] = event_holidays["name"]
            event_holidays["event_date"] = pd.to_datetime(event_holidays["date"])
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cursor:
                for index, row in filtered_df.iterrows():
                    # date_obj = datetime.strptime(row["ds"], "%Y-%m-%d")
                    date_obj = row["ds"].to_pydatetime()
                    total_gross_value = round(float(row["yhat"] / 500)) * 500

                    cursor.execute(
                            """SELECT total_gross FROM public."Predictions_predictions"
                            WHERE date = %s AND restaurant = %s order by created_at desc limit 1""",
                            (date_obj.date(), restaurant)
                        )
                    existing_prediction = cursor.fetchone()

                    # If prediction exists, calculate the percentage difference
                    if existing_prediction:
                        existing_total_gross = existing_prediction[0]
                        if existing_total_gross is not None and existing_total_gross != 0:
                            percentage_difference = ((total_gross_value - existing_total_gross) / existing_total_gross) * 100
                        else:
                            percentage_difference = None
                    else:
                        percentage_difference = None
                    if percentage_difference is not None and percentage_difference > 20:
                        logging.info(f"Alert: Percentage difference for {restaurant} on {date_obj.date()} is {percentage_difference:.2f}%")
                    insert_prediction = """INSERT INTO public."Predictions_predictions" (id, date, restaurant, total_gross, created_at, company, parent_restaurant,percentage_difference)
                            VALUES (gen_random_uuid(),%s,%s,%s,%s,%s,%s,%s) RETURNING id"""
                    cursor.execute(
                        insert_prediction,
                        (
                            date_obj.date(),
                            restaurant,
                            total_gross_value,
                            datetime.now(),
                            company,
                            parent_restaurant,
                            percentage_difference
                        ),
                    )
                    prediction_id = cursor.fetchone()[0]

                    date_key = date_obj.date()
                    for name in filtered_df.columns:
                        if name in ["ds", "yhat"]:
                            continue
                        try:
                            effect_value = (
                                round(float(row[name]))
                                if row[name] not in [None, "", np.nan]
                                else 0
                            )
                        except ValueError:
                            print(
                                f"Error converting value to float for column '{name}'"
                            )
                            effect_value = 0  # Assign a default valu
                        for concert in valid_concerts:
                            if concert in name:
                                actual_concert = concert_dictionary[concert]
                                # logging.info(name)
                                if 'date' in actual_concert.columns:
                                    date_matching_df = actual_concert[
                                        actual_concert["date"] == date_key
                                    ]
                                    if not date_matching_df.empty:
                                        concert_name = date_matching_df["name"].iloc[0]
                                        name = concert_name
                                elif 'ds' in actual_concert.columns:
                                    date_matching_df = actual_concert[
                                        actual_concert["ds"] == date_key
                                    ]
                                    if not date_matching_df.empty:
                                        concert_name = date_matching_df["holiday"].iloc[0]
                                        name = concert_name
                        if (
                            effect_value > 2000
                            and name in event_holidays["event_names"].values
                        ):
                            # print(f'upper {restaurant}: {name}')

                            holiday_param_insert = """ INSERT INTO public."Predictions_holidayparameters" (id,prediction_id, name, effect, type, date, restaurant, company, parent_restaurant,created_at)
                            VALUES (gen_random_uuid(),%s, %s, %s,'event', %s, %s, %s, %s,%s)"""
                            cursor.execute(
                                holiday_param_insert,
                                (
                                    prediction_id,
                                    name,
                                    effect_value,
                                    date_obj,
                                    restaurant,
                                    company,
                                    parent_restaurant,
                                    datetime.now(),
                                ),
                            )

                        elif (
                            effect_value != 0
                            and name not in concert_dictionary
                            and name not in event_holidays["event_names"].values
                        ):
                            # print(f'lower {restaurant}: {name}')
                            try:
                                type = holiday_parameter_type_categorization[name]
                            except:
                                type = None

                            holiday_param_insert_categorized = """ INSERT INTO public."Predictions_holidayparameters" (id,prediction_id, name, effect, type, date, restaurant, company, parent_restaurant,created_at)
                            VALUES (gen_random_uuid(),%s, %s, %s,%s, %s, %s, %s, %s, %s)"""

                            cursor.execute(
                                holiday_param_insert_categorized,
                                (
                                    prediction_id,
                                    name,
                                    effect_value,
                                    type,
                                    date_obj,
                                    restaurant,
                                    company,
                                    parent_restaurant,
                                    datetime.now(),
                                ),
                            )
                        elif (
                            effect_value < -2000
                            and name in holiday_names_negative
                        ):
                            # print(f'upper {restaurant}: {name}')

                            holiday_param_insert = """ INSERT INTO public."Predictions_holidayparameters" (id,prediction_id, name, effect, type, date, restaurant, company, parent_restaurant,created_at)
                            VALUES (gen_random_uuid(),%s, %s, %s,'event', %s, %s, %s, %s,%s)"""
                            cursor.execute(
                                holiday_param_insert,
                                (
                                    prediction_id,
                                    name,
                                    effect_value,
                                    date_obj,
                                    restaurant,
                                    company,
                                    parent_restaurant,
                                    datetime.now(),
                                ),
                            )
        conn.commit()
        conn.close()
    print(f"Finished prediction for {restaurant} of {company}")
