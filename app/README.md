# Streamlit app

Live app: `app.py`  
Milestone notes: `notebooks/15_streamlit_app.ipynb`

```bash
streamlit run app/app.py
```

Needs these committed files:

- `data/processed/customer_features_clustered.csv`
- `data/processed/customer_retention_priority.csv`
- `models/churn_feature_importance_rf.csv`
- `models/churn_feature_importance_lr.csv`
- `models/churn_model_comparison.csv`

## Pages

- Customer lookup: profile, usage, segment, churn probability, retention priority  
- Retention priority explorer: filter/sort by Critical / High / Medium / Low  
- Model and portfolio summary  

Screenshots will be added under `docs/screenshots/` later. There is no market-comparison page.
