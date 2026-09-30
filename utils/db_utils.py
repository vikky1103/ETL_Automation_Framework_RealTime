import snowflake.connector
from config.config import SNOWFLAKE_CONFIG


class DBUtils:
    def __init__(self):
        config = {k: v for k, v in SNOWFLAKE_CONFIG.items() if v not in (None, "")}
        self.conn = snowflake.connector.connect(**config)

    def execute_scalar(self, query):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query)
            row = cursor.fetchone()
            if row is None:
                raise AssertionError("SQL query returned no result.")
            return row[0]
        finally:
            cursor.close()

    def close(self):
        self.conn.close()
