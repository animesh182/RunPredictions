import pandas as pd

closed = pd.DataFrame(
        {
            "holiday": "closed",
            "ds": pd.to_datetime(
                [
                    "2021-12-23",
                    "2021-12-24",
                    "2021-12-25",
                    "2021-12-31",
                    "2022-12-24",
                    "2022-12-25",
                    "2022-12-31",
                    "2023-03-13",
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
  
