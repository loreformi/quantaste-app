
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from ..services import scoring
from ..models import SessionLocal

def update_job():
    """The job that will be run on a schedule."""
    print("Scheduler running: Updating all ticker scores...")
    db: Session = SessionLocal()
    try:
        scoring.update_all_ticker_scores(db)
        print("Scheduler job finished.")
    finally:
        db.close()

scheduler = BackgroundScheduler(daemon=True)
# Schedule to run once every day at a specific time (e.g., 01:00 UTC)
scheduler.add_job(update_job, 'cron', hour=1, minute=0)
