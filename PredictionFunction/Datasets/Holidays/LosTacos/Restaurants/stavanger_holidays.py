import pandas as pd

from PredictionFunction.Datasets.Holidays.LosTacos.dataset_holidays import (
    cruise_ship_arrivals,
    twelfth_working_days,
    last_working_day,
)
christmas_day = pd.DataFrame(
        {
            "holiday": "christmas eve",
            "ds": pd.to_datetime(["2022-12-24"]),
            "lower_window": -5,
            "upper_window": 0,
        }
    )

new_year_eve = pd.DataFrame(
        {
            "holiday": "new_year_eve",
            "ds": pd.to_datetime(["2022-12-31", "2023-12-31"]),
            "lower_window": -6,
            "upper_window": 0,
        }
    )

# firstweek_jan = pd.DataFrame(
#         {
#             "holiday": "firstweek_jan",
#             "ds": pd.to_datetime(["2022-01-10", "2023-01-08", "2024-01-07"]),
#             "lower_window": -7,
#             "upper_window": 0,
#         }
#     )

# new_years_day = pd.DataFrame({
#         'holiday': 'new_years_day',
#         'ds': pd.to_datetime(['2022-01-01', '2022-01-01', '2023-01-01']),
#         'lower_window': 0,
#         'upper_window': 0,
#     })

