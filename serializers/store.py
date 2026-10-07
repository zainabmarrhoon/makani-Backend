from pydantic import BaseModel


class StoreCreateSchema(BaseModel):
    name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str

    show_home: bool = True
    show_products: bool = True
    show_about: bool = True
    show_contact: bool = True
    show_cart: bool = True
    show_orders: bool = True

    hero_title: str | None = None
    hero_description: str | None = None
    hero_button_text: str | None = None
    hero_image: str | None = None

    about_title: str | None = None
    about_description: str | None = None

    benefitpay_iban: str | None = None


class StoreUpdateSchema(BaseModel):
    name: str | None = None
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str | None = None
    status: str | None = None

    show_home: bool | None = None
    show_products: bool | None = None
    show_about: bool | None = None
    show_contact: bool | None = None
    show_cart: bool | None = None
    show_orders: bool | None = None

    hero_title: str | None = None
    hero_description: str | None = None
    hero_button_text: str | None = None
    hero_image: str | None = None

    about_title: str | None = None
    about_description: str | None = None

    benefitpay_iban: str | None = None


class StoreSchema(BaseModel):
    id: int
    owner_id: int
    name: str
    description: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    logo: str | None = None
    slug: str
    status: str

    show_home: bool
    show_products: bool
    show_about: bool
    show_contact: bool
    show_cart: bool
    show_orders: bool

    hero_title: str | None = None
    hero_description: str | None = None
    hero_button_text: str | None = None
    hero_image: str | None = None

    about_title: str | None = None
    about_description: str | None = None

    benefitpay_iban: str | None = None

    class Config:
        from_attributes = True