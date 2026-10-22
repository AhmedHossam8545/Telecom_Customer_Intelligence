from pathlib import Path

import pytest

from src.config import PROJECT_ROOT
from src.market_intelligence.collectors import (
    MarketCollectionCancelledError,
    collect_operator_plans,
)


def test_power_bi_files_exist():
    dash = PROJECT_ROOT / "dashboard"
    assert (dash / "Customer Churn Report.pbix").is_file()
    assert (dash / "image.png").is_file()


def test_processed_serving_files_exist():
    processed = PROJECT_ROOT / "data" / "processed"
    for name in (
        "customer_features_clustered.csv",
        "customer_retention_priority.csv",
        "powerbi_customer_intelligence.csv",
    ):
        assert (processed / name).is_file()


def test_model_metric_files_exist():
    models = PROJECT_ROOT / "models"
    for name in (
        "churn_model_comparison.csv",
        "churn_model_metadata.json",
        "churn_feature_importance_rf.csv",
    ):
        assert (models / name).is_file()


def test_closing_docs_exist():
    docs = PROJECT_ROOT / "docs"
    for name in (
        "final_recommendations.md",
        "cv_project_summary.md",
        "architecture.md",
        "scope.md",
    ):
        assert (docs / name).is_file()


def test_market_collection_is_cancelled():
    with pytest.raises(MarketCollectionCancelledError):
        collect_operator_plans()
