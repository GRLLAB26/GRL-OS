from typing import List

from .product_repository import list_products


class InventorySummary:
    def __init__(self, products: List):
        self.product_count = len(products)
        self.total_quantity = sum(p.quantity for p in products)
        self.total_value = sum(p.quantity * p.price for p in products)
        self.products = products


def get_inventory_summary() -> InventorySummary:
    products = list_products()
    return InventorySummary(products)


def print_inventory_dashboard() -> None:
    summary = get_inventory_summary()
    print("Inventory dashboard")
    print("-------------------")
    print(f"Products: {summary.product_count}")
    print(f"Total quantity: {summary.total_quantity}")
    print(f"Total value: ${summary.total_value:.2f}")
    if summary.product_count:
        print("\nProducts:")
        for p in summary.products:
            print(f"  - {p.sku}: {p.name} ({p.quantity} units @ ${p.price:.2f})")
