from src.obtain_reviews import ObtainReviews as review
from src.llm_model import LLM_Model as llm

if __name__ == "__main__":
    obtain_review = review()
    llm = llm()
    obtain_review.game_id = 2592160
    print(llm.generate_sentiment(reviews=obtain_review.fetch_reviews()))