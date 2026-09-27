from order_report.processing import prepare_orders
from order_report.reports import (
    create_overview,
    create_returns_by_category,
    create_sales_by_category,
    create_sales_by_region,
)


def test_overview_contains_expected_values(sample_orders):
    
    data = prepare_orders(sample_orders)
    
    overview = create_overview(data).set_index("metric")["value"]

    assert overview["total_sales"] == 500.0
    assert overview["order_count"] == 3
    assert overview["return_count"] == 2


def test_sales_by_category_is_summarized_correctly(sample_orders):
    
    data = prepare_orders(sample_orders)
    
    report = create_sales_by_category(data)

    books = report.loc[report["product_category"] == "Books"].iloc[0]
    
    games = report.loc[report["product_category"] == "Games"].iloc[0]

    assert books["order_count"] == 2
    assert books["total_sales"] == 300.0
    assert books["returns"] == 1
    assert books["return_rate"] == 0.5

    assert games["total_sales"] == 200.0
    assert games["return_rate"] == 1.0


def test_sales_by_region_is_summarized_correctly(sample_orders):
    data = prepare_orders(sample_orders)
    
    report = create_sales_by_region(data)

    north = report.loc[report["region"] == "North"].iloc[0]
    
    assert north["order_count"] == 2
    assert north["total_sales"] == 300.0


def test_returns_by_category_sorts_highest_return_rate_first(sample_orders):
    data = prepare_orders(sample_orders)
    
    report = create_returns_by_category(data)

    assert report.iloc[0]["product_category"] == "Games"
    assert report.iloc[0]["return_rate"] == 1.0
