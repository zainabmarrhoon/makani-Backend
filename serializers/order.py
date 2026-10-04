from pydantic import BaseModel


class OrderCreateSchema(BaseModel):
    customer_name: str
    customer_phone: str
    customer_address: str
    total_amount: float
    payment_method: str
    payment_proof: str | None = None


class OrderUpdateSchema(BaseModel):
    status: str


class OrderSchema(BaseModel):
    id: int
    store_id: int
    customer_name: str
    customer_phone: str
    customer_address: str
    total_amount: float
    payment_method: str
    payment_proof: str | None = None
    status: str

    class Config:
        from_attributes = True