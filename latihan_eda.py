import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/contoh_transaksi_bulanan.csv", parse_dates=["month"])

# lihat tren revenue per project dari waktu ke waktu
pivot = df.pivot_table(index="month", columns="project", values="revenue", aggfunc="sum")
pivot.plot(marker="o")
plt.title("Tren Revenue per Project")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig("data/processed/tren_revenue_per_project.png")
print("Chart tersimpan di data/processed/tren_revenue_per_project.png")