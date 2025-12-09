from fastapi import FastAPI
from src.obtain_reviews import ObtainReviews
from src.llm_model import LLM_Model

app = FastAPI()
obtain_review = ObtainReviews()
llm = LLM_Model()

@app.get("/")
def main_root():
    obtain_review.game_id = 2592160
    return llm.generate_sentiment(reviews=obtain_review.fetch_reviews())