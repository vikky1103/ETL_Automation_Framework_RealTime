# Data-Driven ETL Automation Framework – Snowflake

यह framework उस setup के लिए है जहाँ **Source data, transformation और DWH target सभी Snowflake में हैं**। Python/PyTest framework generic है; सामान्यतः नया test case जोड़ने के लिए केवल `test_data/etl_metadata.xlsx` और `SQL/etl_queries.sql` update करने हैं।

## Architecture
```
Snowflake Source/Landing
        |
        | SQL validation queries
        v
Snowflake Transformation/Staging
        |
        v
Snowflake DWH
        |
        v
PyTest + Pandas
        |
        +-- Count validation
        +-- Null validation
        +-- Duplicate validation
        +-- Business-rule validation
        +-- Source-to-target DATA_DIFF
        |
        +-- HTML report
        +-- failed_records CSV
        +-- execution log
        |
        v
Jenkins CI/CD
```

## What changes for a new test?
1. Add SQL blocks in `SQL/etl_queries.sql`.
2. Add one row in `test_data/etl_metadata.xlsx`.
3. Run `pytest`.
4. No new Python test method is normally required.

## Metadata columns
- `test_id`: unique test case ID
- `active`: Y/N
- `test_description`: business-readable description
- `validation_type`: COUNT / NULL_CHECK / DUPLICATE_CHECK / BUSINESS_RULE / DATA_DIFF
- `query_key`: scalar validation SQL key
- `source_query_key`, `target_query_key`: used by DATA_DIFF
- `key_column`: primary/business key for DATA_DIFF or duplicate validation
- `expected_value`: expected result, normally 0 for defect checks
- `severity`: reporting/triage metadata
- `layer`: LANDING / STAGING / DWH / SOURCE_TO_TARGET

## Snowflake configuration
Set environment variables rather than hard-coding credentials:
`SNOWFLAKE_USER`, `SNOWFLAKE_PASSWORD`, `SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_WAREHOUSE`, `SNOWFLAKE_DATABASE`, `SNOWFLAKE_SCHEMA`, optional `SNOWFLAKE_ROLE`.

## Important design rule
**Code = framework engine. Excel = test inventory. SQL = validation logic.**
इसलिए source/target table या business rule बदलने पर सामान्यतः Python code नहीं बदलना चाहिए।
