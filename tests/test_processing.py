import pandas as pd

from order_report.processing import prepare_orders


def test_order_values_are_calculated_correctly(sample_orders):
    
    result = prepare_orders(sample_orders)

    assert result.loc[0, "order_value"] == 200.0
    assert result.loc[0, "discounted_value"] == 180.0
    assert result.loc[2, "order_value"] == 150.0
    assert result.loc[2, "discounted_value"] == 120.0


def test_text_and_return_values_are_normalized(sample_orders):
    
    result = prepare_orders(sample_orders)

    assert result["region"].tolist() == ["North", "South", "North"]
    assert result["product_category"].tolist() == ["Books", "Games", "Books"]
    assert result["returned"].tolist() == [False, True, True]


def test_invalid_numeric_values_use_same_fallbacks_as_original(sample_orders):
    
    data = sample_orders.copy()
    
    data[["quantity", "discount", "unit_price"]] = data[[
        "quantity", "discount", "unit_price"
    ]].astype(object)
    
    data.loc[0, "quantity"] = "invalid"
    data.loc[1, "discount"] = "invalid"
    data.loc[2, "unit_price"] = "invalid"

    result = prepare_orders(data)

    assert result.loc[0, "quantity"] == 1
    assert result.loc[1, "discount"] == 0
    assert result.loc[2, "unit_price"] == 150.0
