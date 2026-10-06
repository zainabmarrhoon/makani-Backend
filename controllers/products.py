
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4

from models.product import ProductModel
from models.store import StoreModel
from serializers.product import ProductSchema
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()


@router.get(
    "/stores/{store_id}/products",
    response_model=list[ProductSchema]
)
def get_products(
    store_id: int,
    db: Session = Depends(get_db)
):
    products = db.query(ProductModel).filter(
        ProductModel.store_id == store_id
    ).all()

    return products


@router.post(
    "/stores/{store_id}/products",
    response_model=ProductSchema,
    status_code=201
)
def create_product(
    store_id: int,
    name: str = Form(...),
    description: str | None = Form(None),
    price: float = Form(...),
    image: UploadFile | None = File(None),
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

    image_path = None

    if image:
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Product image must be a JPG, PNG, or WEBP image"
            )

        file_extension = image.filename.split(".")[-1]
        file_name = f"{uuid4().hex}.{file_extension}"

        image_path = f"uploads/products/{file_name}"

        with open(image_path, "wb") as file:
            file.write(image.file.read())

    new_product = ProductModel(
        store_id=store_id,
        name=name,
        description=description,
        price=price,
        image=image_path
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@router.get(
    "/products/{product_id}",
    response_model=ProductSchema
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db)
):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    return product


@router.put(
    "/products/{product_id}",
    response_model=ProductSchema
)
def update_product(
    product_id: int,
    name: str | None = Form(None),
    description: str | None = Form(None),
    price: float | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_product = db.query(ProductModel).join(StoreModel).filter(
        ProductModel.id == product_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    if name is not None:
        db_product.name = name

    if description is not None:
        db_product.description = description

    if price is not None:
        db_product.price = price

    if image:
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if image.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Product image must be a JPG, PNG, or WEBP image"
            )

        file_extension = image.filename.split(".")[-1]
        file_name = f"{uuid4().hex}.{file_extension}"

        image_path = f"uploads/products/{file_name}"

        with open(image_path, "wb") as file:
            file.write(image.file.read())

        db_product.image = image_path

    db.commit()
    db.refresh(db_product)

    return db_product


@router.delete(
    "/products/{product_id}",
    status_code=204
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_product = db.query(ProductModel).join(StoreModel).filter(
        ProductModel.id == product_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    db.delete(db_product)
    db.commit()

    return

