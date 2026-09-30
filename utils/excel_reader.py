import pandas as pd


def read_test_metadata(file_path):
    df = pd.read_excel(file_path, sheet_name="test_cases")
    df.columns = [str(c).strip().lower() for c in df.columns]
    df = df.fillna("")
    records = df.to_dict(orient="records")
    return [r for r in records if str(r.get("active", "Y")).strip().upper() == "Y"]
