import logging

import pandas as pd

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned",
}


def validate_orders(data: pd.DataFrame) -> None:
    """Validate that the input has the minimum structure required by the program."""
    
    if data.empty:
        raise ValueError("Orderfilen innehåller inga rader.")

    missing_columns = REQUIRED_COLUMNS.difference(data.columns)
    
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Obligatoriska kolumner saknas: {missing}")

    logger.info("Grundvalidering av orderdata godkänd.")


def warn_about_unreasonable_values(data: pd.DataFrame) -> None:

    """Log warnings for suspicious values without changing valid calculations."""

    if (data["quantity"] < 0).any():
        logger.warning("Negativa värden hittades i quantity.")

    if (data["unit_price"] < 0).any():
        logger.warning("Negativa värden hittades i unit_price.")

    invalid_discount = (data["discount"] < 0) | (data["discount"] > 1)
    
    if invalid_discount.any():
        logger.warning("Rabattvärden utanför intervallet 0-1 hittades.")
