
import sqlite3
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DATABASE_DIR = ROOT / "database"
REPORTS_DIR = ROOT / "reports"

for directory in [PROCESSED_DIR, DATABASE_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "waterwatch.db"


# --------------------------------------------------
# 2. EXTRACT: READ CSV FILES
# --------------------------------------------------

def extract_data():
    print("\n[EXTRACT] Reading source CSV files...")

    buildings = pd.read_csv(RAW_DIR / "buildings.csv", dtype=str)
    meters = pd.read_csv(RAW_DIR / "meters.csv", dtype=str)
    readings = pd.read_csv(RAW_DIR / "readings.csv", dtype=str)

    print(f"Buildings extracted: {len(buildings)}")
    print(f"Meters extracted: {len(meters)}")
    print(f"Readings extracted: {len(readings)}")

    return buildings, meters, readings


# --------------------------------------------------
# 3. VALIDATE: IDENTIFY BAD RECORDS
# --------------------------------------------------

def validate_readings(readings, meters):
    print("\n[VALIDATE] Checking reading quality...")

    data = readings.copy()

    known_meter_ids = set(meters["meter_id"].dropna())

    data["consumption_litres"] = pd.to_numeric(
        data["consumption_litres"],
        errors="coerce"
    )

    data["parsed_timestamp"] = pd.to_datetime(
        data["reading_timestamp"],
        errors="coerce"
    )

    data["rejection_reason"] = ""

    def add_reason(mask, reason):
        data.loc[mask, "rejection_reason"] += reason + "; "

    add_reason(
        data["reading_id"].isna() | (data["reading_id"].str.strip() == ""),
        "Missing reading ID"
    )

    add_reason(
        data["reading_id"].duplicated(keep="first"),
        "Duplicate reading ID"
    )

    add_reason(
        data["meter_id"].isna() | (data["meter_id"].str.strip() == ""),
        "Missing meter ID"
    )

    add_reason(
        ~data["meter_id"].isin(known_meter_ids)
        & data["meter_id"].notna()
        & (data["meter_id"].str.strip() != ""),
        "Unknown meter ID"
    )

    add_reason(
        data["parsed_timestamp"].isna(),
        "Invalid timestamp"
    )

    add_reason(
        data["consumption_litres"].isna(),
        "Invalid consumption value"
    )

    add_reason(
        data["consumption_litres"] < 0,
        "Negative consumption"
    )

    valid = data[data["rejection_reason"] == ""].copy()

    rejected = data[data["rejection_reason"] != ""].copy()

    rejected.to_csv(
        REPORTS_DIR / "rejected_readings.csv",
        index=False
    )

    print(f"Valid readings: {len(valid)}")
    print(f"Rejected readings: {len(rejected)}")

    return valid, rejected


# --------------------------------------------------
# 4. TRANSFORM: CLEAN AND AGGREGATE
# --------------------------------------------------

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

    # Flag daily usage above 1.5 times the building's median.
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


# --------------------------------------------------
# 5. LOAD: STORE DATA IN SQLITE
# --------------------------------------------------

def load_data(buildings, meters, clean, daily):
    print("\n[LOAD] Loading data into SQLite...")

    with sqlite3.connect(DATABASE_PATH) as connection:

        buildings.to_sql(
            "buildings",
            connection,
            if_exists="replace",
            index=False
        )

        meters.to_sql(
            "meters",
            connection,
            if_exists="replace",
            index=False
        )

        clean.to_sql(
            "readings",
            connection,
            if_exists="replace",
            index=False
        )

        daily.to_sql(
            "daily_consumption",
            connection,
            if_exists="replace",
            index=False
        )

    print(f"Database created/updated: {DATABASE_PATH}")


# --------------------------------------------------
# 6. ANALYTICS AND REPORTING
# --------------------------------------------------

def generate_reports(valid, rejected, daily):
    print("\n[ANALYTICS] Generating reports...")

    total = len(valid) + len(rejected)
    valid_count = len(valid)
    rejected_count = len(rejected)

    quality_score = (
        (valid_count / total) * 100 if total > 0 else 0
    )

    report = f"""
WATERWATCH DATA QUALITY REPORT
================================

Total records processed: {total}
Valid records: {valid_count}
Rejected records: {rejected_count}

Data quality score: {quality_score:.2f}%

Total recorded water consumption:
{valid["consumption_litres"].sum():.2f} litres

Daily consumption records: {len(daily)}
Potential anomalies detected: {daily["potential_anomaly"].sum()}

Note: Potential anomalies are unusual consumption patterns,
not confirmed water leaks.
"""

    with open(
        REPORTS_DIR / "data_quality_report.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(report)

    # Generate consumption chart
    total_by_date = daily.groupby("reading_date")[
        "total_consumption_litres"
    ].sum()

    plt.figure(figsize=(10, 5))
    total_by_date.plot(kind="line", marker="o")
    plt.title("WaterWatch Daily Water Consumption")
    plt.xlabel("Date")
    plt.ylabel("Consumption (litres)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(REPORTS_DIR / "consumption_trend.png")
    plt.close()

    print(report)
    print("Reports and chart generated successfully.")


# --------------------------------------------------
# 7. RUN THE COMPLETE PIPELINE
# --------------------------------------------------

def main():
    print("===================================")
    print("       WATERWATCH PIPELINE")
    print("===================================")

    buildings, meters, readings = extract_data()

    valid, rejected = validate_readings(readings, meters)

    clean, daily = transform_data(valid, meters, buildings)

    load_data(buildings, meters, clean, daily)

    generate_reports(valid, rejected, daily)

    print("\n===================================")
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("===================================")


if __name__ == "__main__":
    main()
