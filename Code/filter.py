import streamlit as st


def apply_filters(df):

    st.sidebar.header("🔍 Filters")

    categories = sorted(df["Category Name"].dropna().unique())
    selected_category = st.sidebar.selectbox(
        "Category",
        ["All"] + list(categories)
    )

    markets = sorted(df["Market"].dropna().unique())
    selected_market = st.sidebar.selectbox(
        "Market",
        ["All"] + list(markets)
    )

    shipping_modes = sorted(df["Shipping Mode"].dropna().unique())
    selected_shipping = st.sidebar.selectbox(
        "Shipping Mode",
        ["All"] + list(shipping_modes)
    )

    filtered_df = df.copy()

    if selected_category != "All":
        filtered_df = filtered_df[
            filtered_df["Category Name"] == selected_category
        ]

    if selected_market != "All":
        filtered_df = filtered_df[
            filtered_df["Market"] == selected_market
        ]

    if selected_shipping != "All":
        filtered_df = filtered_df[
            filtered_df["Shipping Mode"] == selected_shipping
        ]

    # Empty dataset handling
    if filtered_df.empty:
        st.warning("⚠️ No data found for the selected filters.")
        st.stop()

    return (
        filtered_df,
        selected_category,
        selected_market,
        selected_shipping
    )