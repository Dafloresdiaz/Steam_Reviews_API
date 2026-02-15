from src.models import SentimentResponse, ErrorResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, Query
from src.db.db_operations import DBOperations
from src.obtain_reviews import ObtainReviews
from src.llm_model import LLM_Model
from typing import Optional

app = FastAPI(
    title="Steam Reviews Sentiment Analysis API",
    description="API to analyze sentiment of Steam game reviews using LLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

obtain_review = ObtainReviews()
llm = LLM_Model()
db = DBOperations()

@app.get("/",
         response_model=dict,
         summary="Health check endpoint",
         description="Returns system status to verify server is running",
         responses={
             200: {"description": "System is operational"}
         })
def health_check():
    """
    Health check endpoint to verify the server is running.
    Returns:
        dict: System status message.
    """
    return {"status": "system ok", "message": "Steam Reviews API is running"}

@app.get("/sentiments",
         response_model=SentimentResponse,
         summary="Analyze sentiment for Steam game reviews",
         description="Analyzes sentiment of reviews for any Steam game using query parameters",
         responses={
             200: {"description": "Successful sentiment analysis"},
             400: {"model": ErrorResponse, "description": "Bad request - invalid game ID or parameters"},
             500: {"model": ErrorResponse, "description": "Internal server error"}
         })
def analyze_sentiment(
    game_id: Optional[int] = Query(
        None,
        description="Steam game ID to analyze. If not provided, uses default game (2592160)"
    ),
    limit: Optional[int] = Query(
        200,
        description="Maximum number of reviews to fetch (default: 200)"
    )
):
    """
    Analyze sentiment for a Steam game using query parameters.
    Args:
        game_id (Optional[int]): Steam game ID. Uses default (2592160) if not provided.
        limit (Optional[int]): Maximum number of reviews to analyze. Default is 200.
    Returns:
        SentimentResponse: Contains sentiment analysis and metadata.
    Raises:
        HTTPException: If analysis fails or game ID is invalid.
    Examples:
        /sentiments?game_id=730&limit=100  # CS:GO with 100 reviews
        /sentiments?game_id=2592160        # Specific game with default limit
        /sentiments                        # Default game with default limit
    """
    try:
        # Use default game_id if not provided
        if game_id is None:
            game_id = 2592160
        # Set limit for ObtainReviews (currently hardcoded at 200, but we pass it for future flexibility)
        # Note: The fetch_reviews method has a hardcoded limit of 200 internally
        # Check if sentiment data is cached in Redis
        if db.sentiment_exists(game_id=game_id):
            # Retrieve cached data
            game_sentiment = db.get_sentiment(game_id=game_id)
            sentiment = game_sentiment["sentiment"]
            reviews_count = int(game_sentiment["reviews_count"])
        else:
            # Fetch new reviews and analyze sentiment
            obtain_review.game_id = game_id
            reviews = obtain_review.fetch_reviews()
            reviews_count = len(reviews)
            sentiment = llm.generate_general_sentiment(reviews=reviews)
            # Cache the result in Redis
            db.set_sentiment(
                game_id=game_id,
                sentiment=sentiment,
                reviews_count=reviews_count
            )
        return SentimentResponse(
            game_id=game_id,
            sentiment=sentiment,
            reviews_count=reviews_count,
            success=True
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))