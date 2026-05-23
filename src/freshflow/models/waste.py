"""Waste and spoilage risk models using shelf-life and demand signals."""

from typing import Any

import pandas as pd


def estimate_waste_risk(
    forecasts: pd.DataFrame,
    inventory: pd.DataFrame | None = None,
    shelf_life_days: dict[str, int] | None = None,
) -> pd.DataFrame:
    """Estimate expected waste or spoilage risk by category and time.

    Args:
        forecasts: Demand forecasts from the forecast module.
        inventory: Optional on-hand inventory snapshot.
        shelf_life_days: Category-to-days mapping; if None, read from config.

    Returns:
        DataFrame with waste risk scores or expected units wasted.
    """
    raise NotImplementedError("estimate_waste_risk is not yet implemented")


def train_waste_model(
    features: pd.DataFrame,
    target: pd.Series,
    params: dict[str, Any] | None = None,
) -> Any:
    """Train a supervised waste model when labeled shrink data is available.

    Args:
        features: Training feature matrix.
        target: Observed waste or shrink labels.
        params: Optional model hyperparameters.

    Returns:
        Fitted model object.
    """
    raise NotImplementedError("train_waste_model is not yet implemented")
