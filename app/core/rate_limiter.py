import time
import redis
import logging

from app.config import REDIS_HOST, REDIS_PORT, RATE_LIMIT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self):
        self.max_requests = RATE_LIMIT
        redis_host = REDIS_HOST
        redis_port = REDIS_PORT

        logger.info(f"Initializing Redis connection to {redis_host}:{redis_port}")

        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True,
            socket_connect_timeout=1,
            socket_keepalive=True,
            retry_on_timeout=True,
            health_check_interval=30
        )

        # Test connection on init
        try:
            self.redis_client.ping()
            logger.info("Successfully connected to Redis")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def allow_request(self, client_ip: str) -> bool:
        try:
            current_window = int(time.time())
            key = f"rate_limiter:{client_ip}:{current_window}"

            count = self.redis_client.incr(key)
            if count == 1:
                # Set TTL to 1 second
                self.redis_client.expire(key, 1)  

            return count <= self.max_requests
        except redis.ConnectionError as e:
            logger.error(f"Redis connection error: {e}")
            return True