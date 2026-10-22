"""
Telecom Customer Intelligence & Retention Platform
Streamlit Application — Milestone 15
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Telecom Intelligence Platform",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Constants ──────────────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

TIER_COLORS = {
    "Critical": "#d62728",
    "High":     "#ff7f0e",
    "Medium":   "#2196F3",
    "Low":      "#4caf50",
}
TIER_ICONS = {
    "Critical": "🔴",
    "High":     "🟠",
    "Medium":   "🔵",
    "Low":      "🟢",
}

# ─── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---------- global ---------- */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    background: #0f1117;
    color: #e0e0e0;
}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1a1d2e 0%, #0f1117 100%);
    border-right: 1px solid #2a2d3e;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #c9d1d9 !important;
}

/* ---------- metric cards ---------- */
.metric-card {
    background: linear-gradient(135deg, #1e2030 0%, #16192a 100%);
    border-radius: 12px;
    padding: 18px 22px;
    border: 1px solid #2a2d3e;
    margin-bottom: 10px;
}
.metric-card .label  { font-size: 0.78rem; color: #8b949e; text-transform: uppercase; letter-spacing: 0.06em; }
.metric-card .value  { font-size: 1.8rem; font-weight: 700; margin-top: 4px; }
.metric-card .sub    { font-size: 0.82rem; color: #8b949e; margin-top: 4px; }

/* ---------- tier badges ---------- */
.badge-critical { background:#d62728;  color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }
.badge-high     { background:#ff7f0e;  color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }
.badge-medium   { background:#2196F3;  color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }
.badge-low      { background:#4caf50;  color:#fff; padding:4px 14px; border-radius:20px; font-weight:700; font-size:0.85rem; }

/* ---------- section headers ---------- */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #58a6ff;
    border-bottom: 1px solid #2a2d3e;
    padding-bottom: 6px;
    margin-bottom: 14px;
    margin-top: 10px;
}

/* ---------- recommendation box ---------- */
.rec-box {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    border-left: 4px solid #58a6ff;
    border-radius: 8px;
    padding: 14px 18px;
    font-size: 0.93rem;
    line-height: 1.6;
    color: #c9d1d9;
}

/* ---------- dataframe overrides ---------- */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ---------- progress bar ---------- */
.stProgress > div > div > div { border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ─── Data Loaders ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading customer data…")
def load_data():
    df_feat = pd.read_csv(DATA_DIR / "customer_features_clustered.csv")
    df_pri  = pd.read_csv(DATA_DIR / "customer_retention_priority.csv")

    # Merge — keep clean versions from retention file
    df = df_feat.merge(
        df_pri[["customer_id", "monthly_charges_clean", "estimated_historical_revenue",
                "annualized_revenue", "value_score", "predicted_churn_risk",
                "expected_revenue_at_risk", "retention_priority", "priority_tier",
                "retention_recommendation", "retention_rank"]],
        on="customer_id", how="left"
    )
    # Use original monthly_charges where clean version is available
    df["monthly_charges"] = df["monthly_charges_clean"].fillna(df["monthly_charges"])
    df.drop(columns=["monthly_charges_clean"], inplace=True)
    return df


@st.cache_data(show_spinner="Loading model artifacts…")
def load_model_data():
    fi_rf    = pd.read_csv(MODELS_DIR / "churn_feature_importance_rf.csv")
    fi_lr    = pd.read_csv(MODELS_DIR / "churn_feature_importance_lr.csv")
    model_cmp = pd.read_csv(MODELS_DIR / "churn_model_comparison.csv")

    # Clean feature names
    fi_rf["feature_clean"] = (fi_rf["feature"]
        .str.replace("num__", "", regex=False)
        .str.replace("cat__", "", regex=False)
        .str.replace("_", " ", regex=False).str.title())

    fi_lr["feature_clean"] = (fi_lr["feature"]
        .str.replace("num__", "", regex=False)
        .str.replace("cat__", "", regex=False)
        .str.replace("_", " ", regex=False).str.title())

    return fi_rf, fi_lr, model_cmp


# ─── Sidebar Navigation ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/80/satellite-signal.png", width=60)
    st.markdown("## 📡 Telecom Intelligence")
    st.markdown("**Customer Intelligence & Retention Platform**")
    st.markdown("---")

    page = st.radio(
        "Navigate",
        options=["🔍 Customer Lookup", "🎯 Retention Priority Explorer", "📊 Model & Portfolio Summary"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**Data Snapshot**")

    df = load_data()

    total = len(df)
    churn_rate = df["churn"].mean() * 100
    critical_n = (df["priority_tier"] == "Critical").sum()
    high_n     = (df["priority_tier"] == "High").sum()

    st.metric("Total Customers", f"{total:,}")
    st.metric("Overall Churn Rate", f"{churn_rate:.2f}%")
    st.metric("🔴 Critical Priority", f"{critical_n:,}")
    st.metric("🟠 High Priority", f"{high_n:,}")

    st.markdown("---")
    st.caption("Milestone 15 · Streamlit App")


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 1 — Customer Lookup
# ════════════════════════════════════════════════════════════════════════════════
if page == "🔍 Customer Lookup":
    st.title("🔍 Customer Lookup")
    st.markdown("Search any customer to view their full profile, churn risk assessment, and retention recommendation.")

    # Search bar
    col_search, col_btn = st.columns([4, 1])
    with col_search:
        query = st.text_input(
            "Customer ID",
            placeholder="e.g. CUST_1234",
            label_visibility="collapsed"
        )
    with col_btn:
        st.markdown("<br>", unsafe_allow_html=True)
        search = st.button("Search", use_container_width=True, type="primary")

    # Quick-pick random examples
    st.caption("Quick examples:")
    ex_cols = st.columns(8)
    examples = (df.groupby("priority_tier")
                .apply(lambda g: g.sample(2, random_state=42))
                .reset_index(drop=True)["customer_id"].tolist())
    example_clicked = None
    for i, ex in enumerate(examples[:8]):
        with ex_cols[i % 8]:
            if st.button(ex, key=f"ex_{i}", use_container_width=True):
                example_clicked = ex
                query = ex

    customer_id = example_clicked if example_clicked else query.strip()

    if not customer_id:
        st.info("Enter a Customer ID above or click one of the quick examples.")
        st.stop()

    row = df[df["customer_id"] == customer_id]
    if row.empty:
        st.error(f"No customer found with ID **{customer_id}**. Please check the ID and try again.")
        st.stop()

    row = row.iloc[0]
    tier = str(row.get("priority_tier", "Unknown"))
    tier_color = TIER_COLORS.get(tier, "#666")
    tier_icon  = TIER_ICONS.get(tier, "⚪")

    # ── Header Banner ──
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1d2e,#0f1117);
                border-radius:14px;padding:20px 28px;
                border:1px solid {tier_color}44;margin-bottom:18px;">
        <span style="font-size:1.6rem;font-weight:800;color:#e0e0e0;">{customer_id}</span>
        &nbsp;&nbsp;
        <span class="badge-{tier.lower()}">{tier_icon} {tier} Priority</span>
        &nbsp;&nbsp;
        <span style="color:#8b949e;font-size:0.9rem;">Retention Rank #{int(row.get('retention_rank', 0)):,} of 10,000</span>
    </div>
    """, unsafe_allow_html=True)

    # ── Top KPI Row ──
    k1, k2, k3, k4, k5 = st.columns(5)

    def kpi(col, label, value, sub="", color="#58a6ff"):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value" style="color:{color};">{value}</div>
            <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    churn_risk = float(row.get("predicted_churn_risk", 0))
    risk_color = "#d62728" if churn_risk > 0.15 else "#ff7f0e" if churn_risk > 0.10 else "#4caf50"

    kpi(k1, "Monthly Charges",    f"${row['monthly_charges']:.2f}",        "Current plan rate")
    kpi(k2, "Tenure",             f"{int(row['tenure_months'])} months",   f"~{row['tenure_months']/12:.1f} years")
    kpi(k3, "Churn Risk Score",   f"{churn_risk*100:.1f}%",                "OOF predicted risk", risk_color)
    kpi(k4, "Value Score",        f"{row['value_score']:.1f} / 100",       "Composite value index")
    kpi(k5, "Exp. Revenue at Risk", f"${row['expected_revenue_at_risk']:.2f}", "Annual expected loss")

    # ── Two-column layout ──
    left, right = st.columns([1, 1], gap="large")

    with left:
        # Profile
        st.markdown('<div class="section-header">👤 Customer Profile</div>', unsafe_allow_html=True)

        gender = str(row.get("gender", "N/A"))
        age_raw = row.get("age", None)
        age_str = f"{int(age_raw)} yrs" if pd.notna(age_raw) else "Unknown"
        cluster_map = {0: "Segment A — High Usage / Low Complaints", 1: "Segment B — Moderate Usage"}
        cluster_label = cluster_map.get(int(row.get("cluster", 0)), "Unknown Segment")

        profile_data = {
            "Field": ["Gender", "Age", "Region", "Contract", "Cluster / Segment",
                       "Active Months", "Complaints (Total)", "Recent Complaints (3M)"],
            "Value": [
                gender, age_str,
                str(row.get("region", "N/A")),
                str(row.get("contract_type", "N/A")),
                cluster_label,
                str(int(row.get("active_months", 0))),
                str(int(row.get("complaints_total", 0))),
                str(int(row.get("complaints_recent3", 0))),
            ]
        }
        st.dataframe(pd.DataFrame(profile_data), hide_index=True, use_container_width=True)

        # Financial
        st.markdown('<div class="section-header">💰 Financial Summary</div>', unsafe_allow_html=True)
        fin_data = {
            "Metric": ["Monthly Charges", "Annualized Revenue", "Est. Historical Revenue",
                        "Expected Annual Loss at Risk"],
            "Value": [
                f"${row['monthly_charges']:.2f}",
                f"${row.get('annualized_revenue', row['monthly_charges']*12):.2f}",
                f"${row.get('estimated_historical_revenue', 0):.2f}",
                f"${row.get('expected_revenue_at_risk', 0):.2f}",
            ]
        }
        st.dataframe(pd.DataFrame(fin_data), hide_index=True, use_container_width=True)

    with right:
        # Churn Risk Gauge
        st.markdown('<div class="section-header">📈 Churn Risk Assessment</div>', unsafe_allow_html=True)

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=churn_risk * 100,
            number={"suffix": "%", "font": {"size": 32, "color": "#e0e0e0"}},
            gauge={
                "axis": {"range": [0, 100], "tickfont": {"color": "#8b949e"}},
                "bar": {"color": risk_color, "thickness": 0.28},
                "bgcolor": "#1e2030",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 8],   "color": "#1e3a1e"},
                    {"range": [8, 15],  "color": "#3a2e10"},
                    {"range": [15, 100],"color": "#3a1010"},
                ],
                "threshold": {
                    "line": {"color": "white", "width": 2},
                    "thickness": 0.75,
                    "value": 7.86,
                }
            },
            title={"text": "OOF Predicted Churn Probability<br><sup>Baseline: 7.86% | White line = population avg</sup>",
                   "font": {"color": "#8b949e", "size": 12}},
        ))
        fig_gauge.update_layout(
            height=260,
            paper_bgcolor="#0f1117", plot_bgcolor="#0f1117",
            margin=dict(t=60, b=10, l=30, r=30)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Usage Metrics
        st.markdown('<div class="section-header">📡 Usage Behavior</div>', unsafe_allow_html=True)
        usage_metrics = pd.DataFrame({
            "Metric": ["Avg Call Minutes/Month", "Avg Data Usage (GB)", "Avg SMS Count",
                        "Call Minutes Trend", "Data Usage Trend"],
            "Value": [
                f"{row.get('call_minutes_mean', 0):.0f} min",
                f"{row.get('data_usage_gb_mean', 0):.2f} GB",
                f"{row.get('sms_count_mean', 0):.0f}",
                f"{'📈' if row.get('call_minutes_slope', 0) > 0 else '📉'} {row.get('call_minutes_slope', 0):.2f}",
                f"{'📈' if row.get('data_usage_gb_slope', 0) > 0 else '📉'} {row.get('data_usage_gb_slope', 0):.3f}",
            ]
        })
        st.dataframe(usage_metrics, hide_index=True, use_container_width=True)

    # ── Retention Recommendation ──
    st.markdown('<div class="section-header">🎯 Retention Strategy Recommendation</div>', unsafe_allow_html=True)
    rec = str(row.get("retention_recommendation", "No recommendation available."))
    st.markdown(f'<div class="rec-box">💡 {rec}</div>', unsafe_allow_html=True)

    # ── Usage Mini-Charts ──
    st.markdown('<div class="section-header">📊 Detailed Usage Distribution Context</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)

    for col_ui, metric, label, unit in [
        (c1, "call_minutes_mean", "Avg Monthly Call Minutes", "min"),
        (c2, "data_usage_gb_mean", "Avg Monthly Data (GB)", "GB"),
        (c3, "sms_count_mean", "Avg Monthly SMS", "msgs"),
    ]:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[metric].dropna(), nbinsx=40,
            marker_color="#2a3f5f", opacity=0.8, name="All Customers"
        ))
        fig.add_vline(
            x=row.get(metric, 0), line_color="#ff7f0e", line_width=2.5,
            annotation_text=f"This customer<br>{row.get(metric,0):.1f} {unit}",
            annotation_position="top right",
            annotation_font_color="#ff7f0e"
        )
        fig.update_layout(
            title=label, height=200,
            paper_bgcolor="#0f1117", plot_bgcolor="#1e2030",
            font=dict(color="#8b949e", size=10),
            margin=dict(t=40, b=10, l=10, r=10),
            showlegend=False,
            xaxis=dict(gridcolor="#2a2d3e"),
            yaxis=dict(gridcolor="#2a2d3e"),
        )
        col_ui.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 2 — Retention Priority Explorer
