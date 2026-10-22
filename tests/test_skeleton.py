"""Skeleton tests. Expand as each milestone is implemented."""

from src.config import PROJECT_ROOT, get_settings
from src.ingestion.customer_data import raw_customer_paths


def test_project_root_exists():
    assert (PROJECT_ROOT / "requirements.txt").exists()
    assert (PROJECT_ROOT / "sql" / "schema.sql").exists()


def test_data_layers_exist():
    for layer in ("raw", "interim", "processed"):
        assert (PROJECT_ROOT / "data" / layer).is_dir()


def test_settings_load_without_env_file():
    settings = get_settings()
    assert settings.postgres_db
    assert settings.postgres_port > 0


def test_expected_raw_customer_filenames():
    paths = raw_customer_paths()
    assert set(paths) == {"customer_info", "usage_data", "churn_labels"}
    for path in paths.values():
        assert path.parent.name == "raw"
