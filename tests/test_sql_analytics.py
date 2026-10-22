from src.config import PROJECT_ROOT
from src.db import list_analytics_files


def test_analytics_files_exist():
    files = list_analytics_files()
    names = [path.name for path in files]
    assert names == [
        "00_load_checks.sql",
        "01_churn_rate_by_contract.sql",
        "02_churn_by_tenure_bucket.sql",
        "03_average_usage_by_churn.sql",
        "04_complaints_by_contract_region.sql",
        "05_revenue_by_contract_region.sql",
        "06_high_value_high_risk.sql",
        "07_retention_priority_counts.sql",
    ]


def test_analytics_sql_has_no_secrets_and_uses_customer_tables():
    for path in list_analytics_files():
        sql = path.read_text(encoding="utf-8").lower()
        assert "password" not in sql
        assert "customers" in sql or "customer_usage" in sql or "churn" in sql


def test_schema_file_still_present():
    assert (PROJECT_ROOT / "sql" / "schema.sql").exists()
