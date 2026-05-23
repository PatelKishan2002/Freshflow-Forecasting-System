"""Markdown timing and depth optimization for near-expiry inventory."""

import pandas as pd


def recommend_markdowns(
    waste_risk: pd.DataFrame,
    price_elasticity: pd.DataFrame | None = None,
    constraints: dict[str, float] | None = None,
) -> pd.DataFrame:
    """Recommend markdown depth and timing to minimize waste while protecting margin.

    Args:
        waste_risk: Waste risk estimates by SKU or category and date.
        price_elasticity: Optional elasticity estimates for demand response.
        constraints: Optional business rules (min price, max discount, etc.).

    Returns:
        DataFrame with recommended markdown actions.
    """
    raise NotImplementedError("recommend_markdowns is not yet implemented")
