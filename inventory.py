from app.dashboard import get_inventory_summary


def main() -> None:
    summary = get_inventory_summary()
    print("Inventory dashboard")
    print("-------------------")
    print(f"Products: {summary.product_count}")
    print(f"Total quantity: {summary.total_quantity}")
    print(f"Total value: ${summary.total_value:.2f}")
    print(f"Low stock products: {len(summary.low_stock_products)}")
    if summary.reorder_suggestions:
        print("\nReorder suggestions:")
        for product, amount in summary.reorder_suggestions:
            print(f"  - {product.sku}: reorder {amount} units")


if __name__ == "__main__":
    main()
