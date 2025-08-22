
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Database Models ---

class Ticker(Base):
    __tablename__ = "tickers"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    company_name = Column(String)
    
    prices = relationship("DailyPrice", back_populates="ticker", cascade="all, delete-orphan")
    fundamentals = relationship("Fundamental", back_populates="ticker", cascade="all, delete-orphan")
    scores = relationship("DailyScore", back_populates="ticker", cascade="all, delete-orphan")

class DailyPrice(Base):
    __tablename__ = "daily_prices"
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    
    ticker = relationship("Ticker", back_populates="prices")

class Fundamental(Base):
    __tablename__ = "fundamentals"
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    market_cap = Column(Float, nullable=True)
    pe_ratio = Column(Float, nullable=True)
    pb_ratio = Column(Float, nullable=True)
    debt_to_equity = Column(Float, nullable=True)
    roe = Column(Float, nullable=True)
    
    ticker = relationship("Ticker", back_populates="fundamentals")

class DailyScore(Base):
    __tablename__ = "daily_scores"
    id = Column(Integer, primary_key=True, index=True)
    ticker_id = Column(Integer, ForeignKey("tickers.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    fundamental_score = Column(Float)
    technical_score = Column(Float)
    final_score = Column(Float)
    smoothed_score = Column(Float)
    
    label = Column(String) # Strong Buy, Buy, Neutral, Sell, Strong Sell
    
    ticker = relationship("Ticker", back_populates="scores")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