# ════════════════════════════════════════════════════════════════════════════════
elif page == "🎯 Retention Priority Explorer":
    st.title("🎯 Retention Priority Explorer")
    st.markdown("Browse, filter, and export customers by their operational priority tier.")

    # ── Tier Summary Cards ──
    tier_stats = df.groupby("priority_tier").agg(
        count=("customer_id", "count"),
        avg_value_score=("value_score", "mean"),
        avg_churn_risk=("predicted_churn_risk", "mean"),
        total_revenue_at_risk=("expected_revenue_at_risk", "sum"),
        actual_churn_rate=("churn", "mean"),
    ).reindex(["Critical", "High", "Medium", "Low"])

    cols = st.columns(4)
    for i, (tier_name, color) in enumerate(TIER_COLORS.items()):
        row_t = tier_stats.loc[tier_name]
        with cols[i]:
            st.markdown(f"""
            <div class="metric-card" style="border-top: 3px solid {color};">
                <div class="label">{TIER_ICONS[tier_name]} {tier_name} Priority</div>
                <div class="value" style="color:{color};">{int(row_t['count']):,}</div>
                <div class="sub">customers</div>
                <hr style="border-color:#2a2d3e;margin:8px 0;">
                <div class="sub">Avg Churn Risk: <strong>{row_t['avg_churn_risk']*100:.1f}%</strong></div>
                <div class="sub">Avg Value Score: <strong>{row_t['avg_value_score']:.1f}/100</strong></div>
                <div class="sub">Revenue at Risk: <strong>${row_t['total_revenue_at_risk']:,.0f}</strong></div>
                <div class="sub">Actual Churn Rate: <strong>{row_t['actual_churn_rate']*100:.1f}%</strong></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Filters ──
    st.markdown("### 🔧 Filter Customers")
    f1, f2, f3, f4 = st.columns([2, 2, 2, 2])

    with f1:
        selected_tiers = st.multiselect(
            "Priority Tier",
            options=["Critical", "High", "Medium", "Low"],
            default=["Critical", "High"],
            help="Filter customers by their operational retention priority tier"
        )
    with f2:
        contract_opts = ["All"] + sorted(df["contract_type"].dropna().unique().tolist())
        selected_contract = st.selectbox("Contract Type", contract_opts)

    with f3:
        region_opts = ["All"] + sorted(df["region"].dropna().unique().tolist())
        selected_region = st.selectbox("Region", region_opts)

    with f4:
        churn_filter = st.selectbox(
            "Actual Churn Status",
            options=["All", "Churned (1)", "Retained (0)"],
        )

    # Numeric sliders
    sl1, sl2 = st.columns(2)
    with sl1:
        min_charge, max_charge = float(df["monthly_charges"].min()), float(df["monthly_charges"].max())
        charge_range = st.slider("Monthly Charges ($)", min_charge, max_charge, (min_charge, max_charge))
    with sl2:
        min_risk = float(df["predicted_churn_risk"].min())
        max_risk = float(df["predicted_churn_risk"].max())
        risk_range = st.slider("Predicted Churn Risk (%)", 0.0, 100.0,
                               (min_risk * 100, max_risk * 100))

    # Apply filters
    mask = df["priority_tier"].isin(selected_tiers if selected_tiers else ["Critical", "High", "Medium", "Low"])
    if selected_contract != "All":
        mask &= df["contract_type"] == selected_contract
    if selected_region != "All":
        mask &= df["region"] == selected_region
    if churn_filter == "Churned (1)":
        mask &= df["churn"] == 1
    elif churn_filter == "Retained (0)":
        mask &= df["churn"] == 0
    mask &= (df["monthly_charges"] >= charge_range[0]) & (df["monthly_charges"] <= charge_range[1])
    mask &= (df["predicted_churn_risk"] * 100 >= risk_range[0]) & (df["predicted_churn_risk"] * 100 <= risk_range[1])

    filtered = df[mask].copy()

    # Sort
    sort_col, sort_dir_col = st.columns([3, 1])
    with sort_col:
        sort_by = st.selectbox(
            "Sort by",
            options=["retention_rank", "predicted_churn_risk", "value_score",
                     "expected_revenue_at_risk", "monthly_charges", "tenure_months"],
            index=0,
            format_func=lambda x: x.replace("_", " ").title()
        )
    with sort_dir_col:
        sort_asc = st.selectbox("Direction", ["Ascending", "Descending"], index=0 if sort_by == "retention_rank" else 1)

    filtered = filtered.sort_values(sort_by, ascending=(sort_asc == "Ascending"))

    st.markdown(f"**{len(filtered):,} customers** match your filters (of {len(df):,} total)")

    # ── Results Table ──
    display_cols = {
        "retention_rank": "Rank",
        "customer_id": "Customer ID",
        "priority_tier": "Tier",
        "monthly_charges": "Monthly ($)",
        "tenure_months": "Tenure (Mo)",
        "contract_type": "Contract",
        "region": "Region",
        "value_score": "Value Score",
        "predicted_churn_risk": "Churn Risk",
        "expected_revenue_at_risk": "Rev. at Risk ($)",
        "churn": "Actual Churn",
        "retention_recommendation": "Recommendation",
    }
    table_df = filtered[[c for c in display_cols if c in filtered.columns]].rename(columns=display_cols)
    if "Churn Risk" in table_df.columns:
        table_df["Churn Risk"] = (table_df["Churn Risk"] * 100).round(1).astype(str) + "%"
    if "Value Score" in table_df.columns:
        table_df["Value Score"] = table_df["Value Score"].round(1)
    if "Monthly ($)" in table_df.columns:
        table_df["Monthly ($)"] = table_df["Monthly ($)"].round(2)
    if "Rev. at Risk ($)" in table_df.columns:
        table_df["Rev. at Risk ($)"] = table_df["Rev. at Risk ($)"].round(2)

    st.dataframe(table_df.head(200), hide_index=True, use_container_width=True)
    if len(filtered) > 200:
        st.caption(f"Showing first 200 of {len(filtered):,} matching customers.")

    # Download button
    csv_bytes = filtered[[c for c in display_cols if c in filtered.columns]].rename(columns=display_cols).to_csv(index=False).encode("utf-8")
    st.download_button(
        label=f"⬇️ Download filtered list ({len(filtered):,} customers)",
        data=csv_bytes,
        file_name="filtered_retention_priority.csv",
        mime="text/csv",
        use_container_width=True,
    )

    # ── Tier Distribution Charts ──
    st.markdown("---")
    st.markdown("### 📈 Filtered Cohort Analysis")
    ch1, ch2, ch3 = st.columns(3)

    with ch1:
        tier_count = filtered["priority_tier"].value_counts().reindex(["Critical", "High", "Medium", "Low"]).fillna(0)
        fig_pie = px.pie(
            values=tier_count.values,
            names=tier_count.index,
            color=tier_count.index,
            color_discrete_map=TIER_COLORS,
            title="Tier Distribution (filtered)",
            hole=0.45,
        )
        fig_pie.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#0f1117",
                              font=dict(color="#c9d1d9"), height=280, margin=dict(t=40,b=10))
        st.plotly_chart(fig_pie, use_container_width=True)

    with ch2:
        fig_box = px.box(
            filtered, x="priority_tier", y="predicted_churn_risk",
            category_orders={"priority_tier": ["Critical", "High", "Medium", "Low"]},
            color="priority_tier", color_discrete_map=TIER_COLORS,
            title="Churn Risk Distribution by Tier",
        )
        fig_box.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#1e2030",
                              font=dict(color="#c9d1d9"), height=280,
                              showlegend=False, margin=dict(t=40,b=10),
                              xaxis=dict(gridcolor="#2a2d3e"),
                              yaxis=dict(gridcolor="#2a2d3e", tickformat=".0%"))
        st.plotly_chart(fig_box, use_container_width=True)

    with ch3:
        fig_scatter = px.scatter(
            filtered.sample(min(1000, len(filtered)), random_state=42),
            x="value_score", y="predicted_churn_risk",
            color="priority_tier", color_discrete_map=TIER_COLORS,
            opacity=0.6, size_max=6,
            title="Value Score vs. Churn Risk",
            labels={"value_score": "Value Score", "predicted_churn_risk": "Churn Risk"},
        )
        fig_scatter.update_layout(paper_bgcolor="#0f1117", plot_bgcolor="#1e2030",
                                  font=dict(color="#c9d1d9"), height=280,
                                  margin=dict(t=40,b=10),
                                  xaxis=dict(gridcolor="#2a2d3e"),
                                  yaxis=dict(gridcolor="#2a2d3e", tickformat=".0%"))
        st.plotly_chart(fig_scatter, use_container_width=True)


# ════════════════════════════════════════════════════════════════════════════════
# PAGE 3 — Model & Portfolio Summary
# ════════════════════════════════════════════════════════════════════════════════
elif page == "📊 Model & Portfolio Summary":
    st.title("📊 Model & Portfolio Summary")
    st.markdown("Churn model performance overview, feature importance, and portfolio-level retention economics.")

    fi_rf, fi_lr, model_cmp = load_model_data()

    # ── Portfolio KPIs ──
    st.markdown("### 💼 Portfolio Financial Overview")
    pk1, pk2, pk3, pk4, pk5 = st.columns(5)

    total_annual   = df["annualized_revenue"].sum()
    total_exp_loss = df["expected_revenue_at_risk"].sum()
    total_hist     = df["estimated_historical_revenue"].sum()
    churn_base     = df["churn"].mean()
    imputed_n      = 54  # from notebook 10 analysis

    def pkpi(col, label, value, sub="", color="#58a6ff"):
        col.markdown(f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value" style="color:{color};">{value}</div>
            <div class="sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

    pkpi(pk1, "Total Customers",        f"{len(df):,}",                  f"{imputed_n} imputed charges")
    pkpi(pk2, "Annualized Billing",     f"${total_annual/1e6:.2f}M",     "Portfolio run-rate")
    pkpi(pk3, "Expected Loss at Risk",  f"${total_exp_loss/1e3:.1f}K",   f"{total_exp_loss/total_annual*100:.2f}% of billing", "#d62728")
    pkpi(pk4, "Est. Historical Revenue",f"${total_hist/1e6:.1f}M",       "Cumulative past billing")
    pkpi(pk5, "Baseline Churn Rate",    f"{churn_base*100:.2f}%",        "786 churned / 10,000", "#ff7f0e")

    st.markdown("---")

    # ── Model Performance ──
    st.markdown("### 🤖 Churn Model Performance (Test Set)")

    tuned = model_cmp[model_cmp["Decision Rule"] == "Train-OOF Tuned"].copy()
    tuned = tuned[["Model", "ROC-AUC", "PR-AUC (AP)", "Precision", "Recall", "F1", "Brier", "Threshold"]].round(4)
    st.dataframe(tuned.reset_index(drop=True), hide_index=True, use_container_width=True)

    st.markdown("""
    <div class="rec-box">
    ⚠️ <strong>Model Diagnostic:</strong> All three models achieve ROC-AUC ≈ 0.49–0.49 and PR-AUC ≈ 0.077–0.081
    against a baseline prevalence of 7.86%. This confirms near-random discrimination capability. The pipeline is
    presented as an <em>experimental prototype</em>. Customer Value Score prioritization remains the primary
    actionable signal; predicted churn risk adds marginal information.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🔍 Feature Importance — Random Forest")

    m1, m2 = st.columns([2, 1])

    with m1:
        top_n = st.slider("Show top N features", 5, 36, 15)
        fi_plot = fi_rf.head(top_n).sort_values("importance")
        fig_fi = px.bar(
            fi_plot, x="importance", y="feature_clean",
            orientation="h", color="importance",
            color_continuous_scale="Blues",
            title=f"Top {top_n} Features by Random Forest Importance",
            labels={"importance": "Importance Score", "feature_clean": "Feature"},
        )
        fig_fi.update_layout(
            paper_bgcolor="#0f1117", plot_bgcolor="#1e2030",
            font=dict(color="#c9d1d9"),
            coloraxis_showscale=False,
            height=max(350, top_n * 25),
            margin=dict(t=50, b=10, l=10, r=10),
            xaxis=dict(gridcolor="#2a2d3e"),
            yaxis=dict(gridcolor="#2a2d3e"),
        )
        st.plotly_chart(fig_fi, use_container_width=True)

    with m2:
        st.markdown("**Top 10 Features (RF)**")
        st.dataframe(
            fi_rf[["feature_clean", "importance"]].head(10).rename(
                columns={"feature_clean": "Feature", "importance": "Importance"}
            ).round(4),
            hide_index=True, use_container_width=True
        )
        st.markdown("---")
        st.markdown("**Top 10 Features (LR Coefficients)**")
        st.dataframe(
            fi_lr[["feature_clean", "coefficient"]].head(10).rename(
                columns={"feature_clean": "Feature", "coefficient": "Coefficient"}
            ).round(4),
            hide_index=True, use_container_width=True
        )

    # ── Priority Tier Revenue Breakdown ──
    st.markdown("---")
    st.markdown("### 🎯 Retention Campaign Economics by Tier")

    outreach_costs = {"Critical": 25.0, "High": 12.0, "Medium": 3.0, "Low": 0.5}
    econ = df.groupby("priority_tier").agg(
        customers=("customer_id", "count"),
        total_billing=("annualized_revenue", "sum"),
        exp_revenue_at_risk=("expected_revenue_at_risk", "sum"),
        avg_value_score=("value_score", "mean"),
        actual_churn=("churn", "sum"),
    ).reindex(["Critical", "High", "Medium", "Low"])

    econ["outreach_cost_per_cust"] = econ.index.map(outreach_costs)
    econ["total_outreach_cost"] = econ["customers"] * econ["outreach_cost_per_cust"]
    econ["expected_saved_margin"] = econ["exp_revenue_at_risk"] * 0.60 * 0.15
    econ["net_benefit"] = econ["expected_saved_margin"] - econ["total_outreach_cost"]

    econ_display = econ[["customers", "total_billing", "exp_revenue_at_risk",
                          "total_outreach_cost", "expected_saved_margin", "net_benefit"]].copy()
    econ_display.columns = ["Customers", "Annual Billing ($)", "Exp. Loss at Risk ($)",
                             "Campaign Cost ($)", "Saved Margin ($)", "Net Benefit ($)"]
    econ_display = econ_display.round(2)
    st.dataframe(econ_display, use_container_width=True)

    # Net benefit bar chart
    fig_nb = px.bar(
        econ.reset_index(), x="priority_tier", y="net_benefit",
        color="priority_tier", color_discrete_map=TIER_COLORS,
        title="Expected Net Campaign Benefit by Priority Tier ($)",
        labels={"priority_tier": "Tier", "net_benefit": "Net Benefit ($)"},
        category_orders={"priority_tier": ["Critical", "High", "Medium", "Low"]},
    )
    fig_nb.update_layout(
        paper_bgcolor="#0f1117", plot_bgcolor="#1e2030",
        font=dict(color="#c9d1d9"), height=300, showlegend=False,
        margin=dict(t=50,b=10), xaxis=dict(gridcolor="#2a2d3e"),
        yaxis=dict(gridcolor="#2a2d3e")
    )
    st.plotly_chart(fig_nb, use_container_width=True)

    st.caption("Assumptions: 60% gross margin rate, 15% retention offer success rate. These are illustrative parameters and should be calibrated with actual A/B test results.")
