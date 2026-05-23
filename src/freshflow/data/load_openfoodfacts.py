"""Load Open Food Facts product exports for Canadian SKU enrichment."""

from pathlib import Path

import pandas as pd


def load_openfoodfacts(raw_dir: Path | None = None) -> pd.DataFrame:
    """Load Open Food Facts data from the configured raw directory.

    Args:
        raw_dir: Override path to raw Open Food Facts data. If None, resolved from config.

    Returns:
        Product attribute DataFrame.
    """
    raise NotImplementedError("load_openfoodfacts is not yet implemented")
