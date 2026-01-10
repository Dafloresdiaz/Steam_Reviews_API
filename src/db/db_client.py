import redis
import logging

class DBClient:
    def __init__(self):
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