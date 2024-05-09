import pandas as pd


# firstweek_jan = pd.DataFrame(
#         {
#             "holiday": "firstweek_jan",
#             "ds": pd.to_datetime(["2022-01-10", "2023-01-08", "2024-01-07"]),
#             "lower_window": -7,
#             "upper_window": 0,
#         }
#     )
christmas_day = pd.DataFrame(
        {
            "holiday": "christmas eve",
            "ds": pd.to_datetime(["2022-12-24"]),
            "lower_window": -5,
            "upper_window": 0,
        }
    )

jan_closed = pd.DataFrame({
            "holiday": "jan_closed_2022",
            "ds": pd.to_datetime(
                ["2022-01-30"]
            ),
            "lower_window": -31,
            "upper_window": 0,
            "effect":-10000,
            "prior_scale": 1
        }
    )


start_date_december_holiday = "2020-06-06"
end_date_december_holiday= "2022-11-30"
sundays_2020_2021 = pd.date_range(start=start_date_december_holiday, end=end_date_december_holiday, freq="W-SUN")
december_open_2020_2021 = pd.DataFrame({
            "holiday": "open_december",
            "ds": sundays_2020_2021,
            "lower_window": 0,
            "upper_window": 0,
            "effect":5,
            "prior_scale":100
})

start_date_december_2022 = "2022-12-01"
end_date_december_2022= "2022-12-25"
sundays_2022_december = pd.date_range(start=start_date_december_2022, end=end_date_december_2022, freq="W-SUN")
december_2022 = pd.DataFrame({
            "holiday": "open_december_2022",
            "ds": sundays_2022_december,
            "lower_window": 0,
            "upper_window": 0,
            "effect":5,
            "prior_scale":100
})

start_date_2022_closed = "2022-02-01"
end_date_2022_closed= "2022-11-30"
sundays_2022_open = pd.date_range(start=start_date_2022_closed, end=end_date_2022_closed, freq="W-SUN")
december_open = pd.DataFrame({
            "holiday": "closed_december_2022",
            "ds": sundays_2022_open,
            "lower_window": 0,
            "upper_window": 0,
            "effect":-10000,
            "prior_scale": 1
})

start_date_december_2023 = "2023-12-01"
end_date_december_2023= "2024-01-07"
sundays_2023_december = pd.date_range(start=start_date_december_2023, end=end_date_december_2023, freq="W-SUN")
december_2023 = pd.DataFrame({
            "holiday": "open_december_2023",
            "ds": sundays_2023_december,
            "lower_window": 0,
            "upper_window": 0,
            "effect":5,
            "prior_scale":100
})

start_date_sunday_closed = "2023-01-01"
end_date_sunday_closed= "2023-11-01"
sundays_closed_2023 = pd.date_range(start=start_date_sunday_closed, end=end_date_sunday_closed, freq="W-SUN")
sunday_2023 = pd.DataFrame({
            "holiday": "closed_sunday_2023",
            "ds": sundays_closed_2023,
            "lower_window": 0,
            "upper_window": 0,
            "effect":-10000,
            "prior_scale": 1
})
start_date_sunday_closed_2024 = "2024-01-14"
end_date_sunday_closed_2024= "2024-11-30"
sundays_closed_2024 = pd.date_range(start=start_date_sunday_closed, end=end_date_sunday_closed, freq="W-SUN")
sunday_2024 = pd.DataFrame({
            "holiday": "closed_sunday_2024",
            "ds": sundays_closed_2023,
            "lower_window": 0,
            "upper_window": 0,
            "effect":-10000,
            "prior_scale": 1
})

# new_years_day = pd.DataFrame(
#         {
#             "holiday": "new_years_day",
#             "ds": pd.to_datetime(["2022-01-01", "2023-01-01"]),
#             "lower_window": 0,
#             "upper_window": 0,
#         }
#     )

# first_may = pd.DataFrame(
#         {
#             "holiday": "first_may",
#             "ds": pd.to_datetime(["2021-05-01", "2022-05-01", "2023-05-01"]),
#             "lower_window": -1,
#             "upper_window": 0,
#         }
#     )

easter = pd.DataFrame(
        {
            "holiday": "easter",
            "ds": pd.to_datetime(
                [
                    "2022-04-14",
                    "2022-04-15",
                    "2022-04-16",
                    "2022-04-17",
                    "2023-04-06",
                    "2023-04-07",
                    "2023-04-08",
                    "2023-04-09",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

easter_lowsaturday = pd.DataFrame(
        {
            "holiday": "easter_lowsaturday",
            "ds": pd.to_datetime(["2022-04-16"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )    

easter_mondaydayoff = pd.DataFrame(
        {
            "holiday": "easter_mondaydayoff",
            "ds": pd.to_datetime(["2022-04-18", "2023-04-10"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

# pinse = pd.DataFrame(
#         {
#             "holiday": "pinse",
#             "ds": pd.to_datetime(["2022-06-06", "2023-05-29"]),
#             "lower_window": -4,
#             "upper_window": 0,
#         }
#     )

day_before_red_day = pd.DataFrame(
        {
            "holiday": "day_before_red_day",
            "ds": pd.to_datetime(
                [
                    "2022-04-14",
                    "2022-05-16",
                    "2022-05-25",
                    "2022-12-24",
                    "2023-04-05",
                    "2023-05-16",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

# himmelfart = pd.DataFrame(
#         {
#             "holiday": "himmelfart",
#             "ds": pd.to_datetime(["2022-05-26"]),
#             "lower_window": -1,
#             "upper_window": 0,
#         }
#     )

closed_days = pd.DataFrame(
        {
            "holiday": "closed_days",
            "ds": pd.to_datetime(
                [
                    "2022-04-14",
                    "2022-04-15",
                    "2022-04-17",
                    "2022-04-18",
                    "2022-12-25",
                    "2022-12-26",
                    "2022-06-05",
                    "2022-06-06",
                    "2022-06-11",
                    "2022-06-12",
                    "2023-01-01",
                    "2023-04-06",
                    "2023-04-07",
                    "2023-04-08",
                    "2023-04-09",
                    "2023-04-10",
                    "2023-05-01",
                    "2023-05-17",
                    "2023-05-18",
                    "2023-05-29",
                    "2023-12-24",
                    "2023-12-25",
                    "2023-12-31",
                    "2024-12-24",
                    "2024-12-25",
                    "2024-12-31",
                    "2025-12-24",
                    "2025-12-25",
                    "2025-12-31",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )   
# oslo_pride = pd.DataFrame(
#         {
#             "holiday": "oslo_pride",
#             "ds": pd.to_datetime(["2023-07-01"]),
#             "lower_window": -7,
#             "upper_window": 3,
#         }
#     )    
norway_cup = pd.DataFrame(
        {
            "holiday": "Norway Cup",
            "ds": pd.to_datetime(["2022-08-03", "2023-08-05"]),
            "lower_window": -8,
            "upper_window": 1,
        }
    )
black_friday = pd.DataFrame(
        {
            "holiday": "Black Friday",
            "ds": pd.to_datetime(["2022-11-25", "2023-11-24"]),
            "lower_window": -1,
            "upper_window": 0,
        }
    )  


# SO TESTING EVENTS TO SEE IF RMSE IMPROVES (CLOSED DAYS< UNUSUAL SLOWDOWN AND ELSE)
unusual_low_sale = pd.DataFrame(
        {
            "holiday": "Dec 17-31 unusual low sale",
            "ds": pd.to_datetime(["2021-12-31","2023-11-24"]),
            "lower_window": -14,
            "upper_window": 0,
        }
    )  


