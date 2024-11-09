#!/bin/bash
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate ip2country_env

# Set environment variables
export REDIS_HOST=localhost
export REDIS_PORT=6381
export RATE_LIMIT=2


# Run the application
uvicorn app.main:app --reload 