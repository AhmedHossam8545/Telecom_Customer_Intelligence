# CV project summary

**Telecom Customer Intelligence & Retention Platform**  
End-to-end data science project: quality checks, PostgreSQL/SQL analytics, features, clustering, churn modeling, value-based retention, Power BI, and Streamlit.

## Problem

A telecom needs to know who is likely to leave, which accounts are worth saving, and how to brief retention teams — without claiming a precision the data cannot support.

## Data

- Source: Kaggle telecom churn / data-quality challenge (likely synthetic; documented).
- **10,000** customers, **~120,060** monthly usage rows (2023), churn rate **7.86%**.
- Stack: Python, pandas, scikit-learn, XGBoost, PostgreSQL (Supabase), Power BI, Streamlit.

## What I built

- Validated schema, missingness, duplicates, and temporal-leakage risk.
- Loaded cleaned tables to Postgres and wrote SQL for churn, tenure, usage, revenue, and a value/risk proxy.
- Engineered behavioral features (means, trends, volatility, complaints, tenure, usage-to-charge).
- K-Means segmentation (K=2; weak silhouette, reported honestly).
- Logistic regression, random forest, XGBoost with an out-of-fold threshold; **ROC-AUC ~0.49** — documented as experimental.
- Customer value proxy + four retention tiers (Critical / High / Medium / Low).
- Power BI report and a Streamlit app (lookup, priority explorer, model summary).

## Results a recruiter can quote

- Complete 10k-customer coverage in SQL (0 missing usage or churn links).
- Yearly contracts: **8.82%** churn vs **7.56%** monthly.
- Usage *averages* do not separate churners; volatility features rank higher in importance.
- Retention file: 1,000 Critical / 2,000 High; ~$6.0M annualized charges, ~$463K expected revenue at risk (model-based, not a guarantee).

## Skills

Python, pandas, SQL/PostgreSQL, data quality, feature engineering, K-Means, classification metrics, SHAP-style importance, Power BI, Streamlit, Git.

## Honest limitation

Churn labels have no event date; models do not beat chance on ROC-AUC. The project’s value is the **pipeline, SQL, governance, and decision layer**, not a production churn score.
