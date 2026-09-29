# Purchase Assistant — Catalogue Search Prototype

A lightweight purchasing helper that searches a synthetic product catalogue and purchase-order records using keyword matching and category filtering.

## Features
- Search by product name, category, or SKU
- Filter products by category
- Compare indicative unit price and typical lead time
- Browse sample purchase-order records

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Scope
This is a **rule-based search prototype**, not a generative AI model. It does not connect to an LLM, ERP system, supplier portal, or private company data. Prices are synthetic.
