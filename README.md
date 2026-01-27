# Steam Reviews Sentiment Analysis API

API to analyze sentiment of Steam game reviews using Large Language Models.

## How it works:
* We use the Steam API to obtain game reviews
* We process reviews with cardiffnlp/twitter-roberta-base-sentiment via HuggingFace
* We return a concise sentiment analysis summary

## API Endpoints

### Health Check
```http
GET /
```
Returns system status to verify the server is running.

**Response:**
```json
{
  "status": "system ok",
  "message": "Steam Reviews API is running"
}
```

### Sentiment Analysis
```http
GET /sentiments?game_id={game_id}&limit={limit}
```
Analyzes sentiment for Steam game reviews.

**Query Parameters:**
- `game_id` (optional): Steam game ID. If not provided, uses default game (2592160)
- `limit` (optional): Maximum number of reviews to analyze. Default is 200

**Examples:**
```bash
# Default game with default limit
GET /sentiments

# Specific game (CS:GO) with default limit
GET /sentiments?game_id=730

# Specific game with custom limit
GET /sentiments?game_id=730&limit=100
```

**Response:**
```json
{
  "game_id": 730,
  "sentiment": "The reviews for this game are generally positive...",
  "reviews_count": 100,
  "success": true
}
```

## Setup

### Prerequisites
- Python 3.11+
- Docker Compose
- HuggingFace API key

### Installation
```bash
pip install -r requirements.txt
```

### Environment Variables
```bash
export HUGGINGFACE_API_KEY="your_huggingface_api_key_here"
```

### Running the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running with Docker Compose
```bash
# Run the application with Docker Compose with no logs, remove the -d for logs
docker-compose up -d --build

# Stop the application (keeps containers for quick restart)
docker-compose stop

# For complete removal (stops and removes containers)
docker-compose down
```

**Note:** Ensure your `docker-compose.yaml` includes the service definition and environment variables (e.g., via `env_file: .env` or `environment`).

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Testing-TBD

## Example Usage
```bash
# Health check
curl http://localhost:8000/

# Analyze CS:GO reviews
curl "http://localhost:8000/sentiments?game_id=730&limit=50"
```
