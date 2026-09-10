import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from utils import load_data
from filter import apply_filters
st.set_page_config(
    page_title="Supply Chain Dashboard",
    page_icon="📦",
    layout="wide"
)
st.markdown("""
<div style="
background:linear-gradient(90deg,#000000,#1a1a1a);
padding:35px;
border-radius:18px;
box-shadow:0px 5px 15px rgba(0,0,0,0.3);
">

<h1 style="
color:white;
font-size:48px;
margin-bottom:10px;
">
📦 Supply Chain Analytics Dashboard
</h1>

<p style="
color:#d9d9d9;
font-size:20px;
margin-bottom:0px;
">
Executive Business Intelligence Dashboard
</p>

</div>
""", unsafe_allow_html=True)

st.title("📦 Supply Chain Analytics Dashboard")
st.subheader("📈 Executive KPI Dashboard")
st.caption(
    "Executive Business Intelligence Dashboard"
)
st.info("""
# Welcome 👋

This dashboard provides interactive insights into supply chain performance using Business Intelligence techniques.

Use the **left sidebar** to explore different analytics modules including:

• 📈 Sales Analytics

• 🌍 Geographic Analytics

• 📦 Product Analytics

• 🚚 Delivery Analytics

• 🔮 Sales Forecast

Designed for data-driven decision making and business performance analysis.
""")

df = load_data()

filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)
total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Order Profit Per Order"].sum()

total_orders = len(filtered_df)

total_customers = filtered_df["Customer Id"].nunique()
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "💰 Total Sales",
        f"${total_sales:,.2f}"
    )

with k2:
    st.metric(
        "💵 Total Profit",
        f"${total_profit:,.2f}"
    )

with k3:
    st.metric(
        "📦 Orders",
        total_orders
    )

with k4:
    st.metric(
        "👥 Customers",
        total_customers
    )
st.header("📈 Business Overview")

overview = (
    filtered_df
    .groupby("Category Name")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    overview,
    x="Category Name",
    y="Sales",
    color="Sales",
    title="Sales by Category"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

st.header("📊 Dashboard Statistics")

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("📄 Total Records", len(filtered_df))

with s2:
    st.metric("🌍 Markets", filtered_df["Market"].nunique())

with s3:
    st.metric("📦 Products", filtered_df["Product Name"].nunique())

with s4:
    st.metric("🚚 Shipping Modes", filtered_df["Shipping Mode"].nunique())
st.header("🧭 Dashboard Navigation")

st.info("""
### Available Analytics Pages

📈 Sales Analytics

🌍 Geographic Analytics

📦 Product Analytics

🚚 Delivery Analytics

🔮 Sales Forecast

Use the left sidebar to navigate between pages.
""")
st.header("👨‍💻 About This Project")

st.success("""
Supply Chain Analytics Dashboard

Built using:

• Python

• Pandas

• Plotly

• Streamlit

This project demonstrates Business Intelligence,
Data Analytics,
Supply Chain Analytics,
Dashboard Development,
and Forecasting.
""")
st.divider()

st.header("📊 Executive Summary")

best_market = (
    filtered_df.groupby("Market")["Sales"]
    .sum()
    .idxmax()
)

best_category = (
    filtered_df.groupby("Category Name")["Sales"]
    .sum()
    .idxmax()
)

best_product = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .idxmax()
)

late_delivery = filtered_df["Late_delivery_risk"].sum()

st.info(f"""
### 📈 Business Health Overview

🌍 **Best Performing Market:** {best_market}

📦 **Best Selling Category:** {best_category}

🏆 **Top Selling Product:** {best_product}

🚚 **Late Deliveries:** {late_delivery}

### 📌 Recommendation

• Increase inventory in high-demand markets.

• Focus marketing on the best-selling category.

• Reduce late deliveries to improve customer satisfaction.
""")
st.divider()

st.header("🚀 Dashboard Features")

c1, c2 = st.columns(2)

with c1:
    st.success("""
✅ Sales Analytics

✅ Geographic Analytics

✅ Product Analytics

""")

with c2:
    st.success("""
✅ Delivery Analytics

✅ Sales Forecast

✅ Business Intelligence Dashboard

""")
st.divider()

st.header("📥 Download Filtered Dataset")

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇ Download CSV",
    data=csv,
    file_name="Filtered_Supply_Chain_Data.csv",
    mime="text/csv"
)
st.divider()

st.header("🛠 Technology Stack")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("""
🐍 Python

🐼 Pandas

🔢 NumPy
""")

with tech2:
    st.success("""
📊 Plotly

⚡ Streamlit

📈 Data Visualization
""")

with tech3:
    st.success("""
📦 Supply Chain Analytics

📉 Business Intelligence

🤖 Machine Learning
""")
st.divider()

st.header("🏆 Project Highlights")

st.success("""
✅ Interactive Dashboard

✅ Executive KPI Dashboard

✅ Sales Analytics

✅ Geographic Analytics

✅ Product Analytics

✅ Delivery Analytics

✅ Sales Forecasting

✅ Business Insights

✅ ABC Inventory Analysis

✅ Data-Driven Decision Support
""")
st.divider()

st.header("👨‍💻 About the Developer")

left, right = st.columns([1,3])

with right:
 st.subheader("Tasnim Bin Nasim")

st.write("""
🎓 **University**

Jashore University of Science and Technology

🏫 **Department**

Industrial and Production Engineering

---

### 💼 Areas of Interest

• Supply Chain Analytics

• Business Intelligence

• Data Analytics

• Machine Learning

• Dashboard Development

---

### 🛠 Technical Skills

Python

Pandas

NumPy

Plotly

Streamlit

Excel

Machine Learning
""")
st.caption(
    "Developed by Tasnim Rafsun | Industrial & Production Engineering"
)
st.divider()
with st.sidebar:
    

    st.title("Supply Chain Dashboard")

    st.caption("Business Intelligence System")

    st.divider()
