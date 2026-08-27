import streamlit as st
import pandas as pd

st.title("📊 Dashboard Revenue & Cost")

df = pd.read_csv("data/processed/contoh_transaksi_bulanan.csv", parse_dates=["month"])

st.subheader("Data Bulanan")
st.dataframe(df)

project_dipilih = st.selectbox("Pilih Project", df["project"].unique())
filtered = df[df["project"] == project_dipilih]

st.subheader(f"Tren Revenue — Project: {project_dipilih}")
st.line_chart(filtered.set_index("month")[["revenue", "cost"]])