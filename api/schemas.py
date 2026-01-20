from pydantic import BaseModel
from typing import List, Optional

class TopProduct(BaseModel):
    product: str
    mentions: int

class ChannelActivity(BaseModel):
    date: str
    post_count: int

class Message(BaseModel):
    message_id: int
    message_text: str
    views: int

class VisualStats(BaseModel):
    channel_name: str
    image_count: int
    avg_views: float