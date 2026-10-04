from fastapi import FastAPI

from controllers.notifications import (
    store_router,
    notification_router
)

app = FastAPI()

app.include_router(store_router)
app.include_router(notification_router)


@app.get("/")
def root():
    return {"message": "Makani Backend is running"}