from sqlalchemy import Column, String, Text, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class ProductModel(BaseModel):

    __tablename__ = "products"

    store_id = Column(ForeignKey("stores.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    image = Column(String)

    store = relationship("StoreModel", back_populates="products")