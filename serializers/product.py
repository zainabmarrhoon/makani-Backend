from pydantic import BaseModel

class ProductCreateSchema(BaseModel):
    name: str
    description: str | None = None
    price: float
    image: str | None = None

class ProductUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    image: str | None = None

class ProductSchema(BaseModel):
    id: int
    store_id: int
    name: str
    description: str | None = None
    price: float
    image: str | None = None

    class Config:
        from_attributes = True