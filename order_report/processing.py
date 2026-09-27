import logging

import pandas as pd

from order_report.validation import validate_orders, warn_about_unreasonable_values

logger = logging.getLogger(__name__)

TRUE_VALUES = {"true", "yes", "1", "ja"}


def prepare_orders(data: pd.DataFrame) -> pd.DataFrame:
    """Clean order data and add calculated value columns.

    The transformations intentionally follow the behavior of the original
    program: invalid quantity becomes 1, invalid discount becomes 0 and
    missing unit_price is replaced by the median unit price.
    """
    
    validate_orders(data)
    prepared = data.copy()

    prepared["region"] = _clean_text_column(prepared["region"])
    
    prepared["product_category"] = _clean_text_column(
        prepared["product_category"]
    )

    prepared["quantity"] = _to_numeric_with_default(
        prepared["quantity"], default=1, column_name="quantity"
    )

    prepared["unit_price"] = pd.to_numeric(
        prepared["unit_price"], errors="coerce"
    )
    
    missing_unit_prices = int(prepared["unit_price"].isna().sum())
    
    if missing_unit_prices:
        logger.warning(
            "%d ogiltiga eller saknade unit_price-värden hittades.",
            missing_unit_prices,
        )

    if prepared["unit_price"].notna().sum() == 0:
        raise ValueError(
            "unit_price saknar användbara numeriska värden och kan inte fyllas med median."
        )

    median_price = prepared["unit_price"].median()
    
    if pd.isna(median_price):
        raise ValueError(
            "unit_price saknar användbara numeriska värden och kan inte fyllas med median."
        )
    
    prepared["unit_price"] = prepared["unit_price"].fillna(median_price)

    prepared["discount"] = _to_numeric_with_default(
        prepared["discount"], default=0, column_name="discount"
    )

    prepared["returned"] = (
        prepared["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(TRUE_VALUES)
    )

    warn_about_unreasonable_values(prepared)

    prepared["order_value"] = prepared["quantity"] * prepared["unit_price"]
    
    prepared["discounted_value"] = prepared["order_value"] * (
        1 - prepared["discount"]
    )

    logger.info("Databearbetning och beräkningar genomförda.")
    
    return prepared


def _clean_text_column(series: pd.Series) -> pd.Series:
    return series.fillna("Unknown").astype(str).str.strip().str.title()


def _to_numeric_with_default(
    series: pd.Series,
    default: float,
    column_name: str,
) -> pd.Series:
    
    numeric = pd.to_numeric(series, errors="coerce")
    invalid_count = int(numeric.isna().sum())

    if invalid_count:
        logger.warning(
            "%d ogiltiga eller saknade %s-värden ersätts med %s.",
            invalid_count,
            column_name,
            default,
        )

    return numeric.fillna(default)
