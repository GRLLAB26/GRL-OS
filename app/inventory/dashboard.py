from typing import List

from .product_repository import list_products


def calculate_reorder_amount(quantity: int) -> int:
    return max(10, 20 - quantity)


class InventorySummary:
    def __init__(self, products: List):
        self.product_count = len(products)
        self.total_quantity = sum(p.quantity for p in products)
        self.total_value = sum(p.quantity * p.price for p in products)
        self.products = products
        self.low_stock_products = [p for p in products if p.quantity <= 5]
        self.reorder_suggestions = self._calculate_reorder_suggestions()

    def _calculate_reorder_suggestions(self):
        suggestions = []
        for p in self.low_stock_products:
            reorder_amount = calculate_reorder_amount(p.quantity)
            suggestions.append((p, reorder_amount))
        return suggestions


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
    print(f"Low stock products: {len(summary.low_stock_products)}")
    if summary.product_count:
        print("\nProducts:")
        for p in summary.products:
            status = "LOW" if p.quantity <= 5 else "OK"
            print(f"  - {p.sku}: {p.name} ({p.quantity} units @ ${p.price:.2f}) [{status}]")

    if summary.reorder_suggestions:
        print("\nReorder suggestions:")
        for p, amount in summary.reorder_suggestions:
            print(f"  - {p.sku}: reorder {amount} units to reach a safer stock level")
