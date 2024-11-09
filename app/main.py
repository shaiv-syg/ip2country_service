from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from app.api.router import router
from app.api.exceptions import http_exception_handler, validation_exception_handler

app = FastAPI(
    title="IP-to-Country Service",
    description="A production-ready service for IP geolocation",
    version="1.0.0"
)

# Add custom exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include API routes
app.include_router(router)