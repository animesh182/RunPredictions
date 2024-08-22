from datetime import datetime
import pandas as pd
import psycopg2
from PredictionFunction.utils.params import params,prod_params


def add_opening_hours(df, restaurant_name,normal_hour,special_hour):
    with psycopg2.connect(**prod_params) as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" select id from public."accounts_restaurant" where name=%s """,[restaurant_name])
            restaurant_id= cursor.fetchone()[0]
            opening_hour_query = """
                    SELECT *
                    FROM public."accounts_openinghours"
                    WHERE restaurant_id = %s
                """
            opening_hours_df = pd.read_sql_query(opening_hour_query,conn,params=[restaurant_id])
    opening_hours_df['start_date'] = pd.to_datetime(opening_hours_df['start_date'])
    opening_hours_df['end_date'] = pd.to_datetime(opening_hours_df['end_date'])
    def get_opening_duration(date):
        day_type = int(date.strftime("%w"))
        date = pd.to_datetime(date)
        opening_df = opening_hours_df[
            (opening_hours_df['day_of_week'] == int(day_type)) &  # Ensure day_type matches the 'day_of_week' values in the DataFrame
            (opening_hours_df['start_date'] <= date) &
            (opening_hours_df['end_date'] >= date)
            ]
            
        if not opening_df.empty:
            latest_entry = opening_df.sort_values(by='created_at', ascending=False).iloc[0]
            start = latest_entry['start_hour']
            end = latest_entry['end_hour']
            if start > end:
                duration = (24 - start) + end
            elif start==end:
                duration=0
            else:
                duration = end - start

            return duration
        else:
            return 0  # Assuming 0 hours for closed

    def scale_duration(duration, day_type):
        if duration == 0:
            return -1  # Closedx
        elif duration >= 24:
            return 1  # Open 24 hours
        elif duration in special_hour:
            return 0
        elif duration in normal_hour:
            return 0
        else:
            return 0

    df["opening_duration"] = df["ds"].apply(get_opening_duration)
    df["opening_duration"] = df.apply(
        lambda row: scale_duration(
            row["opening_duration"], int(row["ds"].strftime("%w"))
        ),
        axis=1,
    )
    return df



def get_opening_closing_hours(df, day_type, date_obj):

    # Assuming df is your DataFrame and date_obj is your Timestamp object
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])

    # Convert Series to date
    df['start_date_date'] = df['start_date'].dt.date
    df['end_date_date'] = df['end_date'].dt.date
    date_obj_date = date_obj.date()

    # Filter the DataFrame
    opening_df = df[
        (df['day_of_week'] == int(day_type)) &  # Ensure day_type matches the 'day_of_week' values in the DataFrame
        (df['start_date_date'] <= date_obj_date) &
        (df['end_date_date'] >= date_obj_date)
    ]
    if not opening_df.empty:
        # Sort by created_at in descending order to get the latest entry
        latest_entry = opening_df.sort_values(by='created_at', ascending=False).iloc[0]
        start_hour = latest_entry['start_hour']
        end_hour = latest_entry['end_hour']
        return start_hour, end_hour
    else:
        return None, None