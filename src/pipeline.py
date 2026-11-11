
from .extract import extract_data
from .validate import validate_readings
from .transform import transform_data
from .load import load_data
from .analytics import generate_reports


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

