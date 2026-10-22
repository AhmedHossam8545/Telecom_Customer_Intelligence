# Data layers

| Layer | Path | Git | Rule |
| --- | --- | --- | --- |
| Raw | `data/raw/` | ignored | Immutable originals |
| Interim | `data/interim/` | ignored | ETL scratch |
| Processed | `data/processed/` | committed | Features, scores, Power BI extract |

Do not overwrite raw files. Do not commit `.env`.
