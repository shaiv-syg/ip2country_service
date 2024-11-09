from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="IP-to-Country Service",
    version="1.0.0"
)

app.include_router(router)