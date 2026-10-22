# Telecom Customer Intelligence & Retention Platform

End-to-end telecom data science project: customer quality checks, PostgreSQL analytics, behavioral features, segmentation, churn modeling, value-based retention, a Power BI report, and a Streamlit app.

**Status:** complete for the in-scope customer workstream.  

## Highlights

- **10,000** customers, **~120k** monthly usage rows, **7.86%** churn
- SQL analytics on Supabase (`core.customers`, `core.customer_usage`, `core.churn_labels`)
- Features: tenure, usage trends/volatility, complaints, usage-to-charge
- K-Means (K=2; weak cluster separation, reported as such)
- Logistic regression, random forest, XGBoost — **ROC-AUC ~0.49** (experimental, not production)
- Retention tiers: 1,000 Critical / 2,000 High / 3,000 Medium / 4,000 Low
- Power BI: `dashboard/Customer Churn Report.pbix` (screenshot: `dashboard/image.png`)
- Streamlit: `app/app.py` (documented in `notebooks/15_streamlit_app.ipynb`; screenshots to be added)

Read **`docs/final_recommendations.md`** and **`docs/cv_project_summary.md`** for the portfolio write-up.

## Business questions (in scope)

- Which customers are most likely to churn?
- What behaviors precede churn?
- What customer segments exist?
- Which customers are high-value and high-risk?
- How should retention priorities be assigned?

## Repository layout

```text
data/processed/     cleaned tables, features, retention scores (committed)
sql/                schema + analytics queries
src/                config, db helpers, cancelled market stub
notebooks/          validation → features → models → Streamlit notes
dashboard/          Power BI file + screenshot
app/app.py          Streamlit app
models/             metrics and feature-importance CSVs
docs/               architecture, recommendations, CV summary
tests/
```

Raw files stay local (`data/raw/` is gitignored). Processed outputs needed to run the app are committed.

## Setup

```bash
git clone <your-repo-url>
cd telecom-customer-intelligence
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

`.env` is only required if you reconnect to Supabase. The Streamlit app and notebooks that read CSVs do not need the database.

## Run Streamlit

```bash
streamlit run app/app.py
```

Pages: customer lookup, retention priority explorer, model and portfolio summary.

## Open Power BI

1. Open `dashboard/Customer Churn Report.pbix`
2. If asked to refresh, point at `data/processed/powerbi_customer_intelligence.csv` (or `telecom_customer_churn_powerbi.csv`)
3. Screenshot of the report: `dashboard/image.png`

## SQL analytics

Queries: `sql/analytics/00_*.sql` … `07_*.sql`  
Pasted results and notes: `notebooks/05_sql_analytics.ipynb`

## Tests

```bash
pytest
```

## Documentation

| Doc | Purpose |
| --- | --- |
| `docs/architecture.md` | System diagram |
| `docs/data_source_validation.md` | License/schema/leakage caveats |
| `docs/final_recommendations.md` | Business conclusions |
| `docs/cv_project_summary.md` | One-pager for CVs |
| `docs/scope.md` | In scope vs cancelled market |
| `PROJECT_PLAN.md` | Original plan with scope updates |

## GitHub notes

Do not commit `.env` or `.venv`.  
Do not put database passwords in notebooks.  
Streamlit screenshots can go in `docs/screenshots/` when you have them.

## Honest limitation

Churn has no event timestamp. Predictive models do not beat chance on ROC-AUC. The useful output is the **data pipeline, SQL, quality work, and retention ranking process**.
