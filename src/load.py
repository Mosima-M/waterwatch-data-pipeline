
import sqlite3

from .config import DATABASE_PATH


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
