import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

FEATURE_COLS = [
    "lag_1",
    "lag_2",
    "lag_3",
    "roll_mean_3",
    "month_num",
    "quarter"
]

def train_model(feat_df: pd.DataFrame, test_months: int = 2):
    feat_df = feat_df.dropna(subset=FEATURE_COLS)

    cutoff = feat_df["month"].max() - pd.DateOffset(months=test_months - 1)
    train = feat_df[feat_df["month"] < cutoff]
    test = feat_df[feat_df["month"] >= cutoff]

    model = GradientBoostingRegressor(random_state=42)
    model.fit(train[FEATURE_COLS], train["y"])

    pred = model.predict(test[FEATURE_COLS])
    mae = mean_absolute_error(test["y"], pred)
    rmse = np.sqrt(mean_squared_error(test["y"], pred))

    print(f"MAE  : {mae:,.0f} (rata-rata selisih absolut prediksi vs aktual)")
    print(f"RMSE : {rmse:,.0f} (mirip MAE, tapi lebih 'menghukum' error besar)")

    joblib.dump(model, "src_model.joblib")
    return model