# Architecture

```text
Kaggle customer tables
  customer_info / usage_data / churn_labels
          |
          v
     data/raw/  (immutable)
          |
          v
  Validation + cleaning (notebooks)
          |
          v
     data/processed/
          |
          +------------------+
          |                  |
          v                  v
   PostgreSQL (Supabase)   Python
   SQL analytics           Feature engineering
          |                  |
          |                  +-- Segmentation (K-Means)
          |                  +-- Churn models + SHAP-style importance
          |                  +-- Customer value + retention tiers
          |
          +--------+---------+
                   |
                   v
            Serving layer
          +------+-------+
          |              |
          v              v
      Power BI       Streamlit
      dashboard/     app/app.py
```

## Layers

| Layer | Location | Role |
| --- | --- | --- |
| Raw | `data/raw/` | Original files, not overwritten |
| Processed | `data/processed/` | Cleaned tables, features, scores |
| Database | Supabase PostgreSQL | `core.customers`, `core.customer_usage`, `core.churn_labels` |
| SQL | `sql/analytics/` | Business queries; results logged in `notebooks/05_sql_analytics.ipynb` |
| Models | `models/` | Comparison metrics, feature importance, metadata |
| BI | `dashboard/` | `Customer Churn Report.pbix` and screenshot |
| App | `app/app.py` | Customer lookup, retention explorer, model summary |

Credentials are environment variables only (`.env`, never committed).
