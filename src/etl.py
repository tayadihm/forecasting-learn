import pandas as pd

def extract(path: str) -> pd.DataFrame:
    """Baca Raw Data Transaksi dari CSV."""
    df = pd.read_csv(path)
    return df

def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Bersihkan data mentah, lalu agregasi jadi bulanan per
    project & area."""
    df = df.copy()

    # parse tanggal jadi tipe datetime asli (bukan teks)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])

    # buang baris yang amount-nya kosong atau aneh
    df = df.dropna(subset=["amount"])
    df = df[df["amount"] > 0]

    # ambil awal bulan dari tanggal transaksi, misal 2026-01-05 -> 2026-01-01
    df["month"] = df["transaction_date"].values.astype("datetime64[M]")

    # agregasi: total amount per bulan, project, area dan account_type
    monthly = (
        df.groupby(["month", "project", "area", "account_type"])["amount"]
        .sum()
        .reset_index()
    )

    # ubah dari format panjang (1 baris = 1 jenis akun) jadi lebar
    # (1 baris = 1 bulan-project-area, klom revenue dan cost terpisah)
    pivoted = monthly.pivot_table(
        index=["month", "project", "area"],
        columns="account_type",
        values="amount",
        fill_value=0
    ).reset_index()

    pivoted.columns.name = None
    pivoted = pivoted.rename(columns={"Revenue": "revenue", "Cost": "cost"})
    return pivoted

def load(df: pd.DataFrame, path: str) -> None:
    """Simpan data yang sudah dibersihkan ke CSV."""
    df.to_csv(path, index=False)
    print(f"Data sudah disimpan ke {path} ({len(df)} baris).")

if __name__ == "__main__":
    raw = extract("data/raw/contoh_transaksi.csv")
    monthly = transform(raw)
    print(monthly)
    load(monthly, "data/processed/contoh_transaksi_bulanan.csv")
