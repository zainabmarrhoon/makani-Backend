from pydantic import BaseModel
from decimal import Decimal


class OrderProductBase(BaseModel):
    product_id: int
    quantity: int
    price: Decimal


class OrderProductCreate(OrderProductBase):
    pass


class OrderProductResponse(OrderProductBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True