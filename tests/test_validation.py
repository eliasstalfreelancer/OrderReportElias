import pandas as pd
import pytest

from order_report.processing import prepare_orders
from order_report.validation import validate_orders


def test_missing_required_column_raises_value_error(sample_orders):
    data = sample_orders.drop(columns=["region"])

    with pytest.raises(ValueError, match="region"):
        validate_orders(data)


def test_empty_data_raises_value_error(sample_orders):
    empty_data = sample_orders.iloc[0:0]

    with pytest.raises(ValueError, match="inga rader"):
        validate_orders(empty_data)


def test_all_invalid_unit_prices_raise_clear_error(sample_orders):
    data = sample_orders.copy()
    data["unit_price"] = [None, "fel", "-"]

    with pytest.raises(ValueError, match="unit_price"):
        prepare_orders(data)
