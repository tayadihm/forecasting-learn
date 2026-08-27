import pandas as pd

df = pd.read_csv("data/processed/contoh_transaksi_bulanan.csv", parse_dates=["month"])

print("=== 1. Cek data kosong per kolom ===")
print(df.isna().sum())

print("\n=== 2. Cek duplikat ===")
print("Jumlah duplikat:", df.duplicated().sum())

print("\n=== 3. Statistik dasar (buat lihat nilai aneh) ===")
print(df[["revenue", "cost"]].describe())
# perhatikan: kalau "min" negatif atau "max" jauh lebih besar dari "75%",
# itu sinyal ada outlier / data salah

print("\n=== 4. Cek nilai negatif atau nol ===")
print(df[(df["revenue"] < 0) | (df["revenue"] == 0)])
print(df[(df["cost"] < 0) | (df["cost"] == 0)])

print("\n=== 5. Cek penamaan kategori tidak konsisten ===")
print("Daftar project:", df["project"].unique())
print("Daftar area   :", df["area"].unique())
# kalau muncul nama yang mirip tapi beda penulisan, itu masalah

print("\n=== 6. Cek tipe data tiap kolom ===")
print(df.dtypes)
# "amount"/"revenue"/"cost" harus float/int, kalau muncul "object" berarti masih teks

print("\n=== 7. Cek outlier pakai metode IQR ===")
for col in ["revenue", "cost"]:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    batas_bawah = Q1 - 1.5 * IQR
    batas_atas = Q3 + 1.5 * IQR
    outliers = df[(df[col] < batas_bawah) | (df[col] > batas_atas)]
    print(f"Outlier di kolom '{col}': {len(outliers)} baris")
    if len(outliers) > 0:
        print(outliers[["month", "project", "area", col]])

print("\n=== 8. Cek bulan yang hilang per project-area ===")
semua_bulan = pd.date_range(df["month"].min(), df["month"].max(), freq="MS")
for (project, area), grp in df.groupby(["project", "area"]):
    bulan_ada = set(grp["month"])
    bulan_hilang = sorted(set(semua_bulan) - bulan_ada)
    if bulan_hilang:
        print(f"{project} - {area}: kehilangan {len(bulan_hilang)} bulan -> {bulan_hilang}")