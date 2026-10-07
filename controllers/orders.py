
import json

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4

from models.order import OrderModel
from models.order_product import OrderProductModel
from models.product import ProductModel
from models.store import StoreModel
from models.notification import NotificationModel
from serializers.order import (
    OrderUpdateSchema,
    PaymentStatusUpdateSchema,
    OrderSchema
)
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()


@router.post(
    "/stores/{store_id}/orders",
    response_model=OrderSchema,
    status_code=201
)
def create_order(
    store_id: int,
    customer_name: str = Form(...),
    customer_phone: str = Form(...),
    customer_address: str = Form(...),
    payment_method: str = Form(...),
    products: str = Form(...),
    payment_proof: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    store = db.query(StoreModel).filter(
        StoreModel.id == store_id
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    try:
        products_data = json.loads(products)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid products data"
        )

    if not products_data:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one product"
        )

    payment_proof_path = None

    if payment_proof:
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if payment_proof.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Payment proof must be a JPG, PNG, or WEBP image"
            )

        file_extension = payment_proof.filename.split(".")[-1]
        file_name = f"{uuid4().hex}.{file_extension}"

        payment_proof_path = f"uploads/payments/{file_name}"

        with open(payment_proof_path, "wb") as file:
            file.write(payment_proof.file.read())

    total_amount = 0

    new_order = OrderModel(
        store_id=store_id,
        customer_name=customer_name,
        customer_phone=customer_phone,
        customer_address=customer_address,
        total_amount=0,
        payment_method=payment_method,
        payment_proof=payment_proof_path,
        payment_status="pending",
        status="pending"
    )

    db.add(new_order)
    db.flush()

    for item in products_data:
        product = db.query(ProductModel).filter(
            ProductModel.id == item["product_id"],
            ProductModel.store_id == store_id
        ).first()

        if not product:
            db.rollback()

            raise HTTPException(
                status_code=404,
                detail=f"Product {item['product_id']} not found"
            )

        quantity = int(item["quantity"])

        if quantity <= 0:
            db.rollback()

            raise HTTPException(
                status_code=400,
                detail="Product quantity must be greater than 0"
            )

        item_total = float(product.price) * quantity
        total_amount += item_total

        order_product = OrderProductModel(
            order_id=new_order.id,
            product_id=product.id,
            quantity=quantity,
            price=product.price
        )

        db.add(order_product)

    new_order.total_amount = total_amount

    notification = NotificationModel(
        store_id=store_id,
        order_id=new_order.id,
        message="New order received",
        type="new_order"
    )

    db.add(notification)

    db.commit()
    db.refresh(new_order)

    return new_order


@router.get(
    "/stores/{store_id}/orders",
    response_model=list[OrderSchema]
)
def get_store_orders(
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

    orders = db.query(OrderModel).filter(
        OrderModel.store_id == store_id
    ).all()

    return orders


@router.get(
    "/orders/{order_id}",
    response_model=OrderSchema
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = db.query(OrderModel).filter(
        OrderModel.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


@router.put(
    "/orders/{order_id}/status",
    response_model=OrderSchema
)
def update_order_status(
    order_id: int,
    order: OrderUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_order = db.query(OrderModel).join(StoreModel).filter(
        OrderModel.id == order_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db_order.status = order.status

    notification = NotificationModel(
        store_id=db_order.store_id,
        order_id=db_order.id,
        message=f"Order status changed to {order.status}",
        type="order_status"
    )

    db.add(notification)

    db.commit()
    db.refresh(db_order)

    return db_order


@router.put(
    "/orders/{order_id}/payment-status",
    response_model=OrderSchema
)
def update_payment_status(
    order_id: int,
    payment: PaymentStatusUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_order = db.query(OrderModel).join(StoreModel).filter(
        OrderModel.id == order_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if payment.payment_status not in ["verified", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Payment status must be verified or rejected"
        )

    db_order.payment_status = payment.payment_status

    notification = NotificationModel(
        store_id=db_order.store_id,
        order_id=db_order.id,
        message=f"Payment {payment.payment_status}",
        type="payment"
    )

    db.add(notification)

    db.commit()
    db.refresh(db_order)

    return db_order


@router.delete(
    "/orders/{order_id}",
    status_code=204
)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = db.query(OrderModel).join(StoreModel).filter(
        OrderModel.id == order_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return
