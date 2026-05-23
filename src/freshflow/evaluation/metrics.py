"""Evaluation metrics for forecast, waste, and markdown models."""

import numpy as np
import pandas as pd


def mape(y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray) -> float:
    """Mean absolute percentage error."""
    raise NotImplementedError("mape is not yet implemented")


def rmse(y_true: pd.Series | np.ndarray, y_pred: pd.Series | np.ndarray) -> float:
    """Root mean squared error."""
    raise NotImplementedError("rmse is not yet implemented")


def evaluate_forecast(
    y_true: pd.DataFrame,
    y_pred: pd.DataFrame,
) -> dict[str, float]:
    """Compute standard forecast accuracy metrics.

    Args:
        y_true: Actual outcomes with aligned index/columns.
        y_pred: Predicted outcomes with aligned index/columns.

    Returns:
        Dictionary of metric name to value.
    """
    raise NotImplementedError("evaluate_forecast is not yet implemented")
