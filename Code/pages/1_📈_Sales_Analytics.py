import streamlit as st
import plotly.express as px

from utils import load_data
from filter import apply_filters
st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📊",
    layout="wide"
)
st.title("📊 Sales Analytics")
# ==========================
# Load Dataset
# ==========================

df = load_data()

filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "💰 Total Sales",
        f"${filtered_df['Sales per customer'].sum():,.2f}"
    )

with kpi2:
    st.metric(
        "📦 Total Orders",
        filtered_df.shape[0]
    )

with kpi3:
    st.metric(
        "👥 Customers",
        filtered_df["Customer Id"].nunique()
    )

with kpi4:
    st.metric(
        "🚚 Late Deliveries",
        filtered_df["Late_delivery_risk"].sum()
    )
st.subheader("📊 Sales by Category")

category_sales = (
        filtered_df.groupby("Category Name")["Sales per customer"]
        .sum()
        .reset_index()
    )

fig = px.bar(
        category_sales,
        x="Category Name",
        y="Sales per customer",
        color="Category Name",
        title="Sales by Category"
    )

st.plotly_chart(fig, use_container_width=True)
right_col = st.columns(1)

st.subheader("🥧 Market Share")

market_sales = (
        filtered_df.groupby("Market")["Sales per customer"]
        .sum()
        .reset_index()
    )

fig2 = px.pie(
        market_sales,
        names="Market",
        values="Sales per customer",
        hole=0.4
    )
st.plotly_chart(fig2, use_container_width=True)
st.header("📈 Sales Trend")
monthly_sales = (
    filtered_df
    .set_index("order date (DateOrders)")
    .resample("ME")["Sales"]
    .sum()
    .reset_index()
)

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
st.divider()
st.header("📈 Daily Sales Trend")        
daily_sales = (
    filtered_df
    .groupby(
        filtered_df["order date (DateOrders)"].dt.date
    )["Sales per customer"]
    .sum()
    .reset_index()
)
fig4 = px.line(
    daily_sales,
    x="order date (DateOrders)",
    y="Sales per customer",
    markers=True,
    title="Daily Sales Trend"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)
fig4.update_traces(line=dict(width=3))
fig4 = px.line(
    daily_sales,
    x="order date (DateOrders)",
    y="Sales per customer",
    title="Daily Sales Trend",
    markers=True
)

fig4.update_traces(line=dict(width=3))

st.plotly_chart(fig4, use_container_width=True)
fig4 = px.line(
    daily_sales,
    x="order date (DateOrders)",
    y="Sales per customer",
    title="Daily Sales Trend",
    markers=True
)

fig4.update_traces(line=dict(width=3))

st.write(daily_sales.head())
df["Order Month"] = df["order date (DateOrders)"].dt.to_period("M").astype(str)
st.divider()
st.header("📅 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .groupby("Order Month")["Sales per customer"]
    .sum()
    .reset_index()
)
fig5 = px.line(
    monthly_sales,
    x="Order Month",
    y="Sales per customer",
    title="Monthly Sales Trend",
    markers=True
)

fig5.update_traces(line=dict(width=3))

st.plotly_chart(fig5, use_container_width=True)
st.write("Monthly sales performance over time.")
st.divider()
st.header("🏆 Top 10 Categories")
top_categories = (
    filtered_df.groupby("Category Name")["Sales per customer"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
st.dataframe(
    top_categories,
    use_container_width=True
)
fig3 = px.bar(
    top_categories,
    x="Sales per customer",
    y="Category Name",
    orientation="h",
    color="Sales per customer",
    title="Top 10 Categories by Sales"
)

st.plotly_chart(fig3, use_container_width=True)
st.header("📊 Sales vs Profit")

comparison = (
    filtered_df
    .groupby("Category Name")
    .agg({
        "Sales": "sum",
        "Order Profit Per Order": "sum"
    })
    .reset_index()
)

fig_compare = px.bar(
    comparison,
    x="Category Name",
    y=["Sales", "Order Profit Per Order"],
    barmode="group",
    title="Sales vs Profit by Category"
)

st.plotly_chart(
    fig_compare,
    use_container_width=True
)
st.info("""
### 💡 Sales Business Insight

• Identify the highest revenue categories.

• Compare Sales and Profit together.

• High Sales with Low Profit may indicate excessive discounts or high operational costs.

• Use this analysis to improve pricing and profitability.
""")