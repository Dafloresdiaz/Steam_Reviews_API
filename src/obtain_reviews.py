import requests
import time
from typing import List, Optional

class ObtainReviews:
    """
    Class to fetch game reviews from Steam API.
    This class handles the retrieval of user reviews for a specific game
    from the Steam store API, with pagination support.
    """

    ENDPOINT = "https://store.steampowered.com/appreviews/"

    def __init__(self):
        """
        Initialize the ObtainReviews instance.
        Attributes:
            game_id (Optional[int]): Steam game ID to fetch reviews for.
        """
        self.game_id: Optional[int] = None

    def fetch_reviews(self) -> List[str]:
        """
        Fetch reviews from Steam API for the specified game.
        Returns:
            List[str]: List of review texts from the game.
        Raises:
            Exception: If API request fails or game_id is not set.
        Note:
            Fetches up to 200 reviews in English with pagination support.
            Includes rate limiting to avoid API throttling.
        """
        if not self.game_id:
            raise ValueError("Game ID must be set before fetching reviews")

        all_reviews = []
        cursor = '*'
        limit = 200
        number_review = 1
        while True:
            url = f"{self.ENDPOINT}{self.game_id}"
            params = {
                "json": 1,
                "language": "english",
                "num_per_page": limit,
                "cursor": cursor
            }
            response = requests.get(url, params=params)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch reviews: {response.status_code}")

            data = response.json()
            new_cursor = data.get('cursor', None)
            reviews = data.get('reviews', [])
            if not reviews or new_cursor == cursor:
                break

            for review in reviews:
                all_reviews.append(review.get('review'))
                number_review += 1
                if len(all_reviews) >= limit:
                    return all_reviews
            cursor = new_cursor
            time.sleep(0.2)
        return all_reviews