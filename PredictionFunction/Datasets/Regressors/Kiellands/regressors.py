import pandas as pd

def high_sale_month_kiellands(df):
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    # Apply the conditions for heavy rain weekend
    df['high_sale_months'] = (
        (df['day_of_week'].isin([3,4,5,6])) &
        (df['month'].isin([4, 5,6,7,8,9]))  # Assuming fall is September, October, November
    ).astype(int)
    
    return df