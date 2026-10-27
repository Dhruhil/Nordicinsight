import numpy as np


def mae(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.mean(np.abs(y - pred)))


def rmse(y: np.ndarray, pred: np.ndarray) -> float:
    return float(np.sqrt(np.mean((y - pred) ** 2)))


def mase(y: np.ndarray, pred: np.ndarray, train: np.ndarray, season: int = 168) -> float:
    """MAE divided by the in-sample error of a seasonal naive forecast."""
    scale = np.mean(np.abs(train[season:] - train[:-season]))
    return float(np.mean(np.abs(y - pred)) / scale)