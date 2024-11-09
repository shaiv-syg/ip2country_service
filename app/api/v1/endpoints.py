from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Any
from app.core.validators import is_valid_ip
from app.api.dependencies import get_rate_limiter, get_ip_database
from app.core.rate_limiter import RateLimiter

router = APIRouter()

class LocationResponse(BaseModel):
    country: str
    city: str

class ErrorResponse(BaseModel):
    error: str

@router.get(
    "/find-country",
    response_model=LocationResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid IP address"},
        404: {"model": ErrorResponse, "description": "IP address not found"},
        429: {"model": ErrorResponse, "description": "Too Many Requests"},
    }
)
async def find_country(
    ip: str, 
    request: Request,
    rate_limiter: RateLimiter = Depends(get_rate_limiter),
    ip2country_db: Any = Depends(get_ip_database)
):
    client_ip = request.client.host
    if not rate_limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    if not is_valid_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address")
    location = ip2country_db.lookup(ip)
    if location:
        return location
    else:
        raise HTTPException(status_code=404, detail="IP address not found") 