import pandas as pd

FALL_START_DATES = {
        2022: {"start": "2022-08-08", "end": "2022-08-21"},
        2023: {"start": "2023-08-07", "end": "2023-08-20"},
        2024: {"start": "2024-08-07", "end": "2024-08-20"},
        # Add more years and their respective dates as needed
    }
def is_fall_start(ds):
        date = pd.to_datetime(ds)
        year = date.year  # Extract the year from the input date

        if year not in FALL_START_DATES:
            return False  # or raise an error if you prefer

        start_date = pd.Timestamp(FALL_START_DATES[year]["start"])
        end_date = pd.Timestamp(FALL_START_DATES[year]["end"])

        return start_date <= date <= end_date
def is_first_two_weeks_january_21(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2022-01-10")
        end_date = pd.Timestamp("2022-01-30")
        return start_date <= date <= end_date
def is_fellesferie(ds):
        fellesferie_dates = {
        2022: {"start": "2022-07-05", "end": "2022-08-05"},
        2023: {"start": "2023-07-10", "end": "2023-07-28"},
        2024: {"start": "2023-07-08", "end": "2023-07-26"},
        # Add more years and their respective dates as needed
    }
        date = pd.to_datetime(ds)
        year = date.year  # Extract the year from the input date

        if year not in fellesferie_dates:
            return False  # or raise an error if you prefer

        start_date = pd.Timestamp(fellesferie_dates[year]["start"])
        end_date = pd.Timestamp(fellesferie_dates[year]["end"])
        return start_date <= date <= end_date

def is_specific_month(ds):
        date = pd.to_datetime(ds)
        start_date = pd.to_datetime(
            "2022-07-01"
        )  # replace with the start date of the interval
        end_date = pd.to_datetime(
            "2022-07-31"
        )  # replace with the end date of the interval
        return start_date <= date <= end_date
def is_covid_restriction_christmas(ds):
        date = pd.to_datetime(ds)
        start_date = pd.to_datetime(
            "2021-12-13"
        )  # replace with the start date of the restriction period
        end_date = pd.to_datetime(
            "2022-01-09"
        )  # replace with the end date of the restriction period
        return start_date <= date <= end_date
def is_christmas_shopping(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2022-11-14")
        end_date = pd.Timestamp("2022-12-11")
        return start_date <= date <= end_date
def is_closed(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2022-01-01")  # Replace with the closure start date
        end_date = pd.Timestamp("2022-02-28")  # Replace with the closure end date
        return start_date <= date <= end_date
def is_campaign_active(ds, campaign_row):
         date = pd.to_datetime(ds)
         return 1 if pd.to_datetime(campaign_row['startdate']) <= date <= pd.to_datetime(campaign_row['enddate']) else 0
def is_high_weekends(ds):
        date = pd.to_datetime(ds)
        return date.month > 8 or date.month < 2
def is_fellesferie_sandnes(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2022-07-05")
        end_date = pd.Timestamp("2022-08-05")
        return start_date <= date <= end_date
def is_covid_loose_fall21(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2021-09-20")
        end_date = pd.Timestamp("2021-10-31")
        return start_date <= date <= end_date
def is_fellesferie_stavanger(ds):
        date = pd.to_datetime(ds)
        start_date = pd.Timestamp("2022-07-05")
        end_date = pd.Timestamp("2022-08-05")
        return start_date <= date <= end_date
def is_may(ds):
        ds = pd.to_datetime(ds)
        return ds.month == 5

def is_monday_Fisk_restaurant(ds):
    ds = pd.to_datetime(ds)
    return ds.dayofweek == 0

def is_saturday_rainy_windy(row):
        return 1 if(row['ds'].dayofweek == 5) and (row['rain_sum']>5) and (row['windspeed']>4.5) else 0


def is_high_weekend_spring(ds):
    date = pd.to_datetime(ds)
    high_weekend_spring = {
        2022: {"start": "2022-05-01", "end": "2022-06-30"},
        2023: {"start": "2023-05-01", "end": "2023-06-30"},
        2024: {"start": "2024-05-01", "end": "2024-06-30"},
        # Add more years and their respective dates as needed
    }
    date = pd.to_datetime(ds)
    year = date.year  # Extract the year from the input date

    if year not in high_weekend_spring:
        return False  

    start_date = pd.Timestamp(high_weekend_spring[year]["start"])
    end_date = pd.Timestamp(high_weekend_spring[year]["end"])
    if start_date <= date <= end_date and date.weekday() in [4, 5]:
        return True
    else:
        return False


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



def july_august_weekend_utsalg(df):
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    # Apply the conditions for heavy rain weekend
    df['weekend_july_august'] = (
        (df['day_of_week'].isin([4, 5])) &
        (df['month'].isin([7, 8]))  # Assuming fall is September, October, November
    ).astype(int)
    
    return df


def july_august_wednesnday_stavanger(df):
    df['day_of_week'] = df['ds'].dt.dayofweek
    df['month'] = df['ds'].dt.month
    # Apply the conditions for heavy rain weekend
    df['wednesday_high_sale'] = (
        (df['day_of_week'].isin([2])) &
        (df['month'].isin([6,7,8]))  # Assuming fall is September, October, November
    ).astype(int)
    
    return df