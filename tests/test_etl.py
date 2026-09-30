import logging
from pathlib import Path

import pandas as pd
import pytest

from utils.db_utils import DBUtils
from utils.excel_reader import read_test_metadata
from utils.sql_reader import load_queries
from utils.report_utils import dump_failed_records
from validations.data_diff import compare_source_vs_target
from validations.etl_validations import validate

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]
METADATA_FILE = ROOT / "test_data" / "etl_metadata.xlsx"
SQL_FILE = ROOT / "SQL" / "etl_queries.sql"
metadata = read_test_metadata(METADATA_FILE)
queries = load_queries(SQL_FILE)


@pytest.fixture(scope="session")
def snowflake_connection():
    db = DBUtils()
    try:
        yield db.conn
    finally:
        db.close()


def scalar(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        row = cursor.fetchone()
        if row is None:
            raise AssertionError("SQL query returned no result.")
        return row[0]
    finally:
        cursor.close()


def required_query(key):
    if key not in queries:
        raise AssertionError(f"Query key '{key}' not found in SQL file.")
    return queries[key]


def norm(v):
    if pd.isna(v):
        return None
    try:
        n = float(v)
        return int(n) if n.is_integer() else n
    except (TypeError, ValueError):
        return str(v).strip()


@pytest.mark.parametrize("test_case", metadata, ids=[r["test_id"] for r in metadata])
def test_etl_data_driven(snowflake_connection, test_case):
    test_id = test_case["test_id"]
    description = test_case["test_description"]
    validation_type = str(test_case["validation_type"]).strip().upper()
    expected = norm(test_case.get("expected_value", 0))
    key = str(test_case.get("key_column", "")).strip()
    logger.info("START %s | %s", test_id, description)

    if validation_type == "DATA_DIFF":
        src_key = test_case.get("source_query_key") or f'{test_case["query_key"]}_SRC'
        tgt_key = test_case.get("target_query_key") or f'{test_case["query_key"]}_TGT'
        actual, diff = compare_source_vs_target(
            snowflake_connection, required_query(src_key), required_query(tgt_key), key
        )
        if norm(actual) != expected:
            dump = dump_failed_records(diff, test_id)
            pytest.fail(f"{test_id} failed | DATA_DIFF | Actual={actual} | Expected={expected} | Dump={dump}")
        return

    query_key = test_case["query_key"]
    actual = norm(scalar(snowflake_connection, required_query(query_key)))
    try:
        validate(actual, expected, validation_type)
    except AssertionError as exc:
        detail_key = f"{query_key}_RECORDS"
        dump = None
        if detail_key in queries:
            df = pd.read_sql(queries[detail_key], snowflake_connection)
            dump = dump_failed_records(df, test_id)
        pytest.fail(f"{test_id} failed | {exc} | Dump={dump}")
