import pandas as pd

df = pd.read_csv("data/raw/contoh_transaksi.csv")
print(df)
# print(df.head())      # 5 baris pertama
# print(df.info())      # tipe data tiap kolom
# print(df.columns)     # daftar nama kolom

# revenue_only = df[df["account_type"] == "Revenue"]
# print(revenue_only)

jakarta_only = df[df["area"] == "Jakarta"]
print(jakarta_only)

total_detail = df.groupby(["project", "area", "account_type"])["amount"].sum()
print(total_detail)
