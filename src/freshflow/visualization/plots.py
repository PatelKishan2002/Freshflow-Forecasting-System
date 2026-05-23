"""Visualization helpers for EDA, model diagnostics, and reporting."""

from pathlib import Path
from typing import Any

import matplotlib.figure
import pandas as pd


def plot_forecast_vs_actual(
    actual: pd.DataFrame,
    forecast: pd.DataFrame,
    output_path: Path | None = None,
) -> matplotlib.figure.Figure:
    """Plot actual vs forecasted demand over time.

    Args:
        actual: Actual demand series.
        forecast: Forecast series aligned to actual.
        output_path: If set, save figure to reports/figures via config paths.

    Returns:
        Matplotlib figure handle.
    """
    raise NotImplementedError("plot_forecast_vs_actual is not yet implemented")


def plot_waste_by_department(
    waste: pd.DataFrame,
    output_path: Path | None = None,
) -> matplotlib.figure.Figure:
    """Plot waste risk or shrink by perishable department.

    Args:
        waste: Waste estimates aggregated by department.
        output_path: Optional path to save the figure.

    Returns:
        Matplotlib figure handle.
    """
    raise NotImplementedError("plot_waste_by_department is not yet implemented")
