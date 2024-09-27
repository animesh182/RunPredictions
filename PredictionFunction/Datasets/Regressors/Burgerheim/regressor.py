import pandas as pd

def is_weekend_september(df):
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    # Apply the conditions for heavy rain weekend
    df['high_weekends'] = (
        (df['day_of_week'].isin([5,6])) &
        (df['month'].isin([9]))  # Assuming fall is September, October, November
    ).astype(int)
    
    return df

def low_mondays_august_sept(df):
    df['ds'] = pd.to_datetime(df['ds'])
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    # Apply the conditions for heavy rain weekend
    df['low_mondays'] = (
        (df['day_of_week'] == 0)
    ).astype(int)
    
    return df