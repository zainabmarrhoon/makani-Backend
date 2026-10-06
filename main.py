from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from controllers.order_products import router as order_products_router
from controllers.auth import router as auth_router
from controllers.products import router as products_router
from controllers.stores import router as stores_router
from controllers.orders import router as orders_router
from controllers.notifications import (
    store_router,
    notification_router
)

app = FastAPI()

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.add_middleware(
    CORSMiddleware,

allow_origins=[
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175"
],


    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(products_router, tags=["Products"])
app.include_router(stores_router, tags=["Stores"])
app.include_router(orders_router, tags=["Orders"])
app.include_router(store_router)
app.include_router(notification_router)
app.include_router(order_products_router, tags=["Order Products"])

@app.get("/")
def root():
    return {"message": "Makani API is running"}