# Drammen is not used for comparison
import pandas as pd

# ------Event--------
first_may = pd.DataFrame(
        {
            "holiday": "First of may",
            "ds": pd.to_datetime(["2021-05-01", "2022-05-01", "2023-05-01", "2024-05-01","2025-05-01", "2026-05-01", "2027-05-01"]),
            "upper_window": 0,
            "lower_window": 0,
        }
    )

christmas = pd.DataFrame(
        {
            "holiday": "christmas",
            "ds": pd.to_datetime(["2021-12-25", "2022-12-25","2023-12-25","2024-12-25","2025-12-25","2026-12-25","2027-12-25"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

seventeenth_may = pd.DataFrame(
        {
            "holiday": "Seventeenth of may",
            "ds": pd.to_datetime(
                ["2021-05-17", "2022-05-17", "2023-05-17", "2024-05-17", "2025-05-17", "2026-05-17", "2027-05-17"]
            ),
            "lower_window": -1,
            "upper_window": 0,
        }
    )
firstweek_jan = pd.DataFrame(
        {
            "holiday": "firstweek_jan",
            "ds": pd.to_datetime(["2022-01-10", "2023-01-08", "2024-01-07", "2025-01-07", "2026-01-07"]),
            "lower_window": -6,
            "upper_window": 0,
        }
    )

first_weekend_christmas_school_vacation = pd.DataFrame(
        {
            "holiday": "First weekend of christmas school break",
            "ds": pd.to_datetime(["2021-12-19","2022-12-18","2023-12-17","2024-12-22","2025-12-21"]),
            "lower_window": -2,
            "upper_window": 0,
        }
    )

new_years_day = pd.DataFrame(
        {
            "holiday": "New Years",
            "ds": pd.to_datetime(["2022-01-01", "2023-01-01","2024-01-01","2025-01-01","2026-01-01","2027-01-01"]),
            "lower_window": -1,
            "upper_window": 0,
        }
    )

pinse = pd.DataFrame(
        {
            "holiday": "Pinse",
            "ds": pd.to_datetime(["2022-06-06", "2023-05-29","2024-05-20","2025-06-09"]),
            "lower_window": -3,
            "upper_window": 0,
        }
    )

himmelfart = pd.DataFrame(
        {
            "holiday": "Himmelfart",
            "ds": pd.to_datetime(["2022-05-26","2023-05-18","2024-05-09","2025-05-29"]),
            "lower_window": 0,
            "upper_window": 0,
        }
    )

hostferie_sor_ostlandet_weekdays = pd.DataFrame(
    {
        "holiday": "Høstferie weekdays",
        "ds": pd.to_datetime(["2024-10-4","2023-10-05", "2022-10-07"]),
        "lower_window": -4,
        "upper_window": 0,
    }
) 
hostferie_sor_ostlandet_weekdend = pd.DataFrame(
    {
        "holiday": "Høstferie weekend",
        "ds": pd.to_datetime(["2024-10-06","2023-10-08", "2022-10-09"]),
        "lower_window": -1,
        "upper_window": 0,
    }
) 
hostferie_vestlandet_weekdays = pd.DataFrame(
    {
        "holiday": "Høstferie weekdays",
        "ds": pd.to_datetime(["2023-10-12", "2022-10-13", "2021-10-14"]),
        "lower_window": -3,
        "upper_window": 0,
    }
) 
hostferie_vestlandet_weekdend = pd.DataFrame(
    {
        "holiday": "Høstferie weekend",
        "ds": pd.to_datetime(["2023-10-14", "2022-10-15", "2021-10-16"]),
        "lower_window": -1,
        "upper_window": 0,
    }
) 
vinterferie_vestlandet_weekend_before = pd.DataFrame(
    {
        "holiday": "Helgen før vinterferie",
        "ds": pd.to_datetime(["2022-02-26", "2023-02-25", "2024-02-24"]),
        "lower_window": -1,
        "upper_window": 0,
    }
) 
vinterferie_vestlandet_weekend = pd.DataFrame(
    {
        "holiday": "Helgen i vinterferien",
        "ds": pd.to_datetime(["2022-03-05", "2023-03-04", "2024-03-02"]),
        "lower_window": -1,
        "upper_window": 0,
    }
) 
vinterferie_ostlandet_saturday_before = pd.DataFrame(
    {
        "holiday": "Lørdagen før vinterferien",
        "ds": pd.to_datetime(["2022-02-19", "2023-02-18", "2024-02-17"]),
        "lower_window": 0,
        "upper_window": 0,
    }
) 
vinterferie_ostlandet_saturday = pd.DataFrame(
    {
        "holiday": "Lørdagen i vinterferien",
        "ds": pd.to_datetime(["2022-02-26", "2023-02-25", "2024-02-24"]),
        "lower_window": 0,
        "upper_window": 0,
    }
) 

mela_festival= pd.DataFrame(
    {
        "holiday": "mela festival",
        "ds": pd.to_datetime(["2022-02-26", "2023-08-20", "2024-08-18"]),
        "lower_window": -2,
        "upper_window": 0,
    }
) 

new_year_romjul= pd.DataFrame(
    {
        "holiday": "new year romjul",
        "ds": pd.to_datetime(["2022-12-30", "2023-12-30", "2024-12-30","2025-12-30","2026-12-30"]),
        "lower_window": -4,
        "upper_window": 0,
    }
) 

easter = pd.DataFrame(
    {
        "holiday": "Easter",
        "ds": pd.to_datetime(["2022-04-18", "2023-04-10", "2024-04-01","2025-04-21"]),
        "lower_window": -4,
        "upper_window": 0,
    }
) 

christmas_day = pd.DataFrame(
    {
        "holiday": "Easter",
        "ds": pd.to_datetime(["2022-12-25", "2023-12-25", "2024-12-25","2025-12-25"]),
        "lower_window": -1,
        "upper_window": 0,
    }
) 
