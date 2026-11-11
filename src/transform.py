
import pandas as pd

from .config import PROCESSED_DIR, REPORTS_DIR


def transform_data(valid, meters, buildings):
    print("\n[TRANSFORM] Cleaning and transforming data...")

    clean = valid.copy()

    clean["reading_timestamp"] = (
        clean["parsed_timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    )

    clean = clean.drop(columns=["parsed_timestamp", "rejection_reason"])

    clean = clean.merge(
        meters[["meter_id", "building_id"]],
        on="meter_id",
        how="left"
    )

    clean = clean.merge(
        buildings[["building_id", "building_name", "location", "building_type"]],
        on="building_id",
        how="left"
    )

    clean["reading_date"] = pd.to_datetime(
        clean["reading_timestamp"]
    ).dt.date.astype(str)

    daily = (
        clean.groupby(
            ["reading_date", "building_id", "building_name"],
            as_index=False
        )
        .agg(
            total_consumption_litres=("consumption_litres", "sum"),
            number_of_readings=("reading_id", "count")
        )
    )

    median_usage = daily.groupby("building_id")[
        "total_consumption_litres"
    ].transform("median")

    daily["potential_anomaly"] = (
        daily["total_consumption_litres"] > median_usage * 1.5
    )

    daily.to_csv(
        PROCESSED_DIR / "daily_consumption.csv",
        index=False
    )

    daily[daily["potential_anomaly"]].to_csv(
        REPORTS_DIR / "anomaly_flags.csv",
        index=False
    )

    print(f"Daily consumption records created: {len(daily)}")

    return clean, daily
