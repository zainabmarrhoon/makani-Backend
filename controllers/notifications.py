from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.notification import NotificationModel
from serializers.notification import NotificationResponse


store_router = APIRouter(prefix="/stores", tags=["Notifications"])
notification_router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@store_router.get(
    "/{store_id}/notifications",
    response_model=list[NotificationResponse]
)
def get_store_notifications(
    store_id: int,
    db: Session = Depends(get_db)
):
    notifications = (
        db.query(NotificationModel)
        .filter(NotificationModel.store_id == store_id)
        .order_by(NotificationModel.created_at.desc())
        .all()
    )

    return notifications


@notification_router.put(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db)
):
    notification = (
        db.query(NotificationModel)
        .filter(NotificationModel.id == notification_id)
        .first()
    )

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification