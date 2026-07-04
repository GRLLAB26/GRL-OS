import csv
from dataclasses import dataclass
from typing import List, Optional

from app.db import get_session
from .models import Product


@dataclass
class ProductOut:
    id: int
    sku: str
    name: str
    description: str
    quantity: int
    price: float


def create_product(sku: str, name: str, description: str, quantity: int, price: float) -> ProductOut:
    with get_session() as s:
        product = Product(
            sku=sku,
            name=name,
            description=description,
            quantity=quantity,
            price=price,
        )
        s.add(product)
        s.flush()
        s.refresh(product)
        return ProductOut(
            id=product.id,
            sku=product.sku,
            name=product.name,
            description=product.description or "",
            quantity=product.quantity,
            price=product.price,
        )


def list_products() -> List[ProductOut]:
    with get_session() as s:
        rows = s.query(Product).order_by(Product.id).all()
        return [
            ProductOut(
                id=p.id,
                sku=p.sku,
                name=p.name,
                description=p.description or "",
                quantity=p.quantity,
                price=p.price,
            )
            for p in rows
        ]


def get_product(product_id: int) -> Optional[ProductOut]:
    with get_session() as s:
        p = s.get(Product, product_id)
        if not p:
            return None
        return ProductOut(
            id=p.id,
            sku=p.sku,
            name=p.name,
            description=p.description or "",
            quantity=p.quantity,
            price=p.price,
        )


def update_product(product_id: int, sku: str, name: str, description: str, quantity: int, price: float) -> Optional[ProductOut]:
    with get_session() as s:
        p = s.get(Product, product_id)
        if not p:
            return None
        p.sku = sku
        p.name = name
        p.description = description
        p.quantity = quantity
        p.price = price
        s.add(p)
        s.flush()
        s.refresh(p)
        return ProductOut(
            id=p.id,
            sku=p.sku,
            name=p.name,
            description=p.description or "",
            quantity=p.quantity,
            price=p.price,
        )


def get_product_by_sku(sku: str) -> Optional[ProductOut]:
    with get_session() as s:
        p = s.query(Product).filter(Product.sku == sku).one_or_none()
        if not p:
            return None
        return ProductOut(
            id=p.id,
            sku=p.sku,
            name=p.name,
            description=p.description or "",
            quantity=p.quantity,
            price=p.price,
        )


def delete_product(product_id: int) -> bool:
    with get_session() as s:
        p = s.get(Product, product_id)
        if not p:
            return False
        s.delete(p)
        return True


def export_products(file_path: str) -> int:
    products = list_products()
    with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["sku", "name", "description", "quantity", "price"])
        writer.writeheader()
        for p in products:
            writer.writerow(
                {
                    "sku": p.sku,
                    "name": p.name,
                    "description": p.description,
                    "quantity": p.quantity,
                    "price": p.price,
                }
            )
    return len(products)


def import_products(file_path: str, overwrite: bool = False) -> int:
    count = 0
    with open(file_path, mode="r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        with get_session() as s:
            for row in reader:
                sku = row.get("sku", "").strip()
                if not sku:
                    continue
                name = row.get("name", "").strip()
                description = row.get("description", "").strip()
                quantity = int(row.get("quantity", "0"))
                price = float(row.get("price", "0.0"))

                existing = s.query(Product).filter(Product.sku == sku).one_or_none()
                if existing:
                    if overwrite:
                        existing.name = name
                        existing.description = description
                        existing.quantity = quantity
                        existing.price = price
                        s.add(existing)
                        count += 1
                else:
                    p = Product(
                        sku=sku,
                        name=name,
                        description=description,
                        quantity=quantity,
                        price=price,
                    )
                    s.add(p)
                    count += 1
            if count:
                s.flush()
    return count
