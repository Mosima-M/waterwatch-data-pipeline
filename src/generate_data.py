
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Make generated data reproducible
random.seed(42)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)


def generate_buildings():
    buildings = [
        ["B001", "Sunrise Apartments", "Johannesburg", "Residential"],
        ["B002", "Central Offices", "Pretoria", "Commercial"],
        ["B003", "Green Valley School", "Soweto", "Educational"],
        ["B004", "Riverside Complex", "Sandton", "Residential"],
    ]

    with open(RAW_DATA_DIR / "buildings.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["building_id", "building_name", "location", "building_type"])
        writer.writerows(buildings)

    return buildings


def generate_meters(buildings):
    meters = []

    for building_index, building in enumerate(buildings, start=1):
        for meter_number in range(1, 3):
            meter_id = f"M{building_index:03d}{meter_number:02d}"
            installation_date = f"2024-0{meter_number}-15"

            meters.append([
                meter_id,
                building[0],
                installation_date
            ])

    with open(RAW_DATA_DIR / "meters.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["meter_id", "building_id", "installation_date"])
        writer.writerows(meters)

    return meters


def generate_readings(meters):
    readings = []
    reading_number = 1

    start_date = datetime(2026, 10, 1)

    for day in range(7):
        for meter in meters:
            timestamp = start_date + timedelta(days=day)
            timestamp += timedelta(hours=random.randint(0, 23))

            consumption = round(random.uniform(100, 900), 2)

            readings.append([
                f"R{reading_number:04d}",
                meter[0],
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                consumption
            ])

            reading_number += 1

    # Introduce intentional data-quality problems

    readings.append([
        "R9991", "M00101", "2026-10-08 10:00:00", -150
    ])

    readings.append([
        "R9992", "UNKNOWN", "2026-10-08 11:00:00", 350
    ])

    readings.append([
        "R9993", "", "2026-10-08 12:00:00", 200
    ])

    readings.append([
        "R9994", "M00101", "invalid-date", 400
    ])

    readings.append([
        "R9995", "M00101", "2026-10-08 14:00:00", 500
    ])

    # Duplicate reading ID
    readings.append([
        "R9995", "M00102", "2026-10-08 15:00:00", 600
    ])

    with open(RAW_DATA_DIR / "readings.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "reading_id",
            "meter_id",
            "reading_timestamp",
            "consumption_litres"
        ])
        writer.writerows(readings)

    return readings


def main():
    buildings = generate_buildings()
    meters = generate_meters(buildings)
    readings = generate_readings(meters)

    print("WaterWatch synthetic data generated successfully!")
    print(f"Buildings: {len(buildings)}")
    print(f"Meters: {len(meters)}")
    print(f"Readings: {len(readings)}")
    print(f"Output directory: {RAW_DATA_DIR}")


if __name__ == "__main__":
    main()
