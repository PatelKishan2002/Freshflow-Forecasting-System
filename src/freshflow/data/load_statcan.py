"""Load Statistics Canada retail trade and food CPI tables from raw storage."""

from pathlib import Path

import pandas as pd


def load_statcan(raw_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    """Load StatCan CSV exports from the configured raw directory.

    Args:
        raw_dir: Override path to raw StatCan data. If None, resolved from config.

    Returns:
        Dictionary of dataset name to DataFrame (retail trade, CPI, etc.).
    """
    raise NotImplementedError("load_statcan is not yet implemented")
