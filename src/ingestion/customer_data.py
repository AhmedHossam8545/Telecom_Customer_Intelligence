"""Customer dataset ingestion stubs.

Milestone 2 will download/copy the Kaggle three-table dataset into data/raw/
after source validation in milestone 1.
"""

from pathlib import Path

from src.config import PROJECT_ROOT


RAW_DIR = PROJECT_ROOT / "data" / "raw"


def raw_customer_paths() -> dict[str, Path]:
    """Expected raw files once the customer source is ingested."""
    return {
        "customer_info": RAW_DIR / "customer_info.csv",
        "usage_data": RAW_DIR / "usage_data.csv",
        "churn_labels": RAW_DIR / "churn_labels.csv",
    }
