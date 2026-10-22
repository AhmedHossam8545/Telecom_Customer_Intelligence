# Final business recommendations

Based on **SQL analytics** (`notebooks/05_sql_analytics.ipynb`) and the **Power BI Customer Churn Analysis** page (`dashboard/image.png`). Not based on machine-learning scores.

Portfolio: **10,000** customers, **120,060** usage rows, **786** churners. Load checks: **0** customers missing usage or churn labels. Observed churn rate **7.86%** (Power BI gauge ~0.08).

## Which customers are most likely to churn?

SQL churn **rate** is highest for **Yearly** contracts (**8.82%**, 177 of 2,006), then Prepaid (**7.67%**) and Monthly (**7.56%**). Yearly is only ~**20%** of the book in Power BI, so it is a **rate** problem more than a **volume** problem. Prepaid and Monthly still produce most churners in absolute terms (310 and 299) because they are larger.

SQL tenure **rates** are close together (about **7.4–8.2%**). The highest rates are **12–23 months (8.15%)** and **24–35 months (8.12%)**, not the newest customers (**0–11 months, 7.38%**). The **48+ month** group has the most churners (**301**) because it is the largest (3,791). Power BI shows the same shape in headcount: mid-term **53.89%**, loyal **37.17%**, new **8.94%**.

**Do this:** Review **Yearly renewal** experience. Do not run a “new-customer only” save campaign; the data does not show that new tenure is the riskiest.

## What behaviors precede churn?

SQL averages for churners vs retained customers are almost the same: call minutes **494.75 vs 492.22**, data **9.87 vs 9.90 GB**, SMS **24.84 vs 24.50**, complaints **0.51 vs 0.50**.

Power BI shows why: most of the base already sits in the same usage/spend band (**400–600 call minutes**, monthly spend **$30–$70**). Complaints by contract × region are also tight (**0.49–0.53** average monthly complaints).

**Do this:** Do not target on “low usage” or “high complaints” using portfolio averages. Those splits do not mark churners. Use the Power BI **churn = 1** slicer only to confirm mix, not as a usage rule.

## What customer segments exist?

Power BI mix (all customers):

- **Region:** Suburban 34.02%, Rural 33.11%, Urban 32.87% — even; geography is not a targeting axis.
- **Gender:** Female 50.22%, Male 49.78% — even.
- **Contract:** Prepaid 40.41%, Monthly 39.53%, Yearly 20.06%.
- **Age:** **Unknown** is the largest age bar (~3,000+). Age-based offers need a missing-age path.
- **Spend:** Almost all value sits in **$30–$50** and **$50–$70**; **>$90** is rare.

SQL revenue follows **headcount**, not ARPU. Average monthly charges are ~**50–52** in every contract × region cell. The largest **monthly revenue** groups are Monthly–Suburban (**70,906**), Prepaid–Urban (**70,008**), Prepaid–Suburban (**68,309**). Yearly groups are smaller because there are fewer yearly customers, not because they pay less per month (Yearly–Rural average charge is actually highest at **51.97**).

**Do this:** Protect the large Prepaid/Monthly pools for revenue. Use Yearly as a **retention-rate** watch list, not as the main revenue engine.

## Which customers are high-value and high-risk?

SQL value/risk **proxy** (top-quartile charges, plus above-average complaints or observed churn) — not a predicted probability:

| SQL priority | Customers |
| --- | --- |
| Critical | **1,057** |
| Maintain | **1,445** |
| Standard | **3,363** |
| Low priority | **4,135** |

The SQL Critical **sample** includes monthly charges of **101–370** versus a typical ~**51** in Power BI and SQL averages. Treat those rows as **high bill and/or data-quality flags**, then confirm in the source.

**Do this:** Work the **1,057 Critical** SQL list first. Inside it, prefer **observed churners** and **Yearly** accounts. Spot-check extreme charges before offering discounts.

## How should retention be prioritized?

1. **Critical SQL list (1,057)** — personal follow-up; check Yearly renewals and outlier bills.
2. **Maintain (1,445)** — high charges, lower observed risk; keep them with ordinary care, do not over-incentivize.
3. **Standard (3,363)** — complaints or churn without high charges; cheaper, process-style contact if anything.
4. **Low priority (4,135)** — no extra campaign.

Use Power BI slicers to brief ops: portfolio on **All**, then **churn = 1** to see whether the 786 leavers look like the base (they will, on usage). Keep **Unknown age** visible; do not drop those customers from outreach.

## Data-quality notes that affect the recommendations

- Complete customer coverage in SQL (10k / 10k / 10k, no orphans).
- **Unknown age** dominates the age chart — do not build an age offer as the main lever.
- Extreme monthly charges in the Critical sample need a billing audit.
- Currency is not labeled in SQL; treat revenue figures as **charge units**, not a named currency, unless the Power BI model defines one.
