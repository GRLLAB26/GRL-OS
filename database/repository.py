from dataclasses import dataclass
from typing import List, Optional

from app.db import get_session, init_db
from .models import Product

init_db()


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
