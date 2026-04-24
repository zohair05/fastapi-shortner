from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, utils
from .database import engine, get_db

# Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bitly Clone API")

@app.post("/api/shorten", response_model=schemas.URLResponse)
def create_short_url(url: schemas.URLCreate, db: Session = Depends(get_db)):
    # 1. Create DB entry to get the Auto-Incrementing ID
    db_url = models.URL(long_url=str(url.long_url))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)

    # 2. Convert ID to Base62 short code
    short_code = utils.encode_id(db_url.id)
    db_url.short_code = short_code
    db.commit()
    db.refresh(db_url)

    return db_url

@app.get("/{short_code}")
def redirect_to_url(short_code: str, request: Request, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    # Log the click for analytics
    click = models.Click(
        url_id=db_url.id,
        ip_address=request.client.host if request.client else "Unknown",
        user_agent=request.headers.get("user-agent", "Unknown")
    )
    db.add(click)
    db.commit()

    return RedirectResponse(url=db_url.long_url, status_code=301)

@app.get("/api/analytics/{short_code}", response_model=schemas.AnalyticsResponse)
def get_analytics(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(models.URL).filter(models.URL.short_code == short_code).first()
    
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")

    clicks = db.query(models.Click).filter(models.Click.url_id == db_url.id).all()

    return schemas.AnalyticsResponse(
        long_url=db_url.long_url,
        total_clicks=len(clicks),
        clicks=[schemas.ClickData(
            timestamp=c.timestamp, 
            ip_address=c.ip_address, 
            user_agent=c.user_agent
        ) for c in clicks]
    )