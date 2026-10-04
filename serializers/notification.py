from datetime import datetime
from pydantic import BaseModel


class NotificationSchema(BaseModel):
    id: int
    store_id: int
    order_id: int
    message: str
    type: str
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True