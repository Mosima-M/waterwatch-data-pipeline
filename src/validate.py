
import pandas as pd

from .config import REPORTS_DIR


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
