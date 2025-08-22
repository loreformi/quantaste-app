import yfinance as yf
from sqlalchemy.orm import Session
from .. import models

def clean_invalid_tickers(db: Session):
    print("Starting invalid ticker cleanup...")
    tickers_to_check = db.query(models.Ticker).all()
    deleted_count = 0
    
    for ticker_db in tickers_to_check:
        symbol = ticker_db.symbol
        try:
            ticker_yf = yf.Ticker(symbol)
            info = ticker_yf.info
            hist = ticker_yf.history(period="1d")

            if not info or not info.get('longName') or hist.empty:
                print(f"Invalid ticker detected: {symbol}. Deleting all associated data.")
                db.delete(ticker_db)
                deleted_count += 1
            else:
                print(f"Ticker {symbol} is valid. Keeping.")
        except Exception as e:
            print(f"Error validating ticker {symbol}: {e}. Assuming invalid and deleting.")
            db.delete(ticker_db)
            deleted_count += 1
            
    db.commit()
    print(f"Invalid ticker cleanup finished. Deleted {deleted_count} tickers.")
    return {"message": f"Cleaned up {deleted_count} invalid tickers."}
