import sys
from pathlib import Path

# supaya dashboard.py (di folder app/) bisa import etl.py (di folder src/)
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
import etl

import streamlit as st

st.title("📊 Dashboard Revenue & Cost")

@st.cache_data
def load_data():
    raw = etl.extract("data/raw/contoh_transaksi.csv")
    monthly = etl.transform(raw)
    return monthly

df = load_data()

st.subheader("Data Bulanan")
st.dataframe(df)

project_dipilih = st.selectbox("Pilih Project", df["project"].unique())
filtered = df[df["project"] == project_dipilih]

st.subheader(f"Tren Revenue — {project_dipilih}")
st.line_chart(filtered.set_index("month")[["revenue", "cost"]])