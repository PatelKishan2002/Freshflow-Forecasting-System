"""Build modeling features from interim cleaned tables."""

from pathlib import Path

import pandas as pd


def build_features(
    interim_dir: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """Construct feature matrix for demand, waste, and markdown models.

    Args:
        interim_dir: Directory of per-source cleaned tables. If None, from config.
        output_path: Optional path to persist processed features.

    Returns:
        Modeling-ready feature DataFrame.
    """
    raise NotImplementedError("build_features is not yet implemented")
