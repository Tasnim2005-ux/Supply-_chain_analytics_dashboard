import streamlit as st
import plotly.express as px

from utils import load_data
from filter import apply_filters

st.set_page_config(
    page_title="Geographic Analytics",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Geographic Analytics")

# Load Dataset
df = load_data()

# Apply Filters
filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)
market_sales = (
    filtered_df
    .groupby("Market")["Sales"]
    .sum()
    .reset_index()
)

highest_market = market_sales.loc[market_sales["Sales"].idxmax()]
lowest_market = market_sales.loc[market_sales["Sales"].idxmin()]
st.subheader("📊 Geographic Summary")

g1, g2, g3, g4 = st.columns(4)

with g1:
    st.metric(
        "🥇 Best Market",
        highest_market["Market"]
    )

with g2:
    st.metric(
        "📉 Lowest Market",
        lowest_market["Market"]
    )

with g3:
    st.metric(
        "🌍 Countries",
        filtered_df["Order Country"].nunique()
    )

with g4:
    st.metric(
        "💰 Geographic Sales",
        f"${market_sales['Sales'].sum():,.2f}"
    )
st.header("🌍 Sales by Market")

fig_market = px.bar(
    market_sales,
    x="Market",
    y="Sales",
    color="Sales",
    title="Sales by Market"
)

st.plotly_chart(
    fig_market,
    use_container_width=True
)
st.header("🌎 Top 10 Countries by Sales")

country_sales = (
    filtered_df
    .groupby("Order Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_country = px.bar(
    country_sales,
    x="Order Country",
    y="Sales",
    color="Sales",
    title="Top 10 Countries by Sales"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)
st.header("🥧 Market Share")

fig_market_share = px.pie(
    market_sales,
    names="Market",
    values="Sales",
    hole=0.45,
    title="Market Share"
)

st.plotly_chart(
    fig_market_share,
    use_container_width=True
)
st.info(
    f"""
### 🌍 Geographic Business Insight

🥇 Highest Sales Market:
**{highest_market['Market']}**

📉 Lowest Sales Market:
**{lowest_market['Market']}**

🌎 Countries Served:
**{filtered_df['Order Country'].nunique()}**

💰 Total Geographic Sales:
**${market_sales['Sales'].sum():,.2f}**

### 📌 Recommendation

• Increase investment in high-performing markets.

• Review sales strategy in low-performing markets.

• Expand distribution in growing countries.

• Monitor regional demand regularly.
"""
)