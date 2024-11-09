"""
Unit tests for the API module.
"""

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.api import router

@pytest.fixture
def client():
    app = FastAPI()
    
    # Add custom exception handlers
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.detail}
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        return JSONResponse(
            status_code=400,
            content={"error": "Invalid request parameters"}
        )

    app.include_router(router)
    return TestClient(app)

def test_find_country_valid_ip(client):
    response = client.get("/v1/find-country?ip=1.1.1.1")
    assert response.status_code == 200
    assert response.json() == {
        "country": "Australia",
        "city": "Sydney"
    }

def test_find_country_invalid_ip(client):
    response = client.get("/v1/find-country?ip=invalid_ip")
    assert response.status_code == 400
    assert response.json() == {"error": "Invalid IP address"}

def test_find_country_not_found(client):
    response = client.get("/v1/find-country?ip=3.3.3.3")
    assert response.status_code == 404
    assert response.json() == {"error": "IP address not found"}

def test_rate_limiting(client):
    # Make multiple requests to trigger rate limiting
    for _ in range(6):  # One more than the limit
        response = client.get("/v1/find-country?ip=1.1.1.1")
    
    assert response.status_code == 429
    assert response.json() == {"error": "Too Many Requests"} 