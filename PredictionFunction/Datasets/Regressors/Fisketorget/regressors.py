import pandas as pd

def is_outdoor_seating(df):
    df['month'] = df['ds'].dt.month
    df['day_of_week'] = df['ds'].dt.dayofweek
    #Define what constitutes 'dry' and 'wet'
    fixed_heavy_rain_threshold = 10
    wind_speed_threshold = 10

    # Apply the conditions for heavy rain weekend
    df['outdoor_seating'] = (
        ((df['rain_sum'] < fixed_heavy_rain_threshold) & (df['windspeed'] < wind_speed_threshold)) &
        (df['month'].isin([5, 6, 7, 8, 9])) & (~df['day_of_week'] == 6)  # Assuming fall is September, October, November
    ).astype(int)
    # df.to_csv('outdoor_seating.csv')
    return df

def is_outdoor_seating_month(df):
    df['month'] = df['ds'].dt.month

    # Apply the conditions for heavy rain weekend
    df['outdoor_seating_month'] = (
        (df['month'].isin([5, 6, 7, 8, 9]))  # Assuming months with outdoor seating are- May, June, July, August,September
    ).astype(int)
    return df