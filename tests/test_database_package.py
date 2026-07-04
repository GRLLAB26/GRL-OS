import os


def test_repository_and_dashboard(tmp_path):
    db_file = tmp_path / "inventory.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_file}"

    from database.repository import create_product, list_products
    from app.dashboard import get_inventory_summary

    create_product("SKU-1", "Widget", "A sample widget", 4, 12.5)
    create_product("SKU-2", "Gadget", "Another sample", 1, 9.0)

    products = list_products()
    assert len(products) == 2
    assert products[0].sku == "SKU-1"

    summary = get_inventory_summary()
    assert summary.product_count == 2
    assert summary.total_quantity == 5
    assert summary.low_stock_products[0].sku == "SKU-2"
