from fastapi import APIRouter
from app.api.v1 import endpoints as v1_endpoints

# Create the router instance to export
router = APIRouter()

# Include versioned routes
router.include_router(v1_endpoints.router, prefix="/v1") 