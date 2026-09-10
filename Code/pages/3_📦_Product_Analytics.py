import streamlit as st
import plotly.express as px

from utils import load_data
from filter import apply_filters

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Product Analytics")

# Load Dataset
df = load_data()

# Apply Filters
filtered_df, selected_category, selected_market, selected_shipping = apply_filters(df)
total_products = filtered_df["Product Name"].nunique()
top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    color="Sales",
    title="Top 10 Products by Sales"
)
st.plotly_chart(
    fig_products,
    use_container_width=True,
    key="top_products_sales"
)
top_profit_products = (
    filtered_df
    .groupby("Product Name")["Order Profit Per Order"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_profit = px.bar(
    top_profit_products,
    x="Order Profit Per Order",
    y="Product Name",
    orientation="h",
    color="Order Profit Per Order",
    title="Top 10 Products by Profit"
)

st.plotly_chart(
    fig_profit,
    use_container_width=True,
    key="top_products_profit"
)
product_quantity = (
    filtered_df
    .groupby("Product Name")["Order Item Quantity"]
    .sum()
    .reset_index()
)
fast_products = (
    product_quantity
    .sort_values(
        by="Order Item Quantity",
        ascending=False
    )
    .head(10)
)

fig_fast = px.bar(
    fast_products,
    x="Order Item Quantity",
    y="Product Name",
    orientation="h",
    color="Order Item Quantity",
    title="Top 10 Fast Moving Products"
)

st.plotly_chart(
    fig_fast,
    use_container_width=True,
    key="fast_products"
)
# ==========================
# Slow Moving Products
# ==========================

slow_products = (
    product_quantity
    .sort_values(
        by="Order Item Quantity",
        ascending=True
    )
    .head(10)
)

fig_slow = px.bar(
    slow_products,
    x="Order Item Quantity",
    y="Product Name",
    orientation="h",
    color="Order Item Quantity",
    title="Top 10 Slow Moving Products"
)

st.plotly_chart(
    fig_slow,
    use_container_width=True,
    key="slow_products"
)
# ==========================
# Product KPI Values
# ==========================

total_products = filtered_df["Product Name"].nunique()

fastest_product = fast_products.iloc[0]

slowest_product = slow_products.iloc[0]

average_product_sales = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .mean()
)
st.divider()

st.subheader("📦 Product Summary")

p1, p2, p3, p4 = st.columns(4)

with p1:
    st.metric(
        "📦 Total Products",
        total_products
    )

with p2:
    st.metric(
        "🚀 Fastest Product",
        fastest_product["Product Name"]
    )

with p3:
    st.metric(
        "🐢 Slowest Product",
        slowest_product["Product Name"]
    )

with p4:
    st.metric(
        "💰 Avg Product Sales",
        f"${average_product_sales:,.2f}"
    )
st.header("🏆 Top 10 Products")

top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Product Name",
    y="Sales",
    color="Sales",
    title="Top 10 Products by Sales"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)
st.info(
    f"""
### 📦 Inventory Business Insight

🚀 **Fastest Moving Product:**
{fastest_product['Product Name']}

🐢 **Slowest Moving Product:**
{slowest_product['Product Name']}

📦 **Total Products Managed:**
{total_products}

💰 **Average Sales per Product:**
${average_product_sales:,.2f}

### 📌 Recommendation

• Increase inventory for the fastest moving product to reduce stock-out risk.

• Review the slowest moving product for discounts, promotions, or inventory optimization.

• Monitor inventory levels regularly to balance customer demand and holding costs.
"""
)

st.success(
    "Inventory is performing efficiently. Continue monitoring slow moving products."
)

st.divider()

st.header("📦 ABC Inventory Analysis")

# ==========================
# ABC Analysis Dataset
# ==========================

abc_df = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

# Cumulative Sales
abc_df["Cumulative Sales"] = abc_df["Sales"].cumsum()

# Cumulative Percentage
abc_df["Cumulative %"] = (
    abc_df["Cumulative Sales"]
    / abc_df["Sales"].sum()
    * 100
)

# ==========================
# ABC Classification Function
# ==========================

def abc_category(value):
    if value <= 80:
        return "A"
    elif value <= 95:
        return "B"
    else:
        return "C"

# Create ABC Class Column
abc_df["ABC Class"] = abc_df["Cumulative %"].apply(abc_category)

# Show Table
st.dataframe(
    abc_df,
    use_container_width=True
)

# ==========================
# Summary
# ==========================

abc_summary = (
    abc_df["ABC Class"]
    .value_counts()
    .reset_index()
)

abc_summary.columns = [
    "ABC Class",
    "Products"
]

# ==========================
# Chart
# ==========================

fig_abc = px.bar(
    abc_summary,
    x="ABC Class",
    y="Products",
    color="ABC Class",
    text="Products",
    title="ABC Inventory Classification"
)

st.plotly_chart(
    fig_abc,
    use_container_width=True
)

# ==========================
# Business Insight
# ==========================

st.info(f"""
### 📦 ABC Analysis Insight

🟢 **Class A Products:** {abc_summary.loc[abc_summary['ABC Class']=='A','Products'].sum() if 'A' in abc_summary['ABC Class'].values else 0}

🟡 **Class B Products:** {abc_summary.loc[abc_summary['ABC Class']=='B','Products'].sum() if 'B' in abc_summary['ABC Class'].values else 0}

🔴 **Class C Products:** {abc_summary.loc[abc_summary['ABC Class']=='C','Products'].sum() if 'C' in abc_summary['ABC Class'].values else 0}

### 📌 Recommendation

• Prioritize inventory management for **Class A** products.

• Monitor **Class B** products regularly.

• Optimize stock levels or promotions for **Class C** products.
""")