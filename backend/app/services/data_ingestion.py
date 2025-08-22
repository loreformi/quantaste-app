
import yfinance as yf
from sqlalchemy.orm import Session
from .. import models, schemas
from datetime import datetime

def ingest_data_for_ticker(db: Session, symbol: str):
    """
    Ingests historical price and fundamental data for a given ticker symbol.
    """
    try:
        ticker_obj = yf.Ticker(symbol)
        
        # 1. Get or Create Ticker
        db_ticker = db.query(models.Ticker).filter(models.Ticker.symbol == symbol).first()
        if not db_ticker:
            company_name = ticker_obj.info.get('longName', symbol)
            db_ticker = models.Ticker(symbol=symbol, company_name=company_name)
            db.add(db_ticker)
            db.commit()
            db.refresh(db_ticker)

        # 2. Ingest Historical Prices
        hist_prices = ticker_obj.history(period="5y", auto_adjust=True) # 5 years of data
        if hist_prices.empty:
            print(f"Could not fetch price history for {symbol}")
            return

        for index, row in hist_prices.iterrows():
            db_price = models.DailyPrice(
                ticker_id=db_ticker.id,
                date=index.date(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=row['Volume']
            )
            db.merge(db_price) # Use merge to avoid duplicates on reruns

        # 3. Ingest Fundamental Data
        info = ticker_obj.info
        db_fundamental = models.Fundamental(
            ticker_id=db_ticker.id,
            date=datetime.now().date(),
            market_cap=info.get('marketCap'),
            pe_ratio=info.get('trailingPE'),
            pb_ratio=info.get('priceToBook'),
            debt_to_equity=info.get('debtToEquity'),
            roe=info.get('returnOnEquity')
        )
        db.merge(db_fundamental) # Use merge to update fundamentals daily

        db.commit()
        print(f"Successfully ingested data for {symbol}")

    except Exception as e:
        db.rollback()
        print(f"Failed to ingest data for {symbol}: {e}")

def add_new_ticker(db: Session, symbol: str):
    """Adds a new ticker and ingests its initial data."""
    db_ticker = db.query(models.Ticker).filter(models.Ticker.symbol == symbol.upper()).first()
    if db_ticker:
        return {"message": "Ticker already exists"}
    
    ingest_data_for_ticker(db, symbol.upper())
    return {"message": f"Ticker {symbol.upper()} added and data ingestion started."}
