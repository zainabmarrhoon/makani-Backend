from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4
import os

from models.store import StoreModel
from serializers.store import StoreUpdateSchema, StoreSchema
from database import get_db
from dependencies.get_current_user import get_current_user

router = APIRouter()


@router.get("/stores", response_model=list[StoreSchema])
def get_stores(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    stores = db.query(StoreModel).filter(
        StoreModel.owner_id == current_user.id
    ).all()

    return stores


@router.post("/stores", response_model=StoreSchema, status_code=201)
def create_store(
    name: str = Form(...),
    description: str | None = Form(None),
    phone: str | None = Form(None),
    email: str | None = Form(None),
    address: str | None = Form(None),
    slug: str = Form(...),
    logo: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    existing_store = db.query(StoreModel).filter(
        StoreModel.slug == slug
    ).first()

    if existing_store:
        raise HTTPException(
            status_code=409,
            detail="Store slug already exists"
        )

    logo_path = None

    if logo:
        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ]

        if logo.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Logo must be a JPG, PNG, or WEBP image"
            )

        file_extension = logo.filename.split(".")[-1]
        file_name = f"{uuid4().hex}.{file_extension}"

        logo_path = f"uploads/logos/{file_name}"

        with open(logo_path, "wb") as file:
            file.write(logo.file.read())

    new_store = StoreModel(
        owner_id=current_user.id,
        name=name,
        description=description,
        phone=phone,
        email=email,
        address=address,
        logo=logo_path,
        slug=slug
    )

    db.add(new_store)
    db.commit()
    db.refresh(new_store)

    return new_store


@router.get("/stores/{store_id}", response_model=StoreSchema)
def get_store(
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

    return store


@router.put("/stores/{store_id}", response_model=StoreSchema)
def update_store(
    store_id: int,
    store: StoreUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_store = db.query(StoreModel).filter(
        StoreModel.id == store_id,
        StoreModel.owner_id == current_user.id
    ).first()

    if not db_store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    if store.name is not None:
        db_store.name = store.name

    if store.description is not None:
        db_store.description = store.description

    if store.phone is not None:
        db_store.phone = store.phone

    if store.email is not None:
        db_store.email = store.email

    if store.address is not None:
        db_store.address = store.address

    if store.logo is not None:
        db_store.logo = store.logo

    if store.slug is not None:
        existing_store = db.query(StoreModel).filter(
            StoreModel.slug == store.slug,
            StoreModel.id != store_id
        ).first()

        if existing_store:
            raise HTTPException(
                status_code=409,
                detail="Store slug already exists"
            )

        db_store.slug = store.slug

    if store.status is not None:
        db_store.status = store.status

    db.commit()
    db.refresh(db_store)

    return db_store


@router.delete("/stores/{store_id}", status_code=204)
def delete_store(
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

    db.delete(store)
    db.commit()

    return