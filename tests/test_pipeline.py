
import pandas as pd

import src.validate as validation
import src.transform as transformation

from src.validate import validate_readings
from src.transform import transform_data


def test_validation_rejects_invalid_records(tmp_path, monkeypatch):
    monkeypatch.setattr(validation, "REPORTS_DIR", tmp_path)

    meters = pd.DataFrame({
        "meter_id": ["M001"],
        "building_id": ["B001"]
    })

    readings = pd.DataFrame([
        ["R001", "M001", "2026-10-01 10:00:00", "200"],
        ["R002", "UNKNOWN", "2026-10-01 11:00:00", "300"],
        ["R003", "M001", "invalid-date", "400"],
        ["R004", "M001", "2026-10-01 12:00:00", "-100"],
        ["R005", "", "2026-10-01 13:00:00", "200"],
    ], columns=[
        "reading_id",
        "meter_id",
        "reading_timestamp",
        "consumption_litres"
    ])

    valid, rejected = validate_readings(readings, meters)

    assert len(valid) == 1
    assert len(rejected) == 4


def test_transformation_creates_daily_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(transformation, "PROCESSED_DIR", tmp_path)
    monkeypatch.setattr(transformation, "REPORTS_DIR", tmp_path)

    valid = pd.DataFrame({
        "reading_id": ["R001", "R002"],
        "meter_id": ["M001", "M001"],
        "reading_timestamp": [
            "2026-10-01 10:00:00",
            "2026-10-01 11:00:00"
        ],
        "consumption_litres": [200.0, 300.0],
        "parsed_timestamp": pd.to_datetime([
            "2026-10-01 10:00:00",
            "2026-10-01 11:00:00"
        ]),
        "rejection_reason": ["", ""]
    })

    meters = pd.DataFrame({
        "meter_id": ["M001"],
        "building_id": ["B001"]
    })

    buildings = pd.DataFrame({
        "building_id": ["B001"],
        "building_name": ["Test Building"],
        "location": ["Johannesburg"],
        "building_type": ["Residential"]
    })

    clean, daily = transform_data(valid, meters, buildings)

    assert len(clean) == 2
    assert len(daily) == 1
    assert daily.iloc[0]["total_consumption_litres"] == 500.0

