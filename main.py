from fastapi import FastAPI, HTTPException
from src.obtain_reviews import ObtainReviews
from src.llm_model import LLM_Model
from src.models import SentimentRequest, SentimentResponse, ErrorResponse

app = FastAPI(
    title="Steam Reviews Sentiment Analysis API",
    description="API to analyze sentiment of Steam game reviews using LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

obtain_review = ObtainReviews()
llm = LLM_Model()

@app.get("/", 
         response_model=SentimentResponse,
         summary="Analyze sentiment for default game",
         description="Analyzes sentiment for game ID 2592160 (default game)",
         responses={
             200: {"description": "Successful sentiment analysis"},
             400: {"model": ErrorResponse, "description": "Bad request"},
             500: {"model": ErrorResponse, "description": "Internal server error"}
         })
def main_root():
    """
    Analyze sentiment for a game.
    Returns:
        SentimentResponse: Contains sentiment analysis and metadata.
    Raises:
        HTTPException: If analysis fails or game not found.
    """
    try:
        obtain_review.game_id = 2592160
        reviews = obtain_review.fetch_reviews()
        sentiment = llm.generate_sentiment(reviews=reviews)
        return SentimentResponse(
            game_id=2592160,
            sentiment=sentiment,
            reviews_count=len(reviews),
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze",
          response_model=SentimentResponse,
          summary="Analyze sentiment for specific game",
          description="Analyzes sentiment for a specific Steam game by ID",
          responses={
              200: {"description": "Successful sentiment analysis"},
              400: {"model": ErrorResponse, "description": "Invalid game ID"},
              500: {"model": ErrorResponse, "description": "Internal server error"}
          })
def analyze_sentiment(request: SentimentRequest):
    """
    Analyze sentiment for a specific Steam game.
    Args:
        request (SentimentRequest): Request containing game ID and optional limit.
    Returns:
        SentimentResponse: Contains sentiment analysis and metadata.
    Raises:
        HTTPException: If analysis fails or game not found.
    """
    try:
        obtain_review.game_id = request.game_id
        reviews = obtain_review.fetch_reviews()
        sentiment = llm.generate_sentiment(reviews=reviews)
        return SentimentResponse(
            game_id=request.game_id,
            sentiment=sentiment,
            reviews_count=len(reviews),
            success=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))