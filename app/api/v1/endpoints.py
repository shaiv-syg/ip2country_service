from fastapi import APIRouter, Request, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, Any
from app.core.rate_limiter import RateLimiter
from app.core.validators import is_valid_ip
from app.database import get_ip2country_db
from app.config import IP_COUNTRY_DB
from functools import lru_cache

router = APIRouter()

class Dependencies:
    _rate_limiter: Optional[RateLimiter] = None
    _ip_database: Optional[Any] = None

    @classmethod
    def get_rate_limiter(cls):
        if cls._rate_limiter is None:
            cls._rate_limiter = RateLimiter()
        return cls._rate_limiter

    @classmethod
    def get_ip_database(cls):
        if cls._ip_database is None:
            cls._ip_database = get_ip2country_db(IP_COUNTRY_DB)
        return cls._ip_database

class LocationResponse(BaseModel):
    country: str
    city: str

class ErrorResponse(BaseModel):
    error: str

@lru_cache()
def get_rate_limiter():
    return RateLimiter()

@lru_cache()
def get_ip_database():
    return get_ip2country_db(IP_COUNTRY_DB)

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
    ip2country_db: any = Depends(get_ip_database)
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