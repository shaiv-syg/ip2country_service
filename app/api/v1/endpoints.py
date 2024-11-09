from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from app.core.rate_limiter import RateLimiter
from app.core.validators import is_valid_ip
from app.database import get_ip2country_db
from app.config import IP_COUNTRY_DB

router = APIRouter()
rate_limiter = RateLimiter()
ip2country_db = get_ip2country_db(IP_COUNTRY_DB)

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
async def find_country(ip: str, request: Request):
    client_ip = request.client.host
    if not is_valid_ip(ip):
        raise HTTPException(status_code=400, detail="Invalid IP address")
    if not rate_limiter.allow_request(client_ip):
        raise HTTPException(status_code=429, detail="Too Many Requests")
    location = ip2country_db.lookup(ip)
    if location:
        return location
    else:
        raise HTTPException(status_code=404, detail="IP address not found") 