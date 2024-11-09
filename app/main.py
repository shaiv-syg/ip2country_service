from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api import router
from app.exceptions import http_exception_handler, validation_exception_handler

app = FastAPI(
    title="IP-to-Country Service",
    version="1.0.0"
)

# Add custom exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

app.include_router(router)