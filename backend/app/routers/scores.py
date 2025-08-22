from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..models import get_db
from sqlalchemy import desc

router = APIRouter(
    prefix="/scores",
    tags=["Scores"],
)

@router.get("/", response_model=List[schemas.TickerScoreResponse])
def get_all_latest_scores(db: Session = Depends(get_db)):
    """
    Retrieves the latest score for all tracked tickers.
    """
    tickers = db.query(models.Ticker).all()
    response = []
    for ticker in tickers:
        latest_score = db.query(models.DailyScore)\
            .filter(models.DailyScore.ticker_id == ticker.id)\
            .order_by(desc(models.DailyScore.date))\
            .first()
        
        pydantic_latest_score = None
        if latest_score:
            score_data = {
                "date": latest_score.date,
                "final_score": latest_score.final_score,
                "smoothed_score": latest_score.smoothed_score,
                "label": latest_score.label,
            }
            pydantic_latest_score = schemas.DailyScoreBase.model_validate(score_data)
        
        ticker_data = schemas.TickerScoreResponse(
            id=ticker.id,
            symbol=ticker.symbol,
            company_name=ticker.company_name,
            latest_score=pydantic_latest_score
        )
        response.append(ticker_data)
    return response

@router.get("/{symbol}", response_model=schemas.TickerDetailResponse)
def get_ticker_details(symbol: str, db: Session = Depends(get_db)):
    """
    Retrieves detailed information and a history of scores for a specific ticker.
    """
    ticker = db.query(models.Ticker).filter(models.Ticker.symbol == symbol.upper()).first()
    if not ticker:
        raise HTTPException(status_code=404, detail="Ticker not found")
        
    scores = db.query(models.DailyScore)\
        .filter(models.DailyScore.ticker_id == ticker.id)\
        .order_by(models.DailyScore.date.asc())\
        .all()
        
    pydantic_scores = []
    for score_obj in scores:
        score_data = {
            "date": score_obj.date,
            "final_score": score_obj.final_score,
            "smoothed_score": score_obj.smoothed_score,
            "label": score_obj.label,
        }
        pydantic_scores.append(schemas.DailyScoreBase.model_validate(score_data))
        
    return schemas.TickerDetailResponse(
        id=ticker.id,
        symbol=ticker.symbol,
        company_name=ticker.company_name,
        scores=pydantic_scores
    )
