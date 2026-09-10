import pandas as pd
from pathlib import Path
import streamlit as st


DATA_PATH = Path(__file__).parent.parent / "data" / "clean_supply_chain.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df["order date (DateOrders)"] = pd.to_datetime(
        df["order date (DateOrders)"],
        errors="coerce"
    )

    df["shipping date (DateOrders)"] = pd.to_datetime(
        df["shipping date (DateOrders)"],
        errors="coerce"
    )

    return df