from typing import List

from database.repository import list_products


LOW_STOCK_LIMIT = 5
TARGET_STOCK = 20
MIN_REORDER = 10


class InventorySummary:
    def __init__(self, products: List):
        self.products = products

        self.product_count = len(products)
        self.total_quantity = sum(p.quantity for p in products)
        self.total_value = sum(p.quantity * p.price for p in products)

        self.low_stock_products = sorted(
            [p for p in products if p.quantity <= LOW_STOCK_LIMIT],
            key=lambda p: p.quantity,
        )

        self.reorder_suggestions = self._calculate_reorder_suggestions()

    def _calculate_reorder_suggestions(self):
        suggestions = []

        for product in self.low_stock_products:
            reorder_amount = max(
                MIN_REORDER,
                TARGET_STOCK - product.quantity,
            )

            suggestions.append((product, reorder_amount))

        return suggestions


def get_inventory_summary() -> InventorySummary:
    try:
        products = list_products()
    except Exception:
        products = []

    return InventorySummary(products)