import os


SNOWFLAKE_CONFIG = {
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "database": os.getenv("SNOWFLAKE_DATABASE", "ETL_PRACTICE_DB"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA", "STAGING_SCHEMA"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
}
