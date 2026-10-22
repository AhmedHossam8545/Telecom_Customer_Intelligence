# Data sources

## A. Customer behavioral data

Intended source: [Kaggle telecom customer churn data-quality challenge](https://www.kaggle.com/competitions/telecom-customer-churn-data-quality-challenge)

Expected tables:

- `customer_info`: customer_id, demographics, signup/tenure, contract, monthly charges
- `usage_data`: customer_id, month, call minutes, data usage GB, SMS, complaints
- `churn_labels`: customer_id, observation end date, churn

**Milestone 1** must inspect provenance, license, missingness, temporal coverage, synthetic vs real, and whether prediction features exist before the churn event. Do not use the data until that review is written here.

## B. Egyptian telecom market data

**Cancelled.** Not collected.
