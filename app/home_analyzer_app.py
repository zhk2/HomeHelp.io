
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="HomeLens — Local AI Home Analyzer", layout="wide")

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, parse_dates=["date"])
    # Keep latest month per metro
    latest_date = df["date"].max()
    latest = df[df["date"] == latest_date].copy()
    # Ensure expected cols exist
    for c in ["zhvi","zori","inventory","sales_count","market_temp_index","zhvi_growth","RegionName","StateName"]:
        if c not in latest.columns:
            latest[c] = np.nan
    # Deduplicate per metro/state
    metro = latest[["RegionName","StateName","zhvi","zori","inventory","sales_count","market_temp_index","zhvi_growth"]].drop_duplicates()
    metro = metro.dropna(subset=["RegionName","StateName"])
    return metro, latest_date

def size_adjustment(sqft: float, anchor_sqft: float = 1500.0, elasticity: float = 0.72) -> float:
    return (sqft / anchor_sqft) ** elasticity

def feature_adjustment(beds: int, baths: float) -> float:
    bed_base, bath_base = 3, 2.0
    bed_bump = 0.035 * (beds - bed_base)
    bath_bump = 0.05 * (baths - bath_base)
    return 1.0 + bed_bump + bath_bump

def market_heat_multiplier(market_temp_index):
    if pd.isna(market_temp_index):
        return 1.0
    return 1.0 + 0.03 * (market_temp_index / 10.0)

def growth_premium(zhvi_growth):
    if pd.isna(zhvi_growth):
        return 1.0
    return 1.0 + (0.02 * (zhvi_growth / 1.0))

DATA_PATH = "zillow_merged_metro_month.csv"
metro, latest_date = load_data(DATA_PATH)

st.title("🏠 HomeLens — Local AI Home Analyzer (No API)")
st.caption(f"Using merged Zillow metro dataset — latest month: {latest_date.date()}")

colA, colB = st.columns([1,2], gap="large")

with colA:
    st.subheader("Pick a market")
    states = sorted(metro["StateName"].dropna().unique())
    state = st.selectbox("State", states, index=states.index("Washington") if "Washington" in states else 0)
    cities = sorted(metro.loc[metro["StateName"]==state, "RegionName"].unique())
    region = st.selectbox("Metro / City", cities, index=cities.index("Seattle") if "Seattle" in cities else 0)

    st.subheader("Listing details")
    list_price = st.number_input("List price ($)", min_value=50000, max_value=10000000, value=700000, step=5000)
    sqft = st.number_input("Interior sqft", min_value=200, max_value=20000, value=1400, step=50)
    beds = st.number_input("Bedrooms", min_value=0, max_value=10, value=3, step=1)
    baths = st.number_input("Bathrooms", min_value=0.0, max_value=10.0, value=2.0, step=0.5)
    lot_sqft = st.number_input("Lot sqft (optional)", min_value=0, max_value=100000, value=3500, step=100)
    year_built = st.number_input("Year built (optional)", min_value=1800, max_value=2100, value=1950, step=1)

    go = st.button("Score this listing")

with colB:
    st.subheader("Market snapshot")
    row = metro[(metro["RegionName"]==region) & (metro["StateName"]==state)].iloc[0]
    st.metric("ZHVI (typical home value)", f"${row['zhvi']:,.0f}")
    col1, col2, col3 = st.columns(3)
    col1.metric("ZORI (rent)", f"${row['zori']:,.0f}" if pd.notna(row['zori']) else "—")
    col2.metric("Inventory", f"{int(row['inventory']):,}" if pd.notna(row['inventory']) else "—")
    col3.metric("Sales count", f"{int(row['sales_count']):,}" if pd.notna(row['sales_count']) else "—")

    st.caption("Tip: ZHVI anchors price; we adjust with size elasticity, bed/bath bumps, and mild market factors.")

    st.subheader("Listing valuation")
    if go:
        base_zhvi = float(row["zhvi"])
        f_size = size_adjustment(sqft)
        f_feat = feature_adjustment(beds, baths)
        f_heat = market_heat_multiplier(row["market_temp_index"])
        f_growth = growth_premium(row["zhvi_growth"])

        fair_value = base_zhvi * f_size * f_feat * f_heat * f_growth
        edge = (fair_value - list_price) / list_price
        deal_score = max(0.0, min(1.0, edge / 0.05))

        st.metric("Estimated fair value", f"${fair_value:,.0f}")
        colx, coly = st.columns(2)
        colx.metric("Edge vs list", f"{edge*100:.2f}%")
        coly.metric("Deal score (0–1)", f"{deal_score:.2f}")

        with st.expander("Why this value? (Factors)"):
            st.write({
                "base_zhvi": round(base_zhvi,0),
                "size_factor": round(f_size,3),
                "feature_factor": round(f_feat,3),
                "market_heat_factor": round(f_heat,3),
                "growth_factor": round(f_growth,3),
            })

    st.subheader("Find promising metros")
    st.caption("Quick heuristics: low price-to-rent, rising values, tighter inventory.")
    tmp = metro.copy()
    tmp["price_to_rent"] = tmp["zhvi"] / tmp["zori"]
    tmp["sales_inventory_ratio"] = tmp["sales_count"] / tmp["inventory"]
    tmp = tmp.replace([np.inf, -np.inf], np.nan)

    # Score: lower P/R better, higher growth/heat/sales_inventory better (simple normalized ranks)
    for col in ["price_to_rent","zhvi_growth","market_temp_index","sales_inventory_ratio"]:
        if col not in tmp.columns:
            tmp[col] = np.nan
    tmp["score"] = (
        (1 - (tmp["price_to_rent"] - tmp["price_to_rent"].min()) / (tmp["price_to_rent"].max() - tmp["price_to_rent"].min())) * 0.4 +
        ((tmp["zhvi_growth"] - tmp["zhvi_growth"].min()) / (tmp["zhvi_growth"].max() - tmp["zhvi_growth"].min())) * 0.25 +
        ((tmp["market_temp_index"] - tmp["market_temp_index"].min()) / (tmp["market_temp_index"].max() - tmp["market_temp_index"].min())) * 0.2 +
        ((tmp["sales_inventory_ratio"] - tmp["sales_inventory_ratio"].min()) / (tmp["sales_inventory_ratio"].max() - tmp["sales_inventory_ratio"].min())) * 0.15
    )

    st.dataframe(
        tmp.sort_values("score", ascending=False)
           .head(25)[["RegionName","StateName","zhvi","zori","price_to_rent","sales_inventory_ratio","zhvi_growth","market_temp_index","score"]]
           .round(3)
    )

st.caption("This MVP relies only on your local merged Zillow dataset. No external APIs used.")
