from pydantic import BaseModel


class StoreCreateSchema(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str


class StoreUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str | None = None
    status: str | None = None


class StoreSchema(BaseModel):
    id: int
    owner_id: int
    name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str
    status: str

    class Config:
        from_attributes = True