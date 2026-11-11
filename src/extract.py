import pandas as pd

from .config import RAW_DIR


def extract_data():
    print("\n[EXTRACT] Reading source CSV files...")

    buildings = pd.read_csv(RAW_DIR / "buildings.csv", dtype=str)
    meters = pd.read_csv(RAW_DIR / "meters.csv", dtype=str)
    readings = pd.read_csv(RAW_DIR / "readings.csv", dtype=str)

    print(f"Buildings extracted: {len(buildings)}")
    print(f"Meters extracted: {len(meters)}")
    print(f"Readings extracted: {len(readings)}")

    return buildings, meters, readings
