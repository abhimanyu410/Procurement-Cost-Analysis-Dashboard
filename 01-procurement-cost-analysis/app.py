from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Procurement Analytics", page_icon="📦", layout="wide")
st.title("📦 Procurement Cost & Supplier Performance")
st.caption("Portfolio demonstration using synthetic purchase orders.")

@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "data" / "sample_purchase_orders.csv", parse_dates=["order_date"])
    df["delivered_on_time"] = df["delivered_on_time"].astype(str).str.lower().eq("true")
    return df

df = load_data()
with st.sidebar:
    st.header("Filters")
    suppliers = sorted(df.supplier.unique())
    categories = sorted(df.category.unique())
    selected_suppliers = st.multiselect("Supplier", suppliers, default=suppliers)
    selected_categories = st.multiselect("Category", categories, default=categories)

view = df[df.supplier.isin(selected_suppliers) & df.category.isin(selected_categories)].copy()
if view.empty:
    st.info("No rows match these filters.")
    st.stop()

a, b, c, d = st.columns(4)
a.metric("Total spend", f"₹{view.total_cost_inr.sum():,.0f}")
b.metric("Purchase orders", f"{view.po_id.nunique():,}")
c.metric("Average lead time", f"{view.lead_time_days.mean():.1f} days")
d.metric("On-time delivery", f"{view.delivered_on_time.mean()*100:.1f}%")

left, right = st.columns(2)
with left:
    cat = view.groupby("category", as_index=False).total_cost_inr.sum().sort_values("total_cost_inr", ascending=False)
    st.plotly_chart(px.bar(cat, x="category", y="total_cost_inr", title="Spend by category", labels={"total_cost_inr":"Spend (INR)"}), use_container_width=True)
with right:
    monthly = view.assign(month=view.order_date.dt.to_period("M").astype(str)).groupby("month", as_index=False).total_cost_inr.sum()
    st.plotly_chart(px.line(monthly, x="month", y="total_cost_inr", markers=True, title="Monthly spend"), use_container_width=True)

summary = view.groupby("supplier", as_index=False).agg(spend=("total_cost_inr","sum"), orders=("po_id","nunique"), avg_lead_time=("lead_time_days","mean"), on_time_rate=("delivered_on_time","mean"))
summary["on_time_rate"] = (summary["on_time_rate"] * 100).round(1)
st.subheader("Supplier summary")
st.dataframe(summary.sort_values("spend", ascending=False), use_container_width=True, hide_index=True)
st.subheader("Filtered purchase orders")
st.dataframe(view.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered CSV", view.to_csv(index=False).encode("utf-8"), "filtered_purchase_orders.csv", "text/csv")
