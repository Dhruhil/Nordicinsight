import numpy as np

from nordicinsight.metrics import mae, rmse


def test_zero_error():
    y = np.array([1.0, 2.0, 3.0])
    assert mae(y, y) == 0.0
    assert rmse(y, y) == 0.0


def test_mae_value():
    assert mae(np.array([1.0, 3.0]), np.array([2.0, 2.0])) == 1.0