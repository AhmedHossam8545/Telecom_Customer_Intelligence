# Telecom Customer Intelligence & Retention Platform

## Goal
Build an end-to-end telecom Data Science platform combining customer behavioral analytics, segmentation, churn prediction, customer value, explainable AI, SQL, Power BI, and Streamlit. Egyptian telecom market collection is cancelled.

## Business Questions
- Which customers are most likely to churn?
- What behaviors precede churn?
- What customer segments exist?
- Which customers are high-value and high-risk?
- How should retention priorities be assigned?

## Data Strategy

### A. Customer Behavioral Data
Preferred structure:
- `customer_info`: customer_id, demographics, signup/tenure, contract, monthly charges
- `usage_data`: customer_id, month, call minutes, data usage GB, SMS, complaints
- `churn_labels`: customer_id, observation end date, churn

A current Kaggle telecom data-quality challenge provides this three-table structure and monthly behavioral features. Before using it, inspect provenance, license, missingness, temporal coverage, and whether it is synthetic. Most importantly, verify that features used for prediction are available before the churn event.

Source: https://www.kaggle.com/competitions/telecom-customer-churn-data-quality-challenge


### B. Egyptian Telecom Market Data

**Cancelled.** No operator plan collection, scraping, or market comparison is in this project.

## Architecture

```text
Customer Dataset
        |
        v
   Raw Data Layer
        |
        v
    Validation
        |
        v
   PostgreSQL (Supabase)
        |
        +---------------+
        |               |
        v               v
  SQL Analytics      Python
                        |
                        v
               Feature Engineering
                        |
           +------------+------------+
           |            |            |
           v            v            v
      Segmentation   Churn ML      Customer Value
           |            |            |
           +------------+------------+
                        v
                  SHAP / XAI
                        |
                        v
               Retention Priority
                        |
                  +-----+-----+
                  |           |
                  v           v
              Power BI    Streamlit
```

## PostgreSQL Schema

Core tables:
- `customers`
- `customer_usage`
- `churn_labels`
- `customer_services`
Market tables were planned and then cancelled.

Use PK/FK constraints, indexes, staging tables, and validation queries.

## SQL Analytics
Implement meaningful queries such as:
- churn rate by contract
- churn by tenure bucket
- average usage by churn status
- complaints by segment
- high-value/high-risk customers
- revenue by segment
- (market price-per-GB and operator comparisons cancelled)

SQL must be a real analytical component, not just storage.

## Feature Engineering

Customer-level features:
- tenure
- average/recent/min/max usage
- usage trends
- recent usage decline
- usage volatility
- complaint frequency
- active months
- service count
- monthly charges
- usage-to-charge ratios

Avoid target leakage. For temporal data, build features from an observation window and predict churn in a future window.

## Customer Segmentation
Start with K-Means.
Evaluate with:
- Silhouette Score
- Davies-Bouldin Index
- cluster stability
- business interpretability

Possible segment interpretations should be discovered after clustering, not hardcoded beforehand.

## Churn Prediction
Models:
1. Logistic Regression baseline
2. Random Forest
3. XGBoost
4. Optional LightGBM

Metrics:
- Precision
- Recall
- F1
- ROC-AUC
- PR-AUC
- confusion matrix

Use temporal validation when temporal data is available.

## Customer Value
Do not claim true CLV unless the data supports a defensible CLV model.

Start with a transparent Customer Value Proxy using:
- monthly revenue
- tenure
- usage
- service count

Later upgrade to formal CLV if suitable historical data becomes available.

## Retention Prioritization

```text
Churn Risk + Customer Value -> Retention Priority
```

Example tiers:
- High value + high risk = Critical
- High value + low risk = Maintain
- Low value + high risk = Standard
- Low value + low risk = Low priority

## Explainable AI
Use SHAP for:
- global feature importance
- individual customer explanations
- positive/negative contributors
- churn probability



## Power BI Pages
1. Executive Overview
2. Customer Behavior
3. Customer Segmentation
4. Churn Intelligence
5. Retention Prioritization



## Streamlit
Customer lookup:
- profile
- usage history
- segment
- churn probability
- SHAP explanation
- retention priority


## Project Structure

```text
telecom-customer-intelligence/
├── data/raw/
├── data/interim/
├── data/processed/
├── sql/
├── src/
│   ├── ingestion/
│   ├── etl/
│   ├── features/
│   ├── segmentation/
│   ├── churn/
│   ├── explainability/
│   └── market_intelligence/
├── notebooks/
├── dashboard/
├── app/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── PROJECT_PLAN.md
```

## Milestones

1. Project setup + data-source validation
2. Customer dataset ingestion
3. Data quality and validation
4. PostgreSQL schema + loading
5. SQL analytics
6. EDA
7. Behavioral feature engineering
8. Customer segmentation
9. Temporal churn prediction
10. Customer value + retention prioritization
11. SHAP explainability
14. Power BI dashboard
15. Streamlit application
16. Testing + documentation + CV packaging
12–13. Egyptian market collection — **cancelled**

## Rules
- Inspect the repository before modifying it.
- Implement one milestone at a time.
- Do not jump ahead.
- Keep raw data immutable.
- Separate ingestion, ETL, modeling, and visualization.
- Never hardcode credentials.
- Validate data after every major transformation.
- Log ingestion/ETL operations.
- Prevent temporal leakage.
- Add tests for important transformations.
- Do not fabricate missing data.
- If a source is unavailable, report it instead of silently replacing it.
- Run tests/validation before declaring a milestone complete.
- Prefer simple, maintainable Python.

## Final Deliverables
- Data ingestion pipeline
- Raw/processed data layers
- PostgreSQL database
- SQL analytics
- EDA
- feature engineering
- customer segmentation
- churn model
- temporal validation
- SHAP explainability
- customer value scoring
- retention prioritization
- Power BI dashboard
- Streamlit application
- tests and documentation
- architecture diagram
- final business recommendations

## Scope Rule
Do not build everything at once. Start with the customer data source and validate it thoroughly. Modeling comes only after the data foundation is reliable. Egyptian market collection is cancelled.
