from decimal import Decimal
from pydantic import BaseModel


class OrderProductCreateSchema(BaseModel):
    product_id: int
    quantity: int


class OrderProductSchema(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal

    class Config:
        from_attributes = True