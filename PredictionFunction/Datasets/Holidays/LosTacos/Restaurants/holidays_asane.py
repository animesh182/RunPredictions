import pandas as pd

pre_christmas_covid21 = pd.DataFrame(
        {
            "holiday": "Pre Christmas covid 21",
            "ds": pd.to_datetime(["2021-12-22"]),
            "lower_window": -6,
            "upper_window": 0,
        }
    )

weekendmiddec_21covid = pd.DataFrame(
        {
            "holiday": "weekendmiddec_21covid",
            "ds": pd.to_datetime(["2021-12-12"]),
            "lower_window": -2,
            "upper_window": 0,
        }
    )


fadder_week = pd.DataFrame(
        {
            "holiday": "Fadder week",
            "ds": pd.to_datetime(["2022-08-21", "2023-08-20"]),
            "lower_window": -7,
            "upper_window": 0,
        }
    )   

# only when the holiday is on a weekday. If it is in the weekend there is no effect
# first_may = pd.DataFrame(
#         {
#             "holiday": "First of may",
#             "ds": pd.to_datetime(["2021-05-01", "2023-05-01"]),
#             "lower_window": -1,
#             "upper_window": 0,
#         }
#     )

# pinse = pd.DataFrame(
#         {
#             "holiday": "Pinse",
#             "ds": pd.to_datetime(["2022-06-06", "2023-05-29"]),
#             "lower_window": -4,
#             "upper_window": 0,
#         }
#     )

# himmelfart = pd.DataFrame(
#         {
#             "holiday": "Himmelfart",
#             "ds": pd.to_datetime(["2022-05-26"]),
#             "lower_window": -1,
#             "upper_window": 0,
#         }
#     )

military_excercise = pd.DataFrame(
        {
            "holiday": "Military excercise",
            "ds": pd.to_datetime(
                ["2022-03-12", "2022-03-13", "2022-03-19", "2022-03-20"]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

helg_før_fellesferie = pd.DataFrame(
        {
            "holiday": "Weekends before fellesferie",
            "ds": pd.to_datetime(["2022-07-01", "2022-07-02", "2022-07-03"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )  

closed = pd.DataFrame(
        {
            "holiday": "Closed",
            "ds": pd.to_datetime(
                [
                    "2021-12-22",
                    "2021-12-23",
                    "2021-12-24",
                    "2021-12-25",
                    "2021-12-26",
                    "2021-12-31",
                    "2022-12-24",
                    "2022-12-25",
                    "2022-12-31",
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

july_closed = pd.DataFrame({
            "holiday": "july_closed_2022",
            "ds": pd.to_datetime(
                ["2022-07-31"]
            ),
            "lower_window": -31,
            "upper_window": 0,
            "effect":-10000,
            "prior_scale": 1
        }
    )

unknown_outliers = pd.DataFrame(
        {
            "holiday": "unknown_outliers",
            "ds": pd.to_datetime(["2021-09-06", "2022-11-07"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )    

covid_christmas21_startjan22 = pd.DataFrame(
        {
            "holiday": "covid_christmas21_startjan22",
            "ds": pd.to_datetime(
                [
                    "2021-12-27",
                    "2021-12-28",
                    "2021-12-29",
                    "2021-12-30",
                    "2021-12-31",
                    "2022-01-01",
                    "2022-01-02",
                    "2022-01-03",
                    "2022-01-04",
                    "2022-01-05",
                    "2022-01-06",
                    "2022-01-07",
                    "2022-01-08",
                    "2022-01-09",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )


bergen_pride = pd.DataFrame(
        {
            "holiday": "Bergen Pride",
            "ds": pd.to_datetime(
                [
                    "2023-06-10",
                    "2024-06-08"

                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )


last_day_of_school = pd.DataFrame(
        {
            "holiday": "Last day of school",
            "ds": pd.to_datetime(["2023-06-21","2024-06-28","2025-06-30"]),
            "lower_window": 0,
            "upper_window": 1,
        }
    )

first_day_of_school = pd.DataFrame(
        {
            "holiday": "First day of school",
            "ds": pd.to_datetime(["2022-08-08","2023-08-01","2024-08-15","2025-08-01"]),
            "lower_window": -1,
            "upper_window": 0,
        }
    )

black_friday =  pd.DataFrame(
        {
            "holiday": "Black Friday",
            "ds": pd.to_datetime(["2022-11-26","2022-11-25","2023-11-24","2024-11-29"]),
            "lower_window": -4,
            "upper_window": 0,
        }
    )
christmas =  pd.DataFrame(
        {
            "holiday": "Christmas shopping week",
            "ds": pd.to_datetime(["2021-12-22","2022-12-22","2023-12-22","2024-12-22"]),
            "lower_window": -2,
            "upper_window": 0,
        }
    )
