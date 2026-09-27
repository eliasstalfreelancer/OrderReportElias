import logging

import pandas as pd

logger = logging.getLogger(__name__)


def create_overview(data: pd.DataFrame) -> pd.DataFrame:
    """Create the overall sales and return summary."""
    
    total_sales = round(data["discounted_value"].sum(), 2)
    number_of_orders = data["order_id"].nunique()
    number_of_returns = int(data["returned"].sum())

    return pd.DataFrame(
        {
            "metric": ["total_sales", "order_count", "return_count"],
            "value": [total_sales, number_of_orders, number_of_returns],
        }
    )


def create_sales_by_category(data: pd.DataFrame) -> pd.DataFrame:
    """Create sales summary grouped by product category."""
    return _create_sales_summary(data, "product_category")


def create_sales_by_region(data: pd.DataFrame) -> pd.DataFrame:
    """Create sales summary grouped by region."""
    return _create_sales_summary(data, "region")


def create_returns_by_category(data: pd.DataFrame) -> pd.DataFrame:
    """Create return summary grouped by product category."""
    
    report = (
        data.groupby("product_category", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            returns=("returned", "sum"),
        )
    )

    report["return_rate"] = (
        report["returns"] / report["order_count"]
    ).round(3)

    return report.sort_values(
        "return_rate", ascending=False
    ).reset_index(drop=True)


def generate_reports(data: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Generate every report produced by the application."""
    
    reports = {
        "overview.csv": create_overview(data),
        "sales_by_category.csv": create_sales_by_category(data),
        "sales_by_region.csv": create_sales_by_region(data),
        "returns_by_category.csv": create_returns_by_category(data),
    }
    
    logger.info("Skapade %d rapporter.", len(reports))
    
    return reports


def _create_sales_summary(
    data: pd.DataFrame,
    group_column: str,
) -> pd.DataFrame:
    
    """Create the shared sales summary used for category and region reports."""
    
    report = (
        data.groupby(group_column, as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            total_sales=("discounted_value", "sum"),
            returns=("returned", "sum"),
        )
    )

    report["total_sales"] = report["total_sales"].round(2)
    
    report["return_rate"] = (
        report["returns"] / report["order_count"]
    ).round(3)

    return report.sort_values(
        "total_sales", ascending=False
    ).reset_index(drop=True)
