import mlflow
import numpy as np

from nordicinsight.data import load_hourly_prices
from nordicinsight.metrics import mae, mase, rmse

TEST_DAYS = 90
VAL_DAYS = 90

mlflow.set_experiment("baselines")

for zone in ["SE_3", "SE_4"]:
    y = load_hourly_prices(zone).dropna()
    # The hourly index must be gap-free, or shift(lag) would compare wrong hours.
    assert (y.index.to_series().diff().dropna() == np.timedelta64(1, "h")).all()

    test_start = len(y) - TEST_DAYS * 24      # test set: NOT used in this script
    val_start = test_start - VAL_DAYS * 24
    train = y.iloc[:val_start].to_numpy()
    val = y.iloc[val_start:test_start].to_numpy()

    for lag in (24, 168):
        pred = y.shift(lag).iloc[val_start:test_start].to_numpy()
        metrics = {
            "mae": mae(val, pred),
            "rmse": rmse(val, pred),
            "mase": mase(val, pred, train),
        }
        with mlflow.start_run(run_name=f"seasonal_naive_{lag}_{zone}"):
            mlflow.log_params(
                {
                    "model": "seasonal_naive",
                    "lag_hours": lag,
                    "zone": zone,
                    "split": "validation",
                    "val_start": str(y.index[val_start]),
                    "val_end": str(y.index[test_start - 1]),
                }
            )
            mlflow.log_metrics(metrics)
        print(zone, f"lag={lag}", {k: round(v, 2) for k, v in metrics.items()})