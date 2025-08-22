
import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from sklearn.preprocessing import MinMaxScaler

from .. import models
from . import indicators

# --- SCORING LOGIC ---
# This is a sample implementation. You can adjust weights and logic here.

# 1. Weights Configuration
FUNDAMENTAL_WEIGHT = 0.50
TECHNICAL_WEIGHT = 0.50

FUNDAMENTAL_METRICS_WEIGHTS = {
    "pe_ratio": 0.25,       # Lower is better
    "pb_ratio": 0.25,       # Lower is better
    "debt_to_equity": 0.25, # Lower is better
    "roe": 0.25,            # Higher is better
}

TECHNICAL_INDICATORS_WEIGHTS = {
    "rsi": 0.30,            # Score based on non-extreme values
    "macd": 0.30,           # Score based on MACD line vs Signal line
    "trend": 0.25,          # Score based on SMA 50 vs SMA 200
    "bollinger": 0.15,      # Score based on price position within bands
}

# 2. Scoring Functions

def score_pe_ratio(value):
    if value is None or value <= 0: return 0
    if value < 10: return 100
    if value < 15: return 80
    if value < 20: return 60
    if value < 25: return 40
    if value < 30: return 20
    return 0

def score_pb_ratio(value):
    if value is None or value <= 0: return 0
    if value < 1: return 100
    if value < 1.5: return 80
    if value < 2: return 60
    if value < 3: return 40
    return 20

def score_debt_to_equity(value):
    if value is None: return 50 # Neutral if unknown
    if value < 0.3: return 100
    if value < 0.6: return 80
    if value < 1.0: return 60
    if value < 1.5: return 40
    return 20

def score_roe(value):
    if value is None: return 50 # Neutral if unknown
    if value > 0.20: return 100
    if value > 0.15: return 80
    if value > 0.10: return 60
    if value > 0.05: return 40
    return 20

def calculate_fundamental_score(fundamentals: models.Fundamental):
    if not fundamentals:
        return 0

    pe_score = score_pe_ratio(fundamentals.pe_ratio) * FUNDAMENTAL_METRICS_WEIGHTS["pe_ratio"]
    pb_score = score_pb_ratio(fundamentals.pb_ratio) * FUNDAMENTAL_METRICS_WEIGHTS["pb_ratio"]
    de_score = score_debt_to_equity(fundamentals.debt_to_equity) * FUNDAMENTAL_METRICS_WEIGHTS["debt_to_equity"]
    roe_score = score_roe(fundamentals.roe) * FUNDAMENTAL_METRICS_WEIGHTS["roe"]
    
    total_score = pe_score + pb_score + de_score + roe_score
    return total_score

def calculate_technical_score(tech_df: pd.DataFrame):
    if tech_df.empty:
        return 0
    
    latest = tech_df.iloc[-1]
    
    # RSI Score (reward being not overbought/oversold)
    rsi_score = 100 - (abs(latest['rsi'] - 50) * 2)

    # MACD Score
    macd_score = 100 if latest['macd'] > latest['macd_signal'] else 0
    
    # Trend Score
    trend_score = 100 if latest['sma_50'] > latest['sma_200'] else 0
    
    # Bollinger Band Score
    bb_score = 0
    if latest['close'] < latest['bb_lower']: bb_score = 100 # Potentially oversold
    elif latest['close'] > latest['bb_upper']: bb_score = 0 # Potentially overbought
    else: # Scale within the bands
        span = latest['bb_upper'] - latest['bb_lower']
        if span > 0:
            bb_score = (1 - (latest['close'] - latest['bb_lower']) / span) * 100

    total_score = (
        rsi_score * TECHNICAL_INDICATORS_WEIGHTS["rsi"] +
        macd_score * TECHNICAL_INDICATORS_WEIGHTS["macd"] +
        trend_score * TECHNICAL_INDICATORS_WEIGHTS["trend"] +
        bb_score * TECHNICAL_INDICATORS_WEIGHTS["bollinger"]
    )
    
    return total_score / sum(TECHNICAL_INDICATORS_WEIGHTS.values())

# 3. Main Scoring Orchestrator

def get_classification_label(score):
    if score >= 80: return "Strong Buy"
    if score >= 65: return "Buy"
    if score >= 45: return "Neutral"
    if score >= 25: return "Sell"
    return "Strong Sell"

def calculate_and_store_scores_for_ticker(db: Session, ticker_symbol_param: str):
    symbol = ticker_symbol_param # Explicitly assign to local variable 'symbol'
    # 1. Fetch data
    db_ticker = db.query(models.Ticker).filter(models.Ticker.symbol == symbol).one()
    print(f"DEBUG: Inside calculate_and_store_scores_for_ticker - db_ticker: {db_ticker.symbol}")
    ticker_id = db_ticker.id
    
    prices_query = db.query(models.DailyPrice).filter(models.DailyPrice.ticker_id == ticker_id).order_by(models.DailyPrice.date)
    prices_df = pd.read_sql(prices_query.statement, db.bind, index_col='date')
    
    fundamentals = db.query(models.Fundamental).filter(models.Fundamental.ticker_id == ticker_id).order_by(models.Fundamental.date.desc()).first()

    if prices_df.empty:
        print(f"No price data for {db_ticker.symbol}, skipping scoring.")
        return

    # 2. Calculate scores
    fundamental_score = calculate_fundamental_score(fundamentals)
    
    tech_df = indicators.calculate_technical_indicators(prices_df)
    technical_score = calculate_technical_score(tech_df)
    
    final_score = (fundamental_score * FUNDAMENTAL_WEIGHT) + (technical_score * TECHNICAL_WEIGHT)
    
    # 3. EMA Smoothing
    # Fetch historical scores to continue the EMA chain
    historical_scores = pd.read_sql(
        db.query(models.DailyScore.date, models.DailyScore.final_score)
          .filter(models.DailyScore.ticker_id == ticker_id)
          .order_by(models.DailyScore.date).statement,
        db.bind,
        index_col='date'
    )
    
    # Append today's score and recalculate EMA
    today_date = prices_df.index[-1]
    new_row = pd.DataFrame([{'final_score': final_score}], index=[today_date])
    all_scores = pd.concat([historical_scores[~historical_scores.index.isin(new_row.index)], new_row])
    
    smoothed_scores = all_scores['final_score'].ewm(span=5, adjust=False).mean()
    latest_smoothed_score = smoothed_scores.iloc[-1]

    # 4. Get label
    print(f"DEBUG: {db_ticker.symbol} - Smoothed Score: {latest_smoothed_score:.2f}")
    label = get_classification_label(latest_smoothed_score)
    
    # 5. Store in DB
    new_score = models.DailyScore(
        ticker_id=ticker_id,
        date=today_date,
        fundamental_score=fundamental_score,
        technical_score=technical_score,
        final_score=final_score,
        smoothed_score=latest_smoothed_score,
        label=label
    )
    db.merge(new_score) # Use merge to update score for the day if it exists
    db.commit()
    print(f"Calculated score for {db_ticker.symbol}: {latest_smoothed_score:.2f} ({label})")

def update_all_ticker_scores(db: Session):
    tickers = db.query(models.Ticker).all()
    for ticker in tickers:
        try:
            calculate_and_store_scores_for_ticker(db, ticker.symbol)
        except Exception as e:
            print(f"Error during scoring process: {e}")
