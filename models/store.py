from sqlalchemy import Column, String, Text, ForeignKey, Boolean
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
    hero_image = Column(String)
    slug = Column(String, unique=True, nullable=False)
    status = Column(String, default="draft", nullable=False)

    show_home = Column(Boolean, default=True, nullable=False)
    show_products = Column(Boolean, default=True, nullable=False)
    show_about = Column(Boolean, default=True, nullable=False)
    show_contact = Column(Boolean, default=True, nullable=False)
    show_cart = Column(Boolean, default=True, nullable=False)

    hero_title = Column(String, default="Welcome to our store")
    hero_description = Column(Text)
    hero_button_text = Column(String, default="Shop Now")

    about_title = Column(String, default="About Us")
    about_description = Column(Text)

    owner = relationship(
        "UserModel",
        back_populates="stores"
    )

    products = relationship(
        "ProductModel",
        back_populates="store"
    )

    orders = relationship(
        "OrderModel",
        back_populates="store"
    )

    notifications = relationship(
        "NotificationModel",
        back_populates="store"
    )