import logging
import redis
import os

redis_url = os.getenv("REDIS_URL")

logging.basicConfig(level=logging.INFO)
class DBClient:
    def __init__(self):
        if redis_url:
            try :
                self.redis_client = redis.from_url(
                    redis_url, decode_responses=True
                )
            except redis.RedisError as e:
                logging.error(f"Redis connection error from Render server: {e}")
        else:
            try:
                self.redis_client = redis.Redis(
                    host='redis',
                    port=6379,
                    db=0,
                    decode_responses=True
                )
            except redis.RedisError as e:
                logging.error(f"Redis connection error: {e}")
                raise Exception(f"Error: {e}")