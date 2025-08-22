
import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from . import models
from .models import engine, get_db
from .routers import scores, admin
from .jobs.scheduler import scheduler, update_job
from .services import data_ingestion, scoring

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Crea le tabelle nel database se non esistono
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Quantaste Smart Score API",
    description="API per calcolare e fornire Smart Scores per titoli azionari.",
    version="1.0.0",
)

# Configurazione CORS per permettere al frontend di comunicare con il backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # L'origine del tuo frontend Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusione dei router
app.include_router(scores.router)
app.include_router(admin.router)

@app.on_event("startup")
def startup_event():
    print("Application startup...")
    db: Session = next(get_db())
    try:
        # 1. Controlla se ci sono ticker nel DB
        tickers_exist = db.query(models.Ticker).first()
        if not tickers_exist:
            print("Database is empty. Performing initial data ingestion...")
            default_tickers = os.getenv("DEFAULT_TICKERS", "AAPL,MSFT").split(',')
            for symbol in default_tickers:
                data_ingestion.ingest_data_for_ticker(db, symbol)
            
            print("Initial data ingestion complete. Calculating initial scores...")
            scoring.update_all_ticker_scores(db)
            print("Initial scoring complete.")

        # 2. Avvia lo scheduler per gli aggiornamenti periodici
        print("Starting background scheduler...")
        scheduler.start()
        print("Scheduler started.")

    finally:
        db.close()

@app.on_event("shutdown")
def shutdown_event():
    print("Shutting down scheduler...")
    scheduler.shutdown()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Quantaste API. Visit /docs for documentation."}

