import streamlit as st
import plotly.express as px

from utils import load_data
from filter import apply_filters

st.set_page_config(
    page_title="Sales Forecast",
    page_icon="🔮",
    layout="wide"
)

st.title("🔮 Sales Forecast")

# ==========================
# Load Dataset
# ==========================

df = load_data()

filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)

# ==========================
# Monthly Sales
# ==========================

monthly_sales = (
    filtered_df
    .set_index("order date (DateOrders)")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

# ==========================
# Monthly Trend
# ==========================

st.header("📈 Monthly Sales Trend")

fig_trend = px.line(
    monthly_sales,
    x="order date (DateOrders)",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ==========================
# Moving Average
# ==========================

monthly_sales["Moving Average"] = (
    monthly_sales["Sales"]
    .rolling(3)
    .mean()
)

st.header("📊 3-Month Moving Average")

fig_ma = px.line(
    monthly_sales,
    x="order date (DateOrders)",
    y=["Sales", "Moving Average"],
    title="Sales vs Moving Average"
)

st.plotly_chart(
    fig_ma,
    use_container_width=True
)

# ==========================
# Growth Rate
# ==========================

monthly_sales["Growth Rate (%)"] = (
    monthly_sales["Sales"]
    .pct_change()
    * 100
)

st.header("📈 Monthly Growth Rate")

fig_growth = px.bar(
    monthly_sales,
    x="order date (DateOrders)",
    y="Growth Rate (%)",
    color="Growth Rate (%)",
    title="Monthly Growth Rate (%)"
)

st.plotly_chart(
    fig_growth,
    use_container_width=True
)

# ==========================
# Forecast
# ==========================

forecast_sales = (
    monthly_sales["Sales"]
    .tail(3)
    .mean()
)

latest_sales = monthly_sales["Sales"].iloc[-1]

st.header("🔮 Forecast")

st.metric(
    "Estimated Next Month Sales",
    f"${forecast_sales:,.2f}"
)

# ==========================
# Forecast Insight
# ==========================

if forecast_sales > latest_sales:
    forecast_message = "📈 Sales are expected to increase next month."
    forecast_status = "Positive Growth Expected ✅"
else:
    forecast_message = "📉 Sales may decline next month."
    forecast_status = "Sales Need Attention ⚠️"

st.info(
    f"""
### 🔮 Forecast Business Insight

📊 Latest Month Sales:
${latest_sales:,.2f}

📈 Estimated Next Month Sales:
${forecast_sales:,.2f}

{forecast_message}

### 📌 Recommendation

• Prepare inventory based on forecast demand.

• Monitor sales trends regularly.

• Increase marketing efforts if sales are expected to decline.

• Review customer demand before procurement.
"""
)

if forecast_sales > latest_sales:
    st.success(forecast_status)
else:
    st.warning(forecast_status)