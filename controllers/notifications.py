from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.notification import NotificationModel
from models.store import StoreModel
from serializers.notification import NotificationSchema
from database import get_db
from dependencies.get_current_user import get_current_user


store_router = APIRouter(
    prefix="/stores",
    tags=["Notifications"]
)

notification_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


@store_router.get(
    "/{store_id}/notifications",
    response_model=list[NotificationSchema]
)
def get_store_notifications(
    store_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    store = db.query(StoreModel).filter(
        StoreModel.id == store_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    notifications = db.query(NotificationModel).filter(
        NotificationModel.store_id == store_id
    ).order_by(
        NotificationModel.created_at.desc()
    ).all()

    return notifications


@notification_router.put(
    "/{notification_id}/read",
    response_model=NotificationSchema
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notification = db.query(NotificationModel).join(StoreModel).filter(
        NotificationModel.id == notification_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=404,
            detail="Notification not found"
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification