"""
Write a function to get Redis DB connection which can be used as a
singleton across the application.
"""
import logging

from redis import Redis
from redis.exceptions import RedisError
from dotenv import load_dotenv
import os
load_dotenv()

_redis_instance = None
def get_redis_db() -> Redis:
    """Get a singleton Redis DB connection."""
    global _redis_instance
    if _redis_instance is None:
        try:
            _redis_instance = Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                password=os.getenv("REDIS_PASSWORD", None),
                decode_responses=True
            )
            # Test the connection
            _redis_instance.ping()
            logging.info("Connected to Redis successfully")
        except RedisError as e:
            logging.info(f"❌ Failed to connect to Redis: {e}")
            raise e
    return _redis_instance