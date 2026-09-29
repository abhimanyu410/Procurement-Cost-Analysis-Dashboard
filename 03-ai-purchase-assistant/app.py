from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Purchase Assistant Prototype", page_icon="🤖", layout="wide")
st.title("🤖 Purchase Assistant — Search Prototype")
st.caption("Keyword-based demo using synthetic catalogue and purchase-order data. No external AI service is connected.")

data_dir = Path(__file__).parent / "data"
catalog = pd.read_csv(data_dir / "product_catalog.csv")
orders = pd.read_csv(data_dir / "sample_purchase_orders.csv")

query = st.text_input("What are you looking for?", placeholder="e.g. SS, fittings, SKU-003")
category_options = ["All categories"] + sorted(catalog.category.unique())
category = st.selectbox("Category filter", category_options)
matches = catalog.copy()
if query.strip():
    q = query.strip().lower()
    searchable = matches[["sku","product","category","unit"]].fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    matches = matches[searchable.str.contains(q, regex=False)]
if category != "All categories":
    matches = matches[matches.category == category]
a, b = st.columns(2)
a.metric("Matching products", len(matches))
b.metric("Catalogue items", len(catalog))
st.subheader("Product catalogue matches")
if matches.empty:
    st.info("No keyword match. Try a broader product name or another category.")
else:
    st.dataframe(matches.sort_values("product"), use_container_width=True, hide_index=True)

st.subheader("Sample purchase-order lookup")
order_query = st.text_input("Search orders by supplier, product, category, or PO ID", placeholder="e.g. Prime Steel or MS Pipe")
order_view = orders.copy()
if order_query.strip():
    q = order_query.strip().lower()
    searchable = order_view.fillna("").astype(str).agg(" ".join, axis=1).str.lower()
    order_view = order_view[searchable.str.contains(q, regex=False)]
st.dataframe(order_view.head(100), use_container_width=True, hide_index=True)
st.download_button("Download matching catalogue", matches.to_csv(index=False).encode("utf-8"), "catalogue_matches.csv", "text/csv")
