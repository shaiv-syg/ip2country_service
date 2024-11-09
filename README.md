# IP 2 Country Rate Limited Service

This repository demonstrates a production-grade implementation of an IP-2-Country service exercise. The service provides IP geolocation functionality with built-in rate limiting and extensible database support.

## Exercise Requirements

The service was built according to the following requirements:

1. Clear and readable code implementation
2. Configurable service architecture
3. REST API endpoint at `/v1/find-country?ip=2.22.233.255` returning location data in JSON format:
   ```json
   {
       "country": "XXXX",
       "city": "XXXX"
   }
   ```
4. JSON error responses with appropriate HTTP status codes:
   ```json
   {
       "error": "XXX"
   }
   ```
5. Extensible design supporting multiple IP-2-Country databases (currently implements CSV) but easily extensible to other database types
6. Custom rate-limiting mechanism with configurable requests per second
7. Production-grade implementation with proper testing, configuration, and deployment setup

## Features

- FastAPI-based REST API
- Custom rate limiting implementation using Redis
- Configurable through YAML and environment variables
- Extensible IP database support (currently CSV-based)
- Docker and Docker Compose support
- Test suite
- Development and production configurations

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Conda
## Quick Start

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ip-to-country-service
   ```

2. Run with Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. For development:

   One-time setup:
   ```bash
   # Create and activate conda environment
   conda create -n ip2country_env python=3.9
   conda activate ip2country_env

   # Install requirements
   pip install -r requirements.txt
   ```

   Each time you develop:
   ```bash
   # Start Redis for development
   docker-compose -f docker-compose.dev.yml up -d

   # Run the development server
   ./scripts/run_dev.sh
   ```

4. Run tests:
   ```bash
   ./scripts/run_tests.sh
   ```

## API Documentation

### GET /v1/find-country

Get country and city information for an IP address.

**Parameters:**
- `ip` (string, required): The IP address to look up

**Success Response (200):** 