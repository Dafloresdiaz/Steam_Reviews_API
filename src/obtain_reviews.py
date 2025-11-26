import requests
import time

class ObtainReviews:
    ENDPOINT = "https://store.steampowered.com/appreviews/"
    def __init__(self):
        self.game_id = None

    def fetch_reviews(self) -> list:
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