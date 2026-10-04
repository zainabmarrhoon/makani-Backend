from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from models.product import ProductModel
from models.store import StoreModel
from serializers.product import ProductCreateSchema, ProductUpdateSchema, ProductSchema
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()

@router.get("/stores/{store_id}/products", response_model=list[ProductSchema])
def get_products(store_id: int, db: Session = Depends(get_db)):
    products = db.query(ProductModel).filter(
        ProductModel.store_id == store_id
    ).all()

    return products

@router.post("/stores/{store_id}/products", response_model=ProductSchema, status_code=201)
def create_product(
    store_id: int,
    product: ProductCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    store = db.query(StoreModel).filter(
        StoreModel.id == store_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not store:
        raise HTTPException(status_code=404, detail="Store not found")

    new_product = ProductModel(
        store_id=store_id,
        name=product.name,
        description=product.description,
        price=product.price,
        image=product.image
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

@router.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(ProductModel).filter(
        ProductModel.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(
    product_id: int,
    product: ProductUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_product = db.query(ProductModel).join(StoreModel).filter(
        ProductModel.id == product_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.name is not None:
        db_product.name = product.name

    if product.description is not None:
        db_product.description = product.description

    if product.price is not None:
        db_product.price = product.price

    if product.image is not None:
        db_product.image = product.image

    db.commit()
    db.refresh(db_product)

    return db_product

@router.delete("/products/{product_id}", status_code=204)
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
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()