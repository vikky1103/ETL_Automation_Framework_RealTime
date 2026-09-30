from pathlib import Path
import logging

logger = logging.getLogger(__name__)
FAILED_DATA_DIR = Path("reports/failed_data")


def dump_failed_records(df, test_id):
    if df is None or df.empty:
        return None
    FAILED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    path = FAILED_DATA_DIR / f"{test_id}_failed_records.csv"
    df.to_csv(path, index=False)
    return str(path)
