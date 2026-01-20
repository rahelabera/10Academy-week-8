from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
import schemas
from database import get_db

app = FastAPI(title="Medical Telegram API")

@app.get("/api/reports/top-products", response_model=List[schemas.TopProduct])
def get_top_products(limit: int = 10, db: Session = Depends(get_db)):
    query = text("""
        SELECT unnest(regexp_matches(message_text, '[A-Za-z0-9]+')) AS product, COUNT(*) AS mentions
        FROM marts.fct_messages
        GROUP BY product
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    result = db.execute(query, {"limit": limit}).fetchall()
    return [{"product": row[0], "mentions": row[1]} for row in result]

@app.get("/api/channels/{channel_name}/activity", response_model=List[schemas.ChannelActivity])
def get_channel_activity(channel_name: str, db: Session = Depends(get_db)):
    query = text("""
        SELECT d.full_date, COUNT(m.message_id) AS post_count
        FROM marts.fct_messages m
        JOIN marts.dim_channels c ON m.channel_key = c.channel_key
        JOIN marts.dim_dates d ON m.date_key = d.date_key
        WHERE c.channel_name = :channel_name
        GROUP BY d.full_date
        ORDER BY d.full_date
    """)
    result = db.execute(query, {"channel_name": channel_name}).fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return [{"date": row[0], "post_count": row[1]} for row in result]

@app.get("/api/search/messages", response_model=List[schemas.Message])
def search_messages(query: str, limit: int = 20, db: Session = Depends(get_db)):
    query = text("""
        SELECT message_id, message_text, view_count
        FROM marts.fct_messages
        WHERE message_text ILIKE :query
        LIMIT :limit
    """)
    result = db.execute(query, {"query": f"%{query}%", "limit": limit}).fetchall()
    return [{"message_id": row[0], "message_text": row[1], "views": row[2]} for row in result]

@app.get("/api/reports/visual-content", response_model=List[schemas.VisualStats])
def get_visual_stats(db: Session = Depends(get_db)):
    query = text("""
        SELECT c.channel_name, COUNT(id.message_id) AS image_count, AVG(m.view_count) AS avg_views
        FROM marts.fct_image_detections id
        JOIN marts.fct_messages m ON id.message_id = m.message_id
        JOIN marts.dim_channels c ON m.channel_key = c.channel_key
        GROUP BY c.channel_name
    """)
    result = db.execute(query).fetchall()
    return [{"channel_name": row[0], "image_count": row[1], "avg_views": row[2]} for row in result]