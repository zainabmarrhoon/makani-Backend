from decimal import Decimal
from pydantic import BaseModel


class OrderProductCreate(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class OrderProductResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True