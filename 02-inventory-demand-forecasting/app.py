from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Inventory Demand Forecast", page_icon="📈", layout="wide")
st.title("📈 Inventory Demand Forecasting")
st.caption("Synthetic learning dataset — illustrative forecast, not replenishment advice.")

@st.cache_data
def load_data():
    return pd.read_csv(Path(__file__).parent / "data" / "monthly_demand.csv", parse_dates=["month"])

df = load_data()
product = st.selectbox("Choose product", sorted(df.product.unique()))
data = df[df.product == product].sort_values("month").copy()
data["moving_average_3"] = data.units_sold.shift(1).rolling(3).mean()
forecast = data.units_sold.tail(3).mean()
latest = data.iloc[-1]
a, b, c = st.columns(3)
a.metric("Latest monthly demand", f"{int(latest.units_sold):,} units")
b.metric("Next-month baseline forecast", f"{forecast:,.0f} units")
c.metric("Total stockout days", f"{int(data.stockout_days.sum())}")
st.plotly_chart(px.line(data, x="month", y="units_sold", markers=True, title=f"Monthly demand — {product}"), use_container_width=True)
compare = data.dropna(subset=["moving_average_3"])[["month","units_sold","moving_average_3"]].melt(id_vars="month", var_name="series", value_name="units")
st.plotly_chart(px.line(compare, x="month", y="units", color="series", markers=True, title="Actual demand vs trailing three-month baseline"), use_container_width=True)
st.subheader("Historical records")
st.dataframe(data, use_container_width=True, hide_index=True)
st.download_button("Download selected product data", data.to_csv(index=False).encode("utf-8"), "selected_product_demand.csv", "text/csv")
st.info("Real inventory decisions also need lead times, service levels, supplier constraints, seasonality checks, and stock policies.")
