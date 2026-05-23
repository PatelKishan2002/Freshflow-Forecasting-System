"""Load and validate dunnhumby Complete Journey transaction data from raw storage."""

from pathlib import Path

import pandas as pd


def load_dunnhumby(raw_dir: Path | None = None) -> dict[str, pd.DataFrame]:
    """Load dunnhumby source files from the configured raw directory.

    Args:
        raw_dir: Override path to raw dunnhumby data. If None, resolved from config.

    Returns:
        Dictionary of table name to DataFrame (transactions, products, etc.).
    """
    raise NotImplementedError("load_dunnhumby is not yet implemented")


def filter_perishable_departments(
    products: pd.DataFrame,
    departments: list[str] | None = None,
) -> pd.DataFrame:
    """Filter product catalog to perishable departments defined in config.

    Args:
        products: Product master DataFrame with department column.
        departments: Department names to retain. If None, read from config.

    Returns:
        Filtered product DataFrame.
    """
    raise NotImplementedError("filter_perishable_departments is not yet implemented")
