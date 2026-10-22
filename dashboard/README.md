# Power BI — Customer Churn Analysis

- Report: `Customer Churn Report.pbix`
- Screenshot: `image.png`
- Data: `data/processed/powerbi_customer_intelligence.csv`

The published view is one executive page: **Customer Churn Analysis**. Slicers at the left filter **churn** (All / 0 / 1) and **Tenure Months**.


## Headline KPIs (slicers = All)

| KPI | Value |
| --- | --- |
| Number of customers | **10,000** |
| Sum of churns | **786** |
| Churn rate | **~0.08** (8%) |

The gauge sits near 0.08 on a 0–1 scale, in line with 786 / 10,000.

## Mix visuals (what the donuts show)

**Region** — almost even: Suburban **34.02%**, Rural **33.11%**, Urban **32.87%**. Churn risk is not concentrated in one geography.

**Gender** — Female **50.22%**, Male **49.78%**. No material gender skew in the base.

**Contract type** — Prepaid **40.41%**, Monthly **39.53%**, Yearly **20.06%**. Most customers are prepaid or month-to-month; yearly is the smallest book.

**Tenure cohort**

| Cohort | Share |
| --- | --- |
| 2. Mid-term | **53.89%** |
| 3. Loyal | **37.17%** |
| 1. New | **8.94%** |

The portfolio is mostly mid-term and loyal. New customers are a small slice of headcount.

## Distributions (what the bars show)

**Age group** — **Unknown** is the largest bar (about 3,000+ customers), then 21–30 through >60 in a declining staircase, and **&lt;20** the smallest. Missing age is a first-class segment on this page, not hidden.

**Monthly spend group** — mass of the base is **$30–$50** and **$50–$70** (each near 4,000). **&lt;$30** and **$70–$90** are much smaller; **&gt;$90** is rare.

**Call minutes group** — **400–600 min** dominates (about 6,000+). **200–400 min** and **&gt;600 min** are similar secondary groups. **&lt;200 min** is almost empty.

## How to read the page

1. Leave slicers on **All** for the portfolio snapshot above.
2. Set **churn = 1** to compare the same mix among the 786 churners (region, contract, tenure, spend, usage).
3. Use **Tenure Months** when you need a narrower tenure cut than the New / Mid-term / Loyal donut.

## Insights to carry into the write-up

- Observed churn is **7.86%** of 10k customers — a minority event.
- **Contract and tenure** are the mix dimensions that actually move (yearly is only ~20% of customers; new tenure is only ~9%). Region and gender do not.
- **Typical usage and spend** are mid-range ($30–$70, 400–600 call minutes), so outliers on spend or very low usage are sparse.
- **Unknown age** is the biggest age bucket; any age-based targeting must handle missingness.
