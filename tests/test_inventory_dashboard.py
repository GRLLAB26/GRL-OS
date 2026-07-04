from app.inventory.dashboard import InventorySummary
from app.inventory.models import Product


def test_reorder_suggestions():
    products = [
        Product(id=1, sku="A1", name="LowStock", description="", quantity=3, price=10.0),
        Product(id=2, sku="A2", name="MediumStock", description="", quantity=12, price=5.0),
    ]

    summary = InventorySummary(products)
    assert len(summary.low_stock_products) == 1
    assert summary.reorder_suggestions == [(products[0], 17)]
