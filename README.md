# Data-Driven ETL Automation Framework – Snowflake

This framework is designed for an ETL testing setup where **source data, transformations, and the DWH target are all hosted in Snowflake**.

The framework is built using **Python and PyTest** and follows a data-driven approach. In most cases, adding a new ETL test case requires updating only the `test_data/etl_metadata.xlsx` file and the `SQL/etl_queries.sql` file. No new Python test method is normally required.

## Architecture

```text
Snowflake Source / Landing
          |
          | SQL Validation Queries
          v
Snowflake Transformation / Staging
          |
          v
Snowflake DWH
          |
          v
     PyTest + Pandas
          |
          +-- Count Validation
          +-- Null Validation
          +-- Duplicate Validation
          +-- Business Rule Validation
          +-- Source-to-Target DATA_DIFF
          |
          +-- HTML Report
          +-- Failed Records CSV
          +-- Execution Log
          |
          v
     Jenkins CI/CD
```

## Key Features

* Data-driven ETL test execution
* Snowflake source-to-target validation
* SQL-based validation framework
* PyTest-based automation
* Pandas-based result processing
* Count validation
* Null validation
* Duplicate validation
* Business-rule validation
* Source-to-target data comparison
* Failed-record extraction
* HTML test reports
* Execution logging
* Jenkins CI/CD integration

## What Changes for a New Test Case?

For most new ETL test cases, only the following files need to be updated:

1. Add the required SQL validation block to `SQL/etl_queries.sql`.
2. Add one test-case row to `test_data/etl_metadata.xlsx`.
3. Run the PyTest test suite.

No new Python test method is normally required.

## Metadata Configuration

The `test_data/etl_metadata.xlsx` file acts as the **test inventory** for the framework.

| Column             | Description                                                                                   |
| ------------------ | --------------------------------------------------------------------------------------------- |
| `test_id`          | Unique test case ID                                                                           |
| `active`           | Indicates whether the test case is active (`Y/N`)                                             |
| `test_description` | Business-readable description of the validation                                               |
| `validation_type`  | Type of validation: `COUNT`, `NULL_CHECK`, `DUPLICATE_CHECK`, `BUSINESS_RULE`, or `DATA_DIFF` |
| `query_key`        | Key used to identify the SQL query for scalar validations                                     |
| `source_query_key` | SQL query key used to retrieve source data for `DATA_DIFF` validation                         |
| `target_query_key` | SQL query key used to retrieve target data for `DATA_DIFF` validation                         |
| `key_column`       | Primary/business key used for data comparison or duplicate validation                         |
| `expected_value`   | Expected validation result, normally `0` for defect checks                                    |
| `severity`         | Severity level used for reporting and defect triage                                           |
| `layer`            | Data layer being validated: `LANDING`, `STAGING`, `DWH`, or `SOURCE_TO_TARGET`                |

## Snowflake Configuration

Snowflake credentials and connection details should be configured using **environment variables** rather than hard-coded values.

```text
SNOWFLAKE_USER
SNOWFLAKE_PASSWORD
SNOWFLAKE_ACCOUNT
SNOWFLAKE_WAREHOUSE
SNOWFLAKE_DATABASE
SNOWFLAKE_SCHEMA
SNOWFLAKE_ROLE       # Optional
```

This approach helps keep sensitive credentials outside the source code and makes the framework easier to configure across different environments.

## Framework Design Principle

The framework follows a simple separation of responsibilities:

```text
Code     = Framework Engine
Excel    = Test Inventory
SQL      = Validation Logic
```

Therefore, when a source/target table, validation condition, or business rule changes, the **Python framework code should normally remain unchanged**.

This makes the framework easier to maintain, scale, and reuse across multiple ETL test scenarios.

## Validation Types

### 1. Count Validation

Validates whether the expected number of records exists in the source and target.

```text
Source Count = Target Count
```

### 2. Null Validation

Identifies unexpected `NULL` values in mandatory or business-critical columns.

```text
Expected NULL Count = 0
```

### 3. Duplicate Validation

Checks for duplicate records based on a primary key or business key.

```text
Expected Duplicate Count = 0
```

### 4. Business Rule Validation

Validates business-specific transformation and data-quality rules.

Examples include:

* Valid status values
* Correct calculated amounts
* Valid date ranges
* Mandatory field conditions
* Transformation-specific rules

### 5. Source-to-Target DATA_DIFF

Compares source and target records using a primary/business key and identifies data mismatches.

Typical comparison flow:

```text
Source Data
    |
    v
Key-based Comparison
    |
    v
Target Data
    |
    v
DATA_DIFF
    |
    +-- Missing Records
    +-- Extra Records
    +-- Column Value Mismatches
```

## Execution Flow

```text
Read Test Metadata
        |
        v
Filter Active Test Cases
        |
        v
Identify Validation Type
        |
        v
Fetch SQL Query
        |
        v
Execute Query on Snowflake
        |
        v
Process Results using Pandas
        |
        v
Perform Assertions
        |
        v
Generate Reports / Logs
        |
        v
Publish Results through Jenkins
```

## CI/CD Integration

The framework can be integrated with **Jenkins** to automate ETL validation as part of the CI/CD pipeline.

A typical execution flow is:

```text
Developer / Scheduler
        |
        v
Jenkins Pipeline
        |
        v
Checkout Test Framework
        |
        v
Execute PyTest
        |
        v
Connect to Snowflake
        |
        v
Execute ETL Validations
        |
        v
Generate Reports
        |
        v
Publish Test Results
```

## Project Structure

A typical project structure can look like this:

```text
ETL-Automation-Framework/
│
├── SQL/
│   └── etl_queries.sql
│
├── test_data/
│   └── etl_metadata.xlsx
│
├── tests/
│   └── test_etl.py
│
├── utils/
│   ├── snowflake_connection.py
│   ├── query_executor.py
│   └── validation_utils.py
│
├── reports/
│   └── html_report.html
│
├── failed_records/
│   └── failed_records.csv
│
├── logs/
│   └── execution.log
│
├── requirements.txt
└── README.md
```

## Benefits

* Reduces duplicate Python code
* Supports reusable validation logic
* Makes test cases configuration-driven
* Simplifies maintenance
* Enables scalable ETL test automation
* Separates test data, SQL logic, and framework code
* Supports CI/CD execution through Jenkins
* Provides detailed test reports and failure records

## Summary

The framework uses a **data-driven and configuration-based approach** for ETL automation testing.

The core philosophy is:

```text
Python/PyTest  → Framework Engine
Excel          → Test Case Configuration
SQL            → Validation Logic
Pandas         → Result/Data Processing
Snowflake      → Data Platform
Jenkins        → CI/CD Execution
```

This design allows new ETL validation scenarios to be added with minimal or no changes to the core Python automation code.
