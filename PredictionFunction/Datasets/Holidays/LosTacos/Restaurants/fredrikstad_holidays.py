import pandas as pd

fadder_week = pd.DataFrame(
        {
            "holiday": "fadder_week",
            "ds": pd.to_datetime(
                ["2022-08-15", "2022-08-16", "2022-08-17", "2022-08-18"]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )  

# idyll
idyll = pd.DataFrame(
        {
            "holiday": "idyll",
            "ds": pd.to_datetime(["2022-06-19", "2023-06-18"]),
            "lower_window": -3,
            "upper_window": 0,
        }
    )  

# closed days
closed_days = pd.DataFrame(
        {
            "holiday": "closed_days",
            "ds": pd.to_datetime(
                [
                    "2021-12-22",
                    "2021-12-23",
                    "2021-12-24",
                    "2021-12-25",
                    "2022-12-24",
                    "2022-12-31",
                    "2023-12-24",
                    
                    "2023-12-31",
                    "2024-12-24",
                    
                    "2024-12-31",
                    "2025-12-24",
               
                    "2025-12-31",
                ]
            ),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

# black friday    # 
black_friday = pd.DataFrame(
        {
            "holiday": "Black Friday",
            "ds": pd.to_datetime(["2022-11-25", "2023-11-24"]),
            "lower_window": -1,
            "upper_window": 0,
        }
    )     

feb_closed=  pd.DataFrame(
        {
            "holiday": "Closed february 2024",
            "ds": pd.to_datetime(["2024-02-29"]),
            "lower_window": -30,
            "upper_window": 0,
        }
    )   