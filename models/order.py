from sqlalchemy import Column, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel


class OrderModel(BaseModel):

    __tablename__ = "orders"

    store_id = Column(ForeignKey("stores.id"), nullable=False)
    customer_name = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    customer_address = Column(Text, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    payment_method = Column(String, nullable=False)
    payment_proof = Column(String)
    payment_status = Column(String, default="pending", nullable=False)
    status = Column(String, default="pending", nullable=False)

    store = relationship("StoreModel", back_populates="orders")
    order_products = relationship("OrderProductModel", back_populates="order")
    notifications = relationship(
        "NotificationModel",
        back_populates="order"
    )