from functools import lru_cache
from typing import Any

from app.core.rate_limiter import RateLimiter
from app.database import get_ip2country_db
from app.config import IP_COUNTRY_DB

@lru_cache()
def get_rate_limiter() -> RateLimiter:
    return RateLimiter()

@lru_cache()
def get_ip_database() -> Any:
    return get_ip2country_db(IP_COUNTRY_DB) 