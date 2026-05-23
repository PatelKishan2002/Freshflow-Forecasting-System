"""Demand forecasting models for perishable categories."""

from typing import Any

import pandas as pd


def train_forecast_model(
    features: pd.DataFrame,
    target: pd.Series,
    params: dict[str, Any] | None = None,
) -> Any:
    """Train a demand forecast model on historical features.

    Args:
        features: Training feature matrix.
        target: Training target (e.g., daily units sold).
        params: Optional model hyperparameters; defaults from config when None.

    Returns:
        Fitted model object.
    """
    raise NotImplementedError("train_forecast_model is not yet implemented")


def predict_forecast(
    model: Any,
    features: pd.DataFrame,
    horizon_days: int | None = None,
) -> pd.DataFrame:
    """Generate multi-step demand forecasts.

    Args:
        model: Fitted forecast model.
        features: Feature matrix for prediction period.
        horizon_days: Forecast horizon; if None, read from config.

    Returns:
        DataFrame with forecasted demand by entity and date.
    """
    raise NotImplementedError("predict_forecast is not yet implemented")
