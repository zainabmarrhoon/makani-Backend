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
    slug = Column(String, unique=True, nullable=False)
    status = Column(String, default="draft", nullable=False)

    # Store navigation settings
    show_home = Column(Boolean, default=True, nullable=False)
    show_products = Column(Boolean, default=True, nullable=False)
    show_about = Column(Boolean, default=True, nullable=False)
    show_contact = Column(Boolean, default=True, nullable=False)
    show_cart = Column(Boolean, default=True, nullable=False)
    show_orders = Column(Boolean, default=True, nullable=False)

    # Hero section
    hero_title = Column(String)
    hero_description = Column(Text)
    hero_button_text = Column(String)
    hero_image = Column(String)

    # About section
    about_title = Column(String)
    about_description = Column(Text)

    # BenefitPay
    benefitpay_iban = Column(String)

    owner = relationship("UserModel", back_populates="stores")
    products = relationship("ProductModel", back_populates="store")
    orders = relationship("OrderModel", back_populates="store")
    notifications = relationship(
        "NotificationModel",
        back_populates="store"
    )