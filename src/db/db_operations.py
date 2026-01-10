from src.db.db_client import DBClient
from typing import Any

class DBOperations:
    """Handles database operations for sentiment analysis using Redis."""
    def __init__(self,):
        self.db_client  = DBClient()

    def set_sentiment(self, game_id: int, sentiment: str, reviews_count: int):
        """Store sentiment analysis data for a game in Redis.

        Args:
            game_id (int): The Steam game ID.
            sentiment (str): The analyzed sentiment (e.g., 'positive').
            reviews_count (int): The number of reviews analyzed.
        """
        self.db_client.redis_client.hset(str(game_id),
                                        mapping={
                                            "sentiment": sentiment,
                                            "reviews_count": reviews_count
                                         })
        self.db_client.redis_client.expire(str(game_id), 86400)  # Set expiration to 24 hours

    def get_sentiment(self, game_id: int)-> dict[str, str]:
        """Retrieve sentiment analysis data for a game from Redis.

        Args:
            game_id (int): The Steam game ID.

        Returns:
            dict: A dictionary with 'sentiment' (str) and 'reviews_count' (str), or empty dict if not found.
        """
        game_sentiment = self.db_client.redis_client.hgetall(str(game_id))
        return game_sentiment

    def sentiment_exists(self, game_id: int) -> bool:
        """Check if sentiment data exists for a game in Redis.

        Args:
            game_id (int): The Steam game ID.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        return self.db_client.redis_client.exists(str(game_id)) == 1