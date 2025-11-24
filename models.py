from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SocialPlatform(str, Enum):
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    INSTAGRAM = "instagram"

class Post(BaseModel):
    platform: SocialPlatform
    content: str = Field(..., description="The text content of the post")
    image_path: Optional[str] = Field(None, description="Path to the image asset if any")
    scheduled_time: Optional[datetime] = Field(None, description="When this post should go live")
    hashtags: List[str] = Field(default_factory=list)

class Campaign(BaseModel):
    title: str
    goal: str = Field(..., description="The main goal of this campaign (e.g. 'Raise awareness for water safety')")
    posts: List[Post]
    created_at: datetime = Field(default_factory=datetime.now)
    status: str = "draft"
