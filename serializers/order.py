from decimal import Decimal
from pydantic import BaseModel


class OrderUpdateSchema(BaseModel):
    status: str


class PaymentStatusUpdateSchema(BaseModel):
    payment_status: str


class OrderSchema(BaseModel):
    id: int
    store_id: int
    customer_name: str
    customer_phone: str
    customer_address: str
    total_amount: Decimal
    payment_method: str
    payment_proof: str | None = None
    payment_status: str
    status: str

    class Config:
        from_attributes = True