fadder_week = pd.DataFrame(
        {
            "holiday": "fadder_week",
            "ds": pd.to_datetime(
                [
                    "2022-08-16",
                    "2022-08-17",
                    "2022-08-18",
                    "2022-08-19",
                    "2022-08-20",
                    "2022-08-21",
                    "2023-08-15",
                    "2023-08-16",
                    "2023-08-17",
                    "2023-08-18",
                    "2023-08-19",
                    "2023-08-20",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

# only when the holiday is on a weekday. If it is in the weekend there is no effect
# first_may = pd.DataFrame(
#         {
#             "holiday": "first_may",
#             "ds": pd.to_datetime(["2021-05-01", "2023-05-01"]),
#             "lower_window": -1,
#             "upper_window": 1,
#         }
#     )
eight_may = pd.DataFrame(
        {
            "holiday": "eight_may",
            "ds": pd.to_datetime(["2021-05-08", "2022-05-08", "2023-05-08"]),
            "lower_window": -1,
            "upper_window": 1,
        }
    )
seventeenth_may = pd.DataFrame(
        {
            "holiday": "seventeenth_may",
            "ds": pd.to_datetime(
                ["2021-05-17", "2022-05-17", "2023-05-17", "2024-05-17"]
            ),
            "lower_window": -1,
            "upper_window": 1,
        }
    )

easter = pd.DataFrame(
        {
            "holiday": "easter",
            "ds": pd.to_datetime(
                [
                    "2022-04-14",
                    "2022-04-15",
                    "2022-04-16",
                    "2022-04-17",
                    "2022-04-18",
                    "2023-04-02",
                    "2023-04-06",
                    "2023-04-07",
                    "2023-04-09",
                    "2023-04-10",
                    "2024-03-24",
                    "2024-03-28",
                    "2024-03-29",
                    "2024-03-30",
                    "2024-03-31",
                    "2024-04-01",
                ]
            ),
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

landstreff_russ = pd.DataFrame(
        {
            "holiday": "Landstreff russ",
            "ds": pd.to_datetime(["2022-05-06", "2023-05-05", "2024-05-03"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

# pinse = pd.DataFrame(
#         {
#             "holiday": "pinse",
#             "ds": pd.to_datetime(["2022-06-06", "2022-05-29"]),
#             "lower_window": -4,
#             "upper_window": 0,
#         }
#     )

# # 2023: falls the day after the national independence day, so no effect the day before this year
# himmelfart = pd.DataFrame(
#         {
#             "holiday": "himmelfart",
#             "ds": pd.to_datetime(["2022-05-26"]),
#             "lower_window": -1,
#             "upper_window": 0,
#         }
#     )

fjoge = pd.DataFrame(
        {
            "holiday": "fjoge",
            "ds": pd.to_datetime(
                [
                    "2022-06-22",
                    "2022-06-29",
                    "2022-07-06",
                    "2022-07-13",
                    "2022-07-20",
                    "2023-06-07",
                    "2023-06-21",
                    "2023-06-28",
                    "2023-07-05",
                    "2023-07-12",
                    "2023-07-19",
                    "2023-07-26",
                    "2023-07-27",
                    "2023-07-28",
                    "2023-07-29",
                    "2023-07-29",
                    "2023-07-29",
                    "2024-07-24",
                    "2024-07-25",
                    "2024-07-26",
                    "2024-07-27",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

military_excercise = pd.DataFrame(
        {
            "holiday": "Militærøvelse",
            "ds": pd.to_datetime(["2023-09-07"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )



outliers = pd.DataFrame(
        {
            "holiday": "outliers",
            "ds": pd.to_datetime(
                ["2022-06-11", "2022-08-27", "2022-10-22", "2022-11-05"]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

closed_days = pd.DataFrame(
        {
            "holiday": "closed_days",
            "ds": pd.to_datetime(
                ["2021-12-23", "2021-12-24", "2021-12-25", "2021-12-26",
                 "2023-12-24",
                    "2023-12-25",
                    "2023-12-31",
                    "2024-12-24",
                    "2024-12-25",
                    "2024-12-31",
                    "2025-12-24",
                    "2025-12-25",
                    "2025-12-31",]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

cruise_ship_arrivals_holiday = pd.DataFrame(
        {
            "holiday": "cruise_ship_arrivals",
            "ds": pd.to_datetime(cruise_ship_arrivals),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

pay_day = pd.DataFrame(
        {
            "holiday": "Payday",
            "ds": pd.to_datetime(last_working_day),
            "lower_window": -4,
            "upper_window": 4,
        }
    )
# utopia_friday = pd.DataFrame(
#         {
#             "holiday": "Utopia",
#             "ds": pd.to_datetime(["2022-08-26", "2023-08-25"]),
#             "lower_window": 0,
#             "upper_window": 0,
#         }
#     )
# utopia_saturday = pd.DataFrame(
#         {
#             "holiday": "Utopia",
#             "ds": pd.to_datetime(["2022-08-27", "2023-08-26"]),
#             "lower_window": 0,
#             "upper_window": 0,
#         }
#     )
skeiva_natta = pd.DataFrame(
        {
            "holiday": "Skeiva Nattå",
            "ds": pd.to_datetime(["2022-09-03", "2023-09-02"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

valentines_day = pd.DataFrame(
        {
            "holiday": "valentines_day",
            "ds": pd.to_datetime(["2022-02-14", "2023-02-14","2024-02-14","2025-02-14"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )
food_fun_fest = pd.DataFrame(
        {
            "holiday": "Food fun festival",
            "ds": pd.to_datetime(["2024-02-29"]),
            "lower_window": -7,
            "upper_window": 0,
        }
    )
fiskesprell = pd.DataFrame(
        {
            "holiday": "Fiskesprell",
            "ds": pd.to_datetime(["2024-03-05"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )
stavanger_vinfest = pd.DataFrame(
        {
            "holiday": "Stavanger Vinfest",
            "ds": pd.to_datetime(["2024-03-16"]),
            "lower_window": -3,
            "upper_window": 0,
        }
    )
national_independence_day= pd.DataFrame(
        {
            "holiday": "Independence Day",
            "ds": pd.to_datetime(["2024-05-17"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )
gladmat = pd.DataFrame(
        {
            "holiday": "Gladmat",
            "ds": pd.to_datetime(["2022-07-02","2023-07-01","2024-06-29"]),
            "lower_window": -3,
            "upper_window": 0,
        }
    )
ons=pd.DataFrame(
        {
            "holiday": "ONS",
            "ds": pd.to_datetime(["2024-08-29"]),
            "lower_window": -2,
            "upper_window": 0,
        }
    )

april_closed = pd.DataFrame(
        {
            "holiday": "Closed April",
            "ds": pd.to_datetime(["2023-04-27"]),
            "lower_window": -20,
            "upper_window": 0,
        }
    )

june_july = pd.DataFrame(
        {
            "holiday": "june_july",
            "ds": pd.to_datetime(["2022-07-02", "2023-07-01"]),
            "lower_window": -3,
            "upper_window": 0,
        }
    )

stavanger_pride = pd.DataFrame(
        {
            "holiday": "Stavanger_pride",
            "ds": pd.to_datetime(["2022-09-03","2023-09-02", "2024-09-07"]),
            "lower_window": -1,
            "upper_window": 0,
        }
    )