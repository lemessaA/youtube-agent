from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class VideoStatus(str, Enum):
    IDEA = "idea"
    SCRIPT = "script"
    THUMBNAIL = "thumbnail"
    VIDEO = "video"
    UPLOADED = "uploaded"
    PUBLISHED = "published"

class NicheType(str, Enum):
    AI_TOOLS = "ai_tools"
    STARTUP_IDEAS = "startup_ideas"
    TECH_EXPLAINED = "tech_explained"
    MAKE_MONEY = "make_money"
    SIDE_HUSTLES = "side_hustles"

class VideoIdea(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    niche: NicheType
    viral_score: int = Field(ge=1, le=100)
    target_audience: str
    why_trending: str
    search_demand: str
    competition_level: str
    created_at: Optional[datetime] = None
    status: VideoStatus = VideoStatus.IDEA

class Script(BaseModel):
    id: Optional[str] = None
    video_id: str
    title: str
    hook: str
    intro: str
    main_points: List[str]
    conclusion: str
    call_to_action: str
    scenes: List[Dict[str, Any]]
    voice_tone: str
    estimated_duration: int
    created_at: Optional[datetime] = None

class Thumbnail(BaseModel):
    id: Optional[str] = None
    video_id: str
    thumbnail_text: str
    background_idea: str
    colors: List[str]
    visual_concept: str
    thumbnail_variations: List[str]
    created_at: Optional[datetime] = None

class Video(BaseModel):
    id: Optional[str] = None
    channel_id: str
    video_idea_id: str
    script_id: str
    thumbnail_id: str
    title: str
    description: str
    tags: List[str]
    duration: int
    file_path: Optional[str] = None
    youtube_video_id: Optional[str] = None
    status: VideoStatus = VideoStatus.IDEA
    views: int = 0
    likes: int = 0
    comments: int = 0
    watch_time: int = 0
    ctr: float = 0.0
    created_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

class Channel(BaseModel):
    id: Optional[str] = None
    name: str
    niche: NicheType
    youtube_channel_id: Optional[str] = None
    description: str
    target_audience: str
    upload_frequency: str = "daily"
    video_length_range: str = "60-120"
    style: str = "faceless"
    monetization_enabled: bool = False
    created_at: Optional[datetime] = None

class Analytics(BaseModel):
    id: Optional[str] = None
    video_id: str
    date: datetime
    views: int
    likes: int
    comments: int
    shares: int
    watch_time: int
    ctr: float
    audience_retention: float
    revenue: float = 0.0

class TrendingTopic(BaseModel):
    id: Optional[str] = None
    topic: str
    niche: NicheType
    search_volume: int
    competition_score: int
    trending_score: int
    keywords: List[str]
    related_topics: List[str]
    created_at: Optional[datetime] = None

class MonetizationStrategy(BaseModel):
    id: Optional[str] = None
    channel_id: str
    strategy_type: str
    affiliate_links: List[str] = []
    sponsorship_opportunities: List[str] = []
    digital_products: List[str] = []
    courses: List[str] = []
    revenue_streams: List[str] = []
    created_at: Optional[datetime] = None
