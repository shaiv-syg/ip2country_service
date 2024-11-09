"""
Unit tests for the API module.
"""

import pytest
from fastapi.testclient import TestClient
from app.api import router
from fastapi import FastAPI

@pytest.fixture
def client():
    app = FastAPI()
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
    assert "Invalid IP address" in response.json()["detail"]

def test_find_country_not_found(client):
    response = client.get("/v1/find-country?ip=3.3.3.3")
    assert response.status_code == 404
    assert "IP address not found" in response.json()["detail"]

def test_rate_limiting(client):
    # Make multiple requests to trigger rate limiting
    for _ in range(6):  # One more than the limit
        response = client.get("/v1/find-country?ip=1.1.1.1")
    
    assert response.status_code == 429
    assert "Too Many Requests" in response.json()["detail"] 