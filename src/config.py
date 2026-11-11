
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
DATABASE_DIR = ROOT / "database"
REPORTS_DIR = ROOT / "reports"

DATABASE_PATH = DATABASE_DIR / "waterwatch.db"

for directory in [PROCESSED_DIR, DATABASE_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
