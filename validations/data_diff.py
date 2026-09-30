import logging
import pandas as pd

logger = logging.getLogger(__name__)


def _normalize(value):
    if pd.isna(value):
        return None
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value.strip() if isinstance(value, str) else value


def compare_source_vs_target(connection, source_query, target_query, key_column):
    src = pd.read_sql(source_query, connection)
    tgt = pd.read_sql(target_query, connection)
    src.columns = [str(c).upper() for c in src.columns]
    tgt.columns = [str(c).upper() for c in tgt.columns]
    key = key_column.upper()

    if key not in src.columns or key not in tgt.columns:
        raise AssertionError(f"Key column '{key}' must exist in both source and target queries.")
    if src[key].duplicated().any():
        raise AssertionError(f"Duplicate key found in source DATA_DIFF query: {key}")
    if tgt[key].duplicated().any():
        raise AssertionError(f"Duplicate key found in target DATA_DIFF query: {key}")

    src = src.set_index(key)
    tgt = tgt.set_index(key)
    all_keys = src.index.union(tgt.index)
    common_cols = [c for c in src.columns if c in tgt.columns]
    failures = []

    for k in all_keys:
        if k not in src.index:
            failures.append({key: k, "MISMATCH_TYPE": "TARGET_ONLY"})
            continue
        if k not in tgt.index:
            failures.append({key: k, "MISMATCH_TYPE": "SOURCE_ONLY"})
            continue
        for col in common_cols:
            s, t = _normalize(src.at[k, col]), _normalize(tgt.at[k, col])
            if s != t:
                failures.append({key: k, "COLUMN": col, "SOURCE_VALUE": s, "TARGET_VALUE": t, "MISMATCH_TYPE": "VALUE_MISMATCH"})

    diff = pd.DataFrame(failures)
    return len(diff), diff
