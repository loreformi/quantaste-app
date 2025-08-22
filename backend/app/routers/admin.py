from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .. import models
from ..models import get_db
from ..services import data_ingestion, scoring
from ..services.admin_tasks import clean_invalid_tickers # Direct import of the function
import yfinance as yf # Import yfinance

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

class TickerRequest(BaseModel):
    symbol: str

@router.post("/tickers", status_code=202)
def add_ticker(request: TickerRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Adds a new ticker to the database and triggers an initial data fetch.
    Performs a basic validation to ensure the ticker symbol exists.
    """
    symbol = request.symbol.upper()

    # 1. Check if ticker already exists in DB
    db_ticker = db.query(models.Ticker).filter(models.Ticker.symbol == symbol).first()
    if db_ticker:
        return {"message": "Ticker already exists"}
    
    # 2. Validate ticker symbol using yfinance
    try:
        ticker_obj = yf.Ticker(symbol)
        # Attempt to get some basic info or history to validate
        # A common way to check validity is if info is not empty and has a longName
        info = ticker_obj.info
        if not info or not info.get('longName'):
            # If info is empty or doesn't have a longName, it's likely invalid
            raise HTTPException(status_code=400, detail=f"Invalid ticker symbol: {symbol}. No data found.")
        
        # Also check if history is available for a short period
        hist = ticker_obj.history(period="1d")
        if hist.empty:
            raise HTTPException(status_code=400, detail=f"Invalid ticker symbol: {symbol}. No historical data found.")

    except Exception as e:
        # Catch any exceptions from yfinance (e.g., network issues, invalid symbol format)
        raise HTTPException(status_code=400, detail=f"Validation failed for ticker {symbol}: {e}")

    # 3. If valid and not existing, proceed with background ingestion
    background_tasks.add_task(data_ingestion.ingest_data_for_ticker, db, symbol)
    background_tasks.add_task(scoring.calculate_and_store_scores_for_ticker, db, symbol)
    return {"message": f"Accepted. Task to add ticker {symbol} and ingest data has been started."}

@router.post("/run-update", status_code=202)
def trigger_full_update(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Manually triggers a full data ingestion and scoring update for all tickers.
    """
    background_tasks.add_task(scoring.update_all_ticker_scores, db)
    return {"message": "Accepted. Full data and scoring update initiated."}

@router.post("/clean-invalid-tickers", status_code=202)
def clean_tickers(background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Triggers a background task to identify and delete invalid ticker symbols and their associated data.
    """
    background_tasks.add_task(clean_invalid_tickers, db)
    return {"message": "Accepted. Invalid ticker cleanup initiated."}