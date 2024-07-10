import pandas as pd


def is_event_with_good_weather(df, dataframe_name):
    # Filter rows where event_name is 1
    event_filter = df[dataframe_name] == 1
    warm_threshold = df['sunshine_amount'].quantile(0.70)
    dry_threshold = 5
    condition = (df['sunshine_amount'] >= warm_threshold) & (df['rain_sum'] <= dry_threshold)
    df[f'{dataframe_name}_good_weather'] = 0
    # Set the new column to 1 where both conditions are met
    df.loc[event_filter & condition, f'{dataframe_name}_good_weather'] = 1
    return df

def is_event_with_bad_weather(df, dataframe_name):
    # Filter rows where event_name is 1
    event_filter = df[dataframe_name] == 1
    warm_threshold = df['sunshine_amount'].quantile(0.40)
    dry_threshold = 10
    condition = (df['sunshine_amount'] <= warm_threshold) & (df['rain_sum'] > dry_threshold)
    df[f'{dataframe_name}_bad_weather'] = 0
    # Set the new column to 1 where both conditions are met
    df.loc[event_filter & condition, f'{dataframe_name}_bad_weather'] = 1
    return df

def is_event_with_normal_weather(df, dataframe_name):
    event_filter = df[dataframe_name] == 1
    # Calculate quantiles for sunshine amount
    warm_threshold_lower = df['sunshine_amount'].quantile(0.40)
    warm_threshold_upper = df['sunshine_amount'].quantile(0.70)
    # Define the condition for normal weather
    condition = (
        (((df['sunshine_amount'] > warm_threshold_lower) & (df['sunshine_amount'] < warm_threshold_upper)) | (df['sunshine_amount'] == 0)) 
        & (df['rain_sum'] <= 5)
    )
    df[f'{dataframe_name}_normal_weather'] = 0
    df.loc[event_filter & condition, f'{dataframe_name}_normal_weather'] = 1
    return df

