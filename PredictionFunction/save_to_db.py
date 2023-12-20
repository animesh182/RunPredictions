import datetime


def save_to_db(forecast_df,company,restaurant):
    unwanted_columns = [
        "_lower",
        "_upper",
        "Unnamed",
        "custom_regressor",
        "extra_regressors_additive",
        "trend",
        "additive_terms",
        "yearly",
        "index",
        "0",
        "holidays",
        "weekly_1",
        "weekly_2",
        "weekly_3",
        "weekly_4",
        "weekly_5",
        "weekly_6",
    ]
    filtered_columns = [
        col
        for col in forecast_df.columns
        if not any(unwanted in col for unwanted in unwanted_columns)
    ]
    filtered_df = forecast_df[filtered_columns]

    # filtered_df = forecast_df

    if prediction_category == "day":
        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(row["ds"], "%Y-%m-%d")
            total_gross_value = (
                round(float(row["yhat"] / 500)) * 500
            )  # Round to the nearest 500
            prediction_instance = Predictions(
                company=company,
                restaurant=restaurant,
                date=date_obj.date(),
                total_gross=total_gross_value,
            )
            prediction_instance.save()

            # Save the holiday parameters for this prediction instance
            for name in filtered_df.columns:
                if name in ["ds", "yhat"]:
                    continue
                effect_value = (
                    round(float(row[name]))
                    if row[name] not in [None, "", np.nan]
                    else 0
                )
                if effect_value != 0:
                    holiday_instance = HolidayParameters.objects.create(
                        prediction=prediction_instance,
                        name=name,
                        effect=effect_value,
                        date=date_obj,
                        restaurant=restaurant,
                        company=company,
                    )

    elif prediction_category == "hour":
        latest_hours = defaultdict(dict)
        max_created_at_subquery = (
            Predictions.objects.filter(
                date=OuterRef("date"),
                restaurant=restaurant,
                company=company,
            )
            .order_by("-created_at")
            .values("created_at")[:1]
        )

        # Use the subquery to annotate the queryset with the maximum 'created_at' value
        predictions = Predictions.objects.annotate(
            max_created_at=Subquery(max_created_at_subquery)
        ).filter(
            created_at=F(
                "max_created_at"
            )  # Filter by rows where 'created_at' matches the maximum value
        )
        daily_hourly_sum = defaultdict(float)

        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(row["ds"], "%Y-%m-%d %H:%M:%S")
            day_type = (
                "weekend" if date_obj.weekday() >= 5 else "weekday"
            )  # 5 and 6 are Saturday and Sunday

            restaurant_name = restaurant
            restaurant_uuid = Restaurant.objects.get(name=restaurant_name).id
            default_starting_hour = time(11, 0)  # 11:00 AM
            default_ending_hour = time(23, 0)  # 11:00 PM

            try:
                # Try to fetch the latest opening hours for the restaurant
                opening_hours = OpeningHours.objects.filter(
                    restaurant=restaurant_uuid,
                    is_weekend=True if day_type == "weekend" else False,
                    start_date__lte=date_obj,
                    end_date__gte=date_obj,
                ).latest("created_at")

                # Extract the actual starting and ending hours
                opening_hour = opening_hours.starting_hour
                closing_hour = opening_hours.ending_hour

            except OpeningHours.DoesNotExist:
                # If no opening hours are found, use the default hours
                opening_hour = default_starting_hour
                closing_hour = default_ending_hour

            if opening_hour and closing_hour:
                opening_hour = int(opening_hour)
                closing_hour = int(closing_hour)
                if not is_within_hours(date_obj, opening_hour, closing_hour):
                    filtered_df.at[index, "yhat"] = 0
            else:
                filtered_df.at[index, "yhat"] = 0

        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(
                row["ds"], "%Y-%m-%d %H:%M:%S"
            ).date()
            daily_hourly_sum[date_obj] += float(row["yhat"])
        scaling_factors = {}
        for date, hourly_sum in daily_hourly_sum.items():
            # Replace 'Predictions' with the actual model name if needed
            daily_total = (
                predictions.filter(date=date).values("total_gross").first()
            )
            daily_total = daily_total["total_gross"] if daily_total else 0

            # Convert both 'daily_total' and 'hourly_sum' to the Decimal data type
            daily_total = Decimal(str(daily_total))  # Convert to Decimal
            hourly_sum = Decimal(str(hourly_sum))  # Convert to Decimal

            scaling_factors[date] = (
                daily_total / hourly_sum if hourly_sum != 0 else 0
            )

        # print(scaling_factors)
        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(row["ds"], "%Y-%m-%d %H:%M:%S")
            day_type = (
                "weekend" if date_obj.weekday() >= 5 else "weekday"
            )  # 5 and 6 are Saturday and Sunday
            restaurant_name = (
                restaurant  # Assuming 'restaurant' is a string with the name
            )
            scale_factor = scaling_factors.get(
                date_obj.date(), 1
            )  # Default to 1 if no scaling factor
            # Get operating hours for the specific restaurant and day type
            # Check if the restaurant hours are defined

            total_gross_value = (
                (Decimal(row["yhat"]) * scale_factor)
                if scale_factor
                else Decimal(row["yhat"])
            )
            # Round to the scaled daily predictions

            # print(
            #    f"{date_obj.date()}{date_obj.time()}:Opening Hour:{opening_hour},Closing Hour:{closing_hour},{total_gross_value},{scale_factor}"
            # )
            prediction_instance = PredictionsByHour(
                company=company,
                restaurant=restaurant,
                date=date_obj.date(),
                hour=date_obj.time(),
                total_gross=total_gross_value,
            )
            prediction_instance.save()

    elif prediction_category == "type":
        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(row["ds"], "%Y-%m-%d")
            total_prediction = round(float(row["yhat"]))
            prediction_instance = TypePrediction(
                company=company,
                restaurant=restaurant,
                date=date_obj.date(),
                take_out=total_prediction,
            )
            prediction_instance.save()

        # Here, you can add logic for saving associated parameters if needed

    elif prediction_category == "product":
        for index, row in filtered_df.iterrows():
            date_obj = datetime.datetime.strptime(row["ds"], "%Y-%m-%d")
            total_prediction = round(float(row["yhat"]))
            prediction_instance = ProductMixPrediction(
                company=company,
                restaurant=restaurant,
                date=date_obj.date(),
                product_mix=total_prediction,
            )
            prediction_instance.save()

        # Here, you can add logic for saving associated parameters if needed

    print(f"Finished prediction for {restaurant} of {company}")