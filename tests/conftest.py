import pandas as pd
import pytest


@pytest.fixture
def sample_orders() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "order_date": ["2026-01-01", "2026-01-02", "2026-01-03"],
            "customer_id": [101, 102, 103],
            "region": [" north ", "south", "north"],
            "product_category": ["books", "games", "books"],
            "quantity": [2, 1, 3],
            "unit_price": [100.0, 200.0, 50.0],
            "discount": [0.10, 0.0, 0.20],
            "returned": ["false", "yes", "ja"],
        }
    )
