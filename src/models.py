from pydantic import BaseModel
from typing import List, Optional

class SentimentRequest(BaseModel):
    """
    Request model for sentiment analysis.ß
    Attributes:
        game_id (int): Steam game ID to analyze reviews for.
        limit (Optional[int]): Maximum number of reviews to fetch (default: 200).
    """
    game_id: int
    limit: Optional[int] = 200

class SentimentResponse(BaseModel):
    """
    Response model for sentiment analysis.
    Attributes:
        game_id (int): Steam game ID that was analyzed.
        sentiment (str): Sentiment analysis summary.
        reviews_count (int): Number of reviews analyzed.
        success (bool): Whether the analysis was successful.
    """
    game_id: int
    sentiment: str
    reviews_count: int
    success: bool

class ErrorResponse(BaseModel):
    """
    Error response model.
    Attributes:
        error (str): Error message description.
        success (bool): Always False for error responses.
    """
    error: str
    success: bool = False