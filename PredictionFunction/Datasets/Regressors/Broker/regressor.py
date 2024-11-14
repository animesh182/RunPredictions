import pandas as pd

def is_outdoor_seating_broker(df):
    df['month'] = df['ds'].dt.month
    # Apply the conditions 
    df['outdoor_seating'] = (
        (df['month'].isin([5, 6, 7, 8, 9])) &
        (df['sunshine_amount'] < 200) &
        (df['air_temperature'] > 10) & (df['air_temperature'] < 17)
    ).astype(int)
    # df.to_csv('outdoor_seating.csv')
    return df


def very_good_weather(df):
    df['very_good_weather_low_sales'] = (
        (df['sunshine_amount'] > 350) &
        (df['air_temperature'] > 20) 
    ).astype(int)
    # df.to_csv('outdoor_seating.csv')
    return df

def is_high_weekends(df):
    df['month'] = df['ds'].dt.month
    # Apply the conditions 
    df['high_sales_weekend'] = (
        (df['month'].isin([10,11])) &
        (df['day_of_week'].isin([5]))
    ).astype(int)
    # df.to_csv('outdoor_seating.csv')
    return df

def is_low_weekday(df):
    df['month'] = df['ds'].dt.month
    # Apply the conditions 
    df['low_sales_weekday'] = (
        # (df['month'].isin([10,11])) &
        (df['day_of_week'].isin([6,0,1]))
    ).astype(int)
    # df.to_csv('outdoor_seating.csv')
    return df