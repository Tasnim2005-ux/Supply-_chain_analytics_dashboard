import streamlit as st
import plotly.express as px

from utils import load_data
from filter import apply_filters

st.set_page_config(
    page_title="Delivery Analytics",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Delivery Analytics")

# Load Dataset
df = load_data()

# Apply Filters
filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)
total_orders = len(filtered_df)

late_orders = filtered_df["Late_delivery_risk"].sum()

on_time_orders = total_orders - late_orders

late_percentage = (
    late_orders / total_orders * 100
    if total_orders > 0 else 0
)
st.subheader("🚚 Delivery Summary")

d1, d2, d3, d4 = st.columns(4)

with d1:
    st.metric(
        "📦 Total Orders",
        total_orders
    )

with d2:
    st.metric(
        "✅ On-Time",
        on_time_orders
    )

with d3:
    st.metric(
        "⚠️ Late Deliveries",
        late_orders
    )

with d4:
    st.metric(
        "📉 Late %",
        f"{late_percentage:.2f}%"
    )
st.header("🚚 Shipping Mode Performance")

shipping_sales = (
    filtered_df
    .groupby("Shipping Mode")["Sales"]
    .sum()
    .reset_index()
)

fig_shipping = px.bar(
    shipping_sales,
    x="Shipping Mode",
    y="Sales",
    color="Sales",
    title="Sales by Shipping Mode"
)

st.plotly_chart(
    fig_shipping,
    use_container_width=True
)
st.header("⚠️ Late Delivery Distribution")

late_df = (
    filtered_df["Late_delivery_risk"]
    .value_counts()
    .reset_index()
)

late_df.columns = [
    "Late Delivery",
    "Orders"
]

late_df["Late Delivery"] = late_df["Late Delivery"].replace({
    0: "On Time",
    1: "Late"
})

fig_late = px.pie(
    late_df,
    names="Late Delivery",
    values="Orders",
    hole=0.45,
    title="On-Time vs Late Deliveries"
)

st.plotly_chart(
    fig_late,
    use_container_width=True
)
shipping_summary = (
    filtered_df.groupby("Shipping Mode")["Sales per customer"]
    .sum()
    .reset_index()
)

shipping_summary.columns = [
    "Shipping Mode",
    "Sales"
]
best_shipping = shipping_summary.loc[
    shipping_summary["Sales"].idxmax()
]
worst_shipping = shipping_summary.loc[
    shipping_summary["Sales"].idxmin()
]

st.info(
    f"""
### 🚚 Delivery Business Insight

🚚 Best Shipping Mode:
**{best_shipping['Shipping Mode']}**

💰 Sales:
**${best_shipping['Sales']:,.2f}**

⚠️ Total Late Deliveries:
**{late_orders}**

📉 Late Delivery Rate:
**{late_percentage:.2f}%**

### 📌 Recommendation

• Prioritize high-performing shipping modes.

• Reduce late deliveries through logistics optimization.

• Monitor carrier performance regularly.

• Improve delivery planning during peak demand.
"""
)