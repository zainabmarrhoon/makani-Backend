from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class StoreModel(BaseModel):

    __tablename__ = "stores"

    owner_id = Column(ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    logo = Column(String)
    slug = Column(String, unique=True, nullable=False)
    status = Column(String, default="draft", nullable=False)

    owner = relationship("UserModel", back_populates="stores")