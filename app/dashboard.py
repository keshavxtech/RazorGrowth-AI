import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd

from ml.growth_engine import generate_growth_opportunities


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RazorGrowth AI",
    page_icon="app/assets/azorpay_logo.png",
    layout="wide"
)


# =========================================================
# LOAD DATA
# =========================================================

customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")
transactions = pd.read_csv("data/transactions.csv")
campaigns = pd.read_csv("data/campaigns.csv")


# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(circle at top left, #12131a, #0a0a0f 60%);
    color: #e6e6eb;
}

h1 {
    font-weight: 800 !important;
    background: linear-gradient(90deg, #6366f1, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

h2, h3 {
    font-weight: 700 !important;
    color: #f1f1f4;
}

div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17181f, #1c1d26);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 18px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.35);
}

div[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700 !important;
}

hr {
    border-color: rgba(255,255,255,0.08) !important;
}

.stButton > button {
    background: linear-gradient(90deg, #6366f1, #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    opacity: 0.9;
    transform: scale(1.02);
}

section[data-testid="stSidebar"] {
    background: #0d0e13;
    border-right: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_done" not in st.session_state:
    st.session_state.analysis_done = False

if "campaign_approved" not in st.session_state:
    st.session_state.campaign_approved = False


# =========================================================
# SIDEBAR — MERCHANT INPUTS
# =========================================================

with st.sidebar:

    st.markdown(" Growth Agent")

    st.write(
        "Tell the agent what you want to achieve."
    )

    business_goal = st.selectbox(
        "Business Goal",
        [
            "Increase Revenue",
            "Reduce Customer Churn",
            "Improve Conversion",
            "Recover Failed Payments"
        ]
    )

    # IMPORTANT:
    # User can enter ANY growth target from 1% to 100%

    target_growth = st.number_input(
        "Target Revenue Growth (%)",
        min_value=1,
        max_value=100,
        value=15,
        step=1
    )

    campaign_budget = st.number_input(
        "Campaign Budget (₹)",
        min_value=1000,
        max_value=1000000,
        value=60000,
        step=5000
    )

    campaign_duration = st.number_input(
        "Campaign Duration (Days)",
        min_value=1,
        max_value=90,
        value=16,
        step=1
    )

    target_segment = st.selectbox(
        "Target Segment",
        [
            "All Customers",
            "High Value Customers",
            "Inactive Customers",
            "Failed Payment Customers"
        ]
    )

    analyze = st.button(
        " Analyze My Business",
        use_container_width=True
    )


# =========================================================
# CURRENT BUSINESS METRICS
# =========================================================

successful_transactions = transactions[
    transactions["status"] == "Success"
].copy()

current_revenue = successful_transactions["amount"].sum()

successful_orders = len(successful_transactions)

total_customers = len(customers)

average_order_value = (
    current_revenue / successful_orders
    if successful_orders > 0
    else 0
)


# =========================================================
# ANALYZE BUSINESS
# =========================================================

if analyze:

    st.session_state.analysis_done = True
    st.session_state.campaign_approved = False


# =========================================================
# HEADER
# =========================================================

st.title("RazorGrowth AI")

st.subheader(
    "Autonomous AI Growth Agent for Digital Commerce"
)

st.write(
    "Turn merchant data into intelligent growth opportunities."
)


# =========================================================
# CURRENT METRICS
# =========================================================

st.markdown("Current Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Revenue",
    f"₹{current_revenue:,.0f}"
)

col2.metric(
    "Successful Orders",
    f"{successful_orders:,}"
)

col3.metric(
    "Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Average Order Value",
    f"₹{average_order_value:,.0f}"
)


# =========================================================
# DYNAMIC AI GROWTH TARGET
# =========================================================

if st.session_state.analysis_done:

    # -----------------------------------------------------
    # DYNAMIC CALCULATION
    # -----------------------------------------------------

    growth_multiplier = 1 + (target_growth / 100)

    target_revenue = (
        current_revenue * growth_multiplier
    )

    additional_revenue = (
        target_revenue - current_revenue
    )

    projected_orders = int(
        successful_orders * growth_multiplier
    )

    projected_customers = int(
        total_customers *
        (1 + (target_growth / 100) * 0.35)
    )

    projected_aov = (
        target_revenue / projected_orders
        if projected_orders > 0
        else 0
    )


    # =====================================================
    # GROWTH TARGET
    # =====================================================

    st.divider()

    st.markdown(
        f" AI Growth Target: +{target_growth}%"
    )

    target_col1, target_col2, target_col3 = st.columns(3)

    target_col1.metric(
        "Target Revenue",
        f"₹{target_revenue:,.0f}",
        delta=f"+{target_growth}%"
    )

    target_col2.metric(
        "Additional Revenue Needed",
        f"₹{additional_revenue:,.0f}"
    )

    target_col3.metric(
        "Projected Orders",
        f"{projected_orders:,}",
        delta=f"+{projected_orders - successful_orders:,}"
    )


    # =====================================================
    # PROJECTED BUSINESS METRICS
    # =====================================================

    st.markdown(" Projected Business Impact")

    p1, p2, p3, p4 = st.columns(4)

    p1.metric(
        "Projected Revenue",
        f"₹{target_revenue:,.0f}",
        delta=f"+{target_growth}%"
    )

    p2.metric(
        "Projected Orders",
        f"{projected_orders:,}"
    )

    p3.metric(
        "Projected Customers",
        f"{projected_customers:,}"
    )

    p4.metric(
        "Projected AOV",
        f"₹{projected_aov:,.0f}"
    )


# =========================================================
# REVENUE TREND
# =========================================================

st.divider()

st.subheader(" Revenue Trend")

successful_transactions["transaction_date"] = pd.to_datetime(
    successful_transactions["transaction_date"]
)

daily_revenue = (
    successful_transactions
    .groupby("transaction_date")["amount"]
    .sum()
    .reset_index()
)

st.line_chart(
    daily_revenue.set_index("transaction_date")
)


# =========================================================
# AI BUSINESS ANALYSIS
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(" AI Business Analysis")

    opportunities = generate_growth_opportunities(
        customers,
        products,
        transactions,
        goal=business_goal,
        budget=campaign_budget,
        duration=campaign_duration,
        target_segment=target_segment
    )

    if opportunities:

        for opportunity in opportunities:

            priority = opportunity["priority"]

            if priority == "High":
                icon = "🔴"
            elif priority == "Medium":
                icon = "🟡"
            else:
                icon = "🟢"

            with st.container(border=True):

                st.markdown(
                    f"### {icon} {opportunity['type']}"
                )

                st.write(
                    f"**Priority:** {priority}"
                )

                st.write(
                    opportunity["description"]
                )

                st.write(
                    f"**Recommended Action:** "
                    f"{opportunity['action']}"
                )

                if opportunity["potential_value"] > 0:

                    st.write(
                        f"**Potential Value:** "
                        f"₹{float(opportunity['potential_value']):,.0f}"
                    )

    else:

        st.success(
            "No major growth opportunities detected."
        )


# =========================================================
# DYNAMIC CAMPAIGN RECOMMENDATION
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(" Recommended Growth Campaign")

    # -----------------------------------------------------
    # Campaign strategy changes according to goal
    # -----------------------------------------------------

    if business_goal == "Increase Revenue":

        campaign_name = (
            f"{target_growth}% Revenue Growth Campaign"
        )

        campaign_strategy = (
            f"Target {target_segment.lower()} with "
            "personalized offers, cross-selling, "
            "upselling and high-value product recommendations."
        )

        campaign_objective = (
            f"Generate approximately ₹"
            f"{additional_revenue:,.0f} "
            "in additional revenue."
        )


    elif business_goal == "Reduce Customer Churn":

        campaign_name = (
            f"Customer Retention — {target_growth}% Growth"
        )

        campaign_strategy = (
            "Reactivate inactive customers using "
            "personalized win-back offers, reminders "
            "and loyalty incentives."
        )

        campaign_objective = (
            f"Improve retention while supporting "
            f"a {target_growth}% growth target."
        )


    elif business_goal == "Improve Conversion":

        campaign_name = (
            f"Conversion Boost — {target_growth}% Growth"
        )

        campaign_strategy = (
            "Identify high-traffic, low-conversion products "
            "and run pricing, messaging and offer experiments."
        )

        campaign_objective = (
            f"Increase product conversion enough to support "
            f"a {target_growth}% growth target."
        )


    else:

        campaign_name = (
            f"Payment Recovery — {target_growth}% Growth"
        )

        campaign_strategy = (
            "Recover failed payments using automatic retries, "
            "alternative payment methods and customer reminders."
        )

        campaign_objective = (
            f"Recover lost payment revenue and support "
            f"a {target_growth}% growth target."
        )


    # =====================================================
    # CAMPAIGN CARD
    # =====================================================

    with st.container(border=True):

        st.markdown(
            f"### {campaign_name}"
        )

        st.write(
            f"**Target Segment:** {target_segment}"
        )

        st.write(
            f"**Strategy:** {campaign_strategy}"
        )

        st.write(
            f"**Objective:** {campaign_objective}"
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Campaign Budget",
            f"₹{campaign_budget:,.0f}"
        )

        c2.metric(
            "Duration",
            f"{campaign_duration} Days"
        )

        c3.metric(
            "Growth Target",
            f"+{target_growth}%"
        )


# =========================================================
# BUDGET SAFETY CHECK
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    st.markdown(" Agent Safety Check")

    max_safe_budget = 100000

    if campaign_budget <= max_safe_budget:

        st.success(
            f"Budget approved for execution: "
            f"₹{campaign_budget:,.0f}"
        )

        budget_safe = True

    else:

        st.error(
            "Campaign blocked: budget exceeds the "
            f"₹{max_safe_budget:,.0f} safety limit."
        )

        budget_safe = False


# =========================================================
# APPROVE CAMPAIGN
# =========================================================

if st.session_state.analysis_done:

    st.divider()

    if budget_safe:

        approve = st.button(
            " Approve & Execute Campaign",
            use_container_width=True
        )

        if approve:

            st.session_state.campaign_approved = True

            st.success(
                f"Campaign approved! "
                f"Targeting +{target_growth}% growth "
                f"with a budget of ₹{campaign_budget:,.0f}."
            )

            st.balloons()

    else:

        st.button(
            " Campaign Locked",
            disabled=True,
            use_container_width=True
        )


# =========================================================
# CAMPAIGN STATUS
# =========================================================

if st.session_state.campaign_approved:

    st.divider()

    st.markdown(" Campaign Status")

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Status",
        "Approved"
    )

    s2.metric(
        "Growth Target",
        f"+{target_growth}%"
    )

    s3.metric(
        "Budget",
        f"₹{campaign_budget:,.0f}"
    )


# =========================================================
# TRANSACTION SUMMARY
# =========================================================

st.divider()

st.subheader(" Transaction Summary")

status_counts = transactions["status"].value_counts()

st.bar_chart(status_counts)