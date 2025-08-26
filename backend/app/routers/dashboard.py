import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from ..schemas import TickerData, ScoreData, MacroOutlookData, SentimentData
from ..services.market_data import get_ticker_data
from ..services.scoring import get_score_data
from ..services.indicators import get_macro_outlook_data, get_sentiment_data

router = APIRouter()

# Load environment variables
load_dotenv()

@router.get("/dashboard/ticker/{symbol}", response_model=TickerData)
async def read_ticker_data(symbol: str):
    data = get_ticker_data(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Ticker data not found")
    return data

@router.get("/dashboard/score/{symbol}", response_model=ScoreData)
async def read_score_data(symbol: str):
    data = get_score_data(symbol)
    if not data:
        raise HTTPException(status_code=404, detail="Score data not found")
    return data

@router.get("/dashboard/macro-outlook", response_model=List[MacroOutlookData])
async def read_macro_outlook():
    data = get_macro_outlook_data()
    if not data:
        raise HTTPException(status_code=404, detail="Macro outlook data not found")
    return data

@router.get("/dashboard/sentiment", response_model=SentimentData)
async def read_sentiment_data():
    data = get_sentiment_data()
    if not data:
        raise HTTPException(status_code=404, detail="Sentiment data not found")
    return data

@router.get("/dashboard/economic-calendar")
async def get_economic_calendar():
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="FRED API key not configured.")

    base_url = "https://api.stlouisfed.org/fred/releases/dates"
    
    today = datetime.now().date()
    start_filter_date = today - timedelta(days=30)
    end_filter_date = today + timedelta(days=30)

    params = {
        "api_key": api_key,
        "file_type": "json",
        "limit": 1000
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        fred_data = response.json()
        
        calendar_data = []
        if "release_dates" in fred_data:
            for release in fred_data["release_dates"]:
                release_date_str = release.get("date")
                if release_date_str:
                    release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
                    if start_filter_date <= release_date <= end_filter_date:
                        calendar_data.append({
                            "Date": release_date_str,
                            "Time": "N/A",
                            "Country": "USA",
                            "Event": release.get("release_name", "N/A"),
                            "Actual": "N/A",
                            "Forecast": "N/A",
                            "Previous": "N/A"
                        })
            calendar_data.sort(key=lambda x: x["Date"])
        
        return calendar_data
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching economic calendar data from FRED: {e}")