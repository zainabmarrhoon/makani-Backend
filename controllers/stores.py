from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from uuid import uuid4

from models.store import StoreModel
from models.product import ProductModel
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
        slug=slug,
        hero_description=description,
        about_description=description
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

    if store.hero_image is not None:
        db_store.hero_image = store.hero_image

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

    if store.benefitpay_iban is not None:
        db_store.benefitpay_iban = store.benefitpay_iban

    if store.show_home is not None:
        db_store.show_home = store.show_home

    if store.show_products is not None:
        db_store.show_products = store.show_products

    if store.show_about is not None:
        db_store.show_about = store.show_about

    if store.show_contact is not None:
        db_store.show_contact = store.show_contact

    if store.show_cart is not None:
        db_store.show_cart = store.show_cart

    if store.show_orders is not None:
        db_store.show_orders = store.show_orders

    if store.hero_title is not None:
        db_store.hero_title = store.hero_title

    if store.hero_description is not None:
        db_store.hero_description = store.hero_description

    if store.hero_button_text is not None:
        db_store.hero_button_text = store.hero_button_text

    if store.about_title is not None:
        db_store.about_title = store.about_title

    if store.about_description is not None:
        db_store.about_description = store.about_description

    db.commit()
    db.refresh(db_store)

    return db_store


@router.post("/stores/{store_id}/hero-image", response_model=StoreSchema)
def upload_hero_image(
    store_id: int,
    hero_image: UploadFile = File(...),
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

    allowed_types = [
        "image/jpeg",
        "image/png",
        "image/webp"
    ]

    if hero_image.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Hero image must be a JPG, PNG, or WEBP image"
        )

    file_extension = hero_image.filename.split(".")[-1]
    file_name = f"{uuid4().hex}.{file_extension}"

    hero_image_path = f"uploads/hero/{file_name}"

    with open(hero_image_path, "wb") as file:
        file.write(hero_image.file.read())

    store.hero_image = hero_image_path

    db.commit()
    db.refresh(store)

    return store


@router.get("/public/stores/{slug}")
def get_public_store(
    slug: str,
    db: Session = Depends(get_db)
):
    store = db.query(StoreModel).filter(
        StoreModel.slug == slug,
        StoreModel.status == "published"
    ).first()

    if not store:
        raise HTTPException(
            status_code=404,
            detail="Store not found"
        )

    products = db.query(ProductModel).filter(
        ProductModel.store_id == store.id
    ).all()

    return {
        "id": store.id,
        "name": store.name,
        "description": store.description,
        "phone": store.phone,
        "email": store.email,
        "address": store.address,
        "logo": store.logo,
        "hero_image": store.hero_image,
        "slug": store.slug,
        "status": store.status,
        "benefitpay_iban": store.benefitpay_iban,
        "show_home": store.show_home,
        "show_products": store.show_products,
        "show_about": store.show_about,
        "show_contact": store.show_contact,
        "show_cart": store.show_cart,
        "show_orders": store.show_orders,
        "hero_title": store.hero_title,
        "hero_description": store.hero_description,
        "hero_button_text": store.hero_button_text,
        "about_title": store.about_title,
        "about_description": store.about_description,
        "products": products
    }


@router.get("/stores/{store_id}/preview")
def preview_store(
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

    products = db.query(ProductModel).filter(
        ProductModel.store_id == store.id
    ).all()

    return {
        "id": store.id,
        "name": store.name,
        "description": store.description,
        "phone": store.phone,
        "email": store.email,
        "address": store.address,
        "logo": store.logo,
        "hero_image": store.hero_image,
        "slug": store.slug,
        "status": store.status,
        "benefitpay_iban": store.benefitpay_iban,
        "show_home": store.show_home,
        "show_products": store.show_products,
        "show_about": store.show_about,
        "show_contact": store.show_contact,
        "show_cart": store.show_cart,
        "show_orders": store.show_orders,
        "hero_title": store.hero_title,
        "hero_description": store.hero_description,
        "hero_button_text": store.hero_button_text,
        "about_title": store.about_title,
        "about_description": store.about_description,
        "products": products
    }


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