from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.order_product import OrderProductModel
from models.order import OrderModel
from models.product import ProductModel
from serializers.order_product import (
    OrderProductCreateSchema,
    OrderProductSchema
)
from database import get_db

router = APIRouter()


@router.get(
    "/orders/{order_id}/products",
    response_model=list[OrderProductSchema]
)
def get_order_products(
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

    order_products = db.query(OrderProductModel).filter(
        OrderProductModel.order_id == order_id
    ).all()

    return order_products


@router.post(
    "/orders/{order_id}/products",
    response_model=OrderProductSchema,
    status_code=201
)
def create_order_product(
    order_id: int,
    order_product: OrderProductCreateSchema,
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

    product = db.query(ProductModel).filter(
        ProductModel.id == order_product.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    new_order_product = OrderProductModel(
        order_id=order_id,
        product_id=order_product.product_id,
        quantity=order_product.quantity,
        price=order_product.price
    )

    db.add(new_order_product)
    db.commit()
    db.refresh(new_order_product)

    return new_order_product