"""
Unit tests for the RateLimiter class.
"""

import pytest
import time
from app.core.rate_limiter import RateLimiter

@pytest.fixture(autouse=True)
def clear_redis():
    # Create a limiter instance using the default rate limit
    limiter = RateLimiter()
    # Clear Redis before each test
    limiter.redis_client.flushall()
    yield limiter

def test_rate_limiter_allow_requests(clear_redis):
    limiter = clear_redis  # Use the fixture
    client_ip = "127.0.0.1"
    
    # First two requests should be allowed (based on RATE_LIMIT=2 from docker-compose.test.yml)
    assert limiter.allow_request(client_ip) is True
    assert limiter.allow_request(client_ip) is True
    
    # Third request should be blocked
    assert limiter.allow_request(client_ip) is False
    
    # Wait for 1 second and try again
    time.sleep(1.1)
    assert limiter.allow_request(client_ip) is True

def test_rate_limiter_multiple_clients(clear_redis):
    limiter = clear_redis  # Use the fixture
    client1 = "127.0.0.1"
    client2 = "127.0.0.2"
    
    # Both clients should be allowed their first two requests
    assert limiter.allow_request(client1) is True
    assert limiter.allow_request(client1) is True
    assert limiter.allow_request(client2) is True
    assert limiter.allow_request(client2) is True
    
    # Third request for each should be blocked
    assert limiter.allow_request(client1) is False
    assert limiter.allow_request(client2) is False 