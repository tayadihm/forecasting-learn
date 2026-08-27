import pandas as pd

## time series lagging, rolling mean, dan fitur kalender

def build_features(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    target: "revenue" atau cost"
    Menambahkan kolom lag, rolling mean, dan fitur kalender.
    """
    df = df.sort_values(["project", "area", "month"]).copy()
    df["y"] = df[target]

    group = ["project", "area"]
    for lag in [1, 2, 3]:
        df[f"lag_{lag}"] = df.groupby(group)["y"].shift(lag)
    df["roll_mean_3"] = df.groupby(group)["y"].transform(lambda x: x.shift(1).rolling(3).mean())

    df["month_num"] = df["month"].dt.month
    df["quarter"] = df["month"].dt.quarter

    return df