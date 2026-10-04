from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from .base import BaseModel


class NotificationModel(BaseModel):

    __tablename__ = "notifications"

    store_id = Column(
        ForeignKey("stores.id"),
        nullable=False
    )

    order_id = Column(
        ForeignKey("orders.id"),
        nullable=False
    )

    message = Column(
        String,
        nullable=False
    )

    type = Column(
        String,
        nullable=False
    )

    is_read = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    store = relationship(
        "StoreModel",
        back_populates="notifications"
    )

    order = relationship(
        "OrderModel",
        back_populates="notifications"
    )