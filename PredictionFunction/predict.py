
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

from PredictionFunction.utils.fetch_sales_data import fetch_salesdata
from PredictionFunction.PredictionTypes.daily_data_prep import prepare_data
from PredictionFunction.utils.utils import tourist_data
def predict(m,future,df,company,restaurant,start_date,end_date,prediction_category):
    if future.empty:
            raise ValueError("The future DataFrame is empty.")

        ######### make forecast and plots

        # This must be changted to the correct opening hours, which varies for days and restaurants. Create dictionary for that and use here
        # future.to_csv("futuredata.csv")
    forecast = m.predict(future)
    forecast.to_csv("forecast.csv")
    # forecast2 = m1.predict(future_residual)
    # forecast2 = m1.predict(future_residual)
    # forecast2.to_csv("forecast2.csv")
    sales_data=fetch_salesdata(company,restaurant,start_date,end_date)
    catering_df = sales_data
    try:
        # Change the date format to include the hour
        if prediction_category == "hour":
            catering_df["date"] = catering_df["date"].dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        else:
            catering_df["date"] = catering_df["date"].dt.strftime("%Y-%m-%d")
            forecast_copy = forecast.copy()
            forecast_copy.set_index("ds", inplace=True)
            catering_df.set_index("date", inplace=True)

        for index, row in catering_df.iterrows():
            if pd.to_datetime(index) in forecast_copy.index:
                forecast_copy.loc[index, "yhat"] += float(row["total_net"])

        forecast_copy.reset_index(inplace=True)
        forecast_copy = forecast_copy[["ds", "yhat"]]
        forecast_copy.columns = ["ds", "yhat_copy"]

        forecast = forecast.merge(forecast_copy, on="ds", how="left")
        forecast["yhat"].fillna(forecast["yhat_copy"], inplace=True)
        forecast.drop(columns=["yhat_copy"], inplace=True)
    except:
        pass

    # Set negative sales to 0 (this might happen sometimes for closed days)
    forecast.loc[forecast["yhat"] < 0, "yhat"] = 0
    # we reset the index after the operation over is finished, because we use it as a column below
    forecast.reset_index(level=0, inplace=True)

    if prediction_category == "day":
        merged_data, _, _ = prepare_data(company, restaurant, start_date, end_date)
    # elif prediction_category=="hour":
    #     merged_data, _, _ = hourly_sales(company, restaurant, start_date, end_date)
    # elif prediction_category=="type":
    #     merged_data, _, _ = type_predictor(company, restaurant, start_date, end_date)
    # elif prediction_category=="product":
    #     merged_data, _, _ = product_mix_predictions(company, restaurant, start_date, end_date)

    # We might need this for daily predictions
    # # merged_data = merged_data.iloc[:-15]

    # if prediction_category=="day" and company == "Yips"::

    if (
        prediction_category == "day"
        and company == "Los Tacos"
        and restaurant != "Sandnes"
    ):
        # if prediction_category=="day":
        #################### Implement XGBoost model here



        # Extract all components from Prophet's forecast
        prophet_variables = forecast[forecast["ds"].isin(df["ds"])]
        if prediction_category == "hour":
            prophet_variables = prophet_variables.reindex(df.index)
        else:
            prophet_variables = prophet_variables.set_index(df.index)
        columns_to_rename = [
            "christmas_shopping",
            "closed_jan",
            "covid_restriction_christmas",
            "custom_regressor",
            "days_since_last_15",
            "days_since_last_30",
            "days_until_next_30",
            "fornebu_large_concerts",
            "high_weekend",
            "ullevaal_big_football_games",
            "sunshine_amount",
        ]
        rename_dict = {col: col + "_new" for col in columns_to_rename}
        prophet_variables = prophet_variables.rename(columns=rename_dict)

        # Drop the 'ds' column from prophet_variables before concatenating
        prophet_variables = prophet_variables.drop(columns=["ds"])
        df_xgb = pd.concat([df, prophet_variables], axis=1)
        df_xgb["residuals"] = df_xgb["y"] - df_xgb["yhat"]

        # sace df_xgb to csv
        df_xgb.to_csv("df_xgb.csv")

        # set max columns to none and print columns in df_xgb
        pd.set_option("display.max_columns", None)
        # print("df_xgb columns here:")
        # print(df_xgb.columns)

        # Check for duplicate rows based on 'ds' column
        # print(df_xgb.shape)
        duplicate_rows = df_xgb[df_xgb.duplicated(subset="ds", keep="first")]
        # print("Number of duplicate rows based on 'ds' column:", duplicate_rows.shape[0])

        # Drop duplicate rows based on 'ds' column
        df_xgb.drop_duplicates(subset="ds", keep="first", inplace=True)

        # Assuming 'ds' column is in datetime format. If not, convert it first.
        df_xgb["ds"] = pd.to_datetime(df_xgb["ds"])

        # Extract month and week number
        df_xgb["month"] = df_xgb["ds"].dt.month
        df_xgb["week"] = df_xgb["ds"].dt.isocalendar().week  

        # Create an interaction term between month and week
        df_xgb["month_week_interaction"] = df_xgb["month"] * df_xgb["week"]

        # week temp interaction var
        # df_xgb['temp_week_interaction'] = df_xgb['air_temperature'] * df_xgb['week']

        # df_xgb.drop(columns=['ds'], inplace=True)

        # df_xgb['rain_temp_interaction'] = df_xgb['rain_sum'] * df_xgb['air_temperature']

        # Selecting only the required columns
        columns_to_use = [
            "sunshine_amount",
            "air_temperature",
            "rain_sum",
            "windspeed",
            "ds",
            "residuals",
            "yhat",
            "y",
            "weekly",
            "month_week_interaction",
        ]
        df_xgb = df_xgb[columns_to_use]

        # Convert columns to appropriate data types
        df_xgb["rain_sum"] = df_xgb["rain_sum"].astype(float)
        df_xgb["windspeed"] = df_xgb["windspeed"].astype(float)
        df_xgb["sunshine_amount"] = df_xgb["sunshine_amount"].astype(float)
        # df_xgb['total_net'] = df_xgb['total_net'].astype(float)

        # If you want to keep 'ds' column for the model, convert it to string
        # Otherwise, you can drop it
        df_xgb["ds"] = df_xgb["ds"].astype(str)

        # Training and test set
        test_days = 600
        if restaurant == "Oslo Torggata":
            test_days -= 235
        training_set = df_xgb.iloc[:-test_days, :]
        test_set = df_xgb.iloc[-test_days:, :]

        # isolate X and Y
        y_train = training_set.residuals
        y_test = test_set.residuals
        X_train = training_set.iloc[:, 2:]
        X_test = test_set.iloc[:, 2:]

        # Remove rows with invalid y_test values
        valid_indices = ~y_test.isnull() & (y_test != np.inf) & (y_test != -np.inf)
        y_test = y_test[valid_indices]
        X_test = X_test[valid_indices]

        X_train = training_set.drop(columns=["ds", "residuals", "y"])
        X_test = test_set.drop(columns=["ds", "residuals", "y"])

        # print("X_train shape:", X_train.shape)
        # print("y_train shape:", y_train.shape)
        # print("X_test shape:", X_test.shape)
        # print("y_test shape:", y_test.shape)

        # Find and print duplicate columns
        duplicate_columns = X_train.columns[X_train.columns.duplicated()]
        print("Duplicate Columns are as follows:")
        for col in duplicate_columns:
            print(col)

        # create XGBoost matrices
        valid_index = y_train.notna()
        X_train = X_train[valid_index]
        y_train = y_train[valid_index]

        valid_test_index = y_test.notna()
        X_test = X_test[valid_test_index]
        y_test = y_test[valid_test_index]
        Train = xgb.DMatrix(data=X_train, label=y_train)
        Test = xgb.DMatrix(data=X_test, label=y_test)

        # set parameters
        parameters = {
            "learning_rate": 0.1,
            "max_depth": 3,
            "min_child_weight": 2,
            "gamma": 0,
            "subsample": 1,
            "colsample_bytree": 0.5,
            "random_state": 1502,
            "eval_metric": "rmse",
            "objective": "reg:squarederror",
        }

        # XGBoost model

        model = xgb.train(
            params=parameters,
            dtrain=Train,
            num_boost_round=100,
            evals=[(Test, "residuals")],
            early_stopping_rounds=10,
            verbose_eval=15,
        )

        # forecasting and visualization with XGBoost

        # Forecasting
        predictions_xgb = pd.Series(model.predict(Test), name="XGBoost")

        # save predictions_xgb to csv
        predictions_xgb.to_csv("predictions_xgb.csv")

        # Adjust the Prophet forecast with the residuals predicted by XGBoost
        test_set["adjusted_forecast"] = test_set["yhat"] + predictions_xgb

        # save test_set to csv
        test_set.to_csv("test_set.csv")

        predictions_xgb.index = test_set.ds

        # Set up index
        training_set.index = training_set.ds
        test_set.index = test_set.ds

        # Vizualization
        # plt.show()

        # Assessment

        # MAE and RMSE
        from sklearn.metrics import mean_absolute_error, mean_squared_error

        # print("MAE: ")
        # print(round(mean_absolute_error(test_set['residuals'], predictions_xgb), 0))

        # print("RMSE: ")
        # print(round(np.sqrt(mean_squared_error(test_set['residuals'], predictions_xgb)), 0))

        # Plot the feature importance
        # plt.show()

        # Extract feature importances
        gain = model.get_score(importance_type="gain")
        cover = model.get_score(importance_type="cover")

        # Convert to DataFrame for better visualization
        importance_df = pd.DataFrame(
            {
                "Feature": list(gain.keys()),
                "Gain": list(gain.values()),
                "Cover": list(cover.values()),
            }
        ).sort_values(by="Gain", ascending=False)

        # print(importance_df)

        # how well is the model doing on unseen data?
        # Convert pandas DataFrame to DMatrix format
        dtrain = xgb.DMatrix(X_train)
        dval = xgb.DMatrix(X_test)

        # Now use these DMatrix objects for predictions
        train_preds = model.predict(dtrain)
        val_preds = model.predict(dval)

        train_rmse = mean_squared_error(y_train, train_preds, squared=False)
        val_rmse = mean_squared_error(y_test, val_preds, squared=False)

        print(f"Training RMSE: {train_rmse}")
        print(f"Validation RMSE: {val_rmse}")

        # add manual predictions for holidays we don't have data for. This must be an imported table later
        # Identify the row for the holiday in the forecast DataFrame
        oslo_pride_mainday = forecast[
            forecast["ds"] == pd.to_datetime("2023-07-01")
        ]  # replace with the date of your holiday
        oslo_pride_minusone = forecast[
            forecast["ds"] == pd.to_datetime("2023-06-30")
        ]

        multiplier_data = tourist_data[restaurant]
        temp_df = pd.DataFrame()
        for month, multiplier in multiplier_data.items():
            temp_df = forecast[
                (forecast["ds"].dt.month_name() == month)
                & (forecast["ds"].dt.year == 2023)  # Replace with the desired year
            ].copy()
            temp_df["yhat"] *= float(multiplier)
            forecast.loc[temp_df.index, "yhat"] *= float(multiplier)
        # Update the prediction for the holiday
        forecast.loc[oslo_pride_mainday.index, "yhat"] *= 1.20
        forecast.loc[oslo_pride_minusone.index, "yhat"] *= 1.20

        # df_cv = cross_validation(m, initial='640 days', period='7 days', horizon='30 days')

        # df_p = performance_metrics(df_cv)
        # selected_metrics = df_p[['horizon', 'rmse', 'mae', 'smape']]
        # selected_metrics = df_p[['horizon', 'rmse']]
        # print(selected_metrics)

        from sklearn.metrics import mean_squared_error
        from math import sqrt

        # Filter the forecast to only the dates present in the original dataset
        forecast_filtered = forecast[forecast["ds"].isin(df["ds"])]

        # Join the original and forecast dataframes to align y and yhat
        merged = pd.merge(df, forecast_filtered, on="ds", how="inner")
        test_set.to_csv('1234.csv')
        # Compute RMSE
        # rmse = sqrt(mean_squared_error(merged['y'], merged['yhat']))
        rmse_original = sqrt(mean_squared_error(test_set["y"], test_set["yhat"]))
        # Remove rows where either 'y' or 'adjusted_forecast' contains NaN
        valid_rows = ~test_set["y"].isna() & ~test_set["adjusted_forecast"].isna()
        filtered_test_set = test_set[valid_rows]
        rmse_adjusted = sqrt(
            mean_squared_error(
                filtered_test_set["y"], filtered_test_set["adjusted_forecast"]
            )
        )

        print("Original RMSE: ", rmse_original)
        print("Adjusted RMSE: ", rmse_adjusted)

    # print(forecast[forecast['sentrum_scene_concerts'] != 0]['sentrum_scene_concerts'])
    # df_p['rmse'] = np.exp(df_p['rmse'])
    # print(df_p)

    # forecast[['ds','yhat','yhat_lower','yhat_upper']]

    # Set the date column as the index
    # df.set_index('ds', inplace=True)

    # month_plot(df['y'].resample(rule='MS').mean())

    forecast.to_csv("forecast.csv")

    # Calculate the median of the logarithmic values
    log_median = df["y"].median()
    # Convert the median back to its original scale
    original_median = np.exp(log_median)
    # print(original_median)

    # create a pandas dataframe of the forecasst
    forecast = pd.DataFrame(forecast)


    # create a residual df that we use in a gradient booster model that captures weather effect
    # 2. Subtract those forecasts from your target variable to get the residuals
    df["residuals"] = df["y"] - forecast["yhat"]
    # Export the residuals dataframe to a .csv file
    df[["ds", "residuals"]].to_csv("residuals.csv", index=False)
    return forecast

   