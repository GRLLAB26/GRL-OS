import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.inventory.models import Product
from app.db import Base


def test_create_product(tmp_path):
    db_file = tmp_path / "inventory.db"
    url = f"sqlite:///{db_file}"

    engine = create_engine(url, future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, future=True)

    with Session() as s:
        product = Product(sku="SKU123", name="Test Product", description="A test item", quantity=5, price=9.99)
        s.add(product)
        s.commit()
        s.refresh(product)

        assert product.id is not None
        assert product.sku == "SKU123"

        result = s.execute(text("SELECT count(*) FROM products")).scalar()
        assert result == 1
