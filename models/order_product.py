from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class OrderProductModel(BaseModel):

    __tablename__ = "order_products"

    order_id = Column(
        ForeignKey("orders.id"),
        nullable=False
    )

    product_id = Column(
        ForeignKey("products.id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    price = Column(
        Numeric(10, 2),
        nullable=False
    )

    order = relationship(
        "OrderModel",
        back_populates="order_products"
    )

    product = relationship(
        "ProductModel",
        back_populates="order_products"
    )