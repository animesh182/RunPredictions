import pandas as pd

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

closed_march = pd.DataFrame(
        {
            "holiday": "march closed",
            "ds": pd.to_datetime(["2023-04-30"]),
            "lower_window": -12,
            "upper_window": 0,
        }
    )    

