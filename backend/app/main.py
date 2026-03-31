import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime

from agents import DailyAutomationAgent, TrendResearchAgent, AnalyticsAgent, MonetizationAgent
from models import Channel, Video, VideoIdea, NicheType
from config import db
from utils.scheduler import scheduler
from utils.middleware import LoggingMiddleware, RateLimitMiddleware, SecurityMiddleware, CORSMiddleware as CustomCORSMiddleware
from utils.exceptions import YouTubeAutomationException, create_internal_server_exception

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI YouTube Automation API",
    description="Complete AI-powered YouTube automation system",
    version="1.0.0"
)

# CORS middleware (custom class: only allow_origins/methods/headers)
app.add_middleware(
    CustomCORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware, calls=100, period=60)
app.add_middleware(SecurityMiddleware)

# Initialize agents
automation_agent = DailyAutomationAgent()
trend_agent = TrendResearchAgent()
analytics_agent = AnalyticsAgent()
monetization_agent = MonetizationAgent()

# Pydantic models for requests/responses
class ChannelCreate(BaseModel):
    name: str
    niche: NicheType
    description: str
    target_audience: str
    upload_frequency: str = "daily"
    video_length_range: str = "60-120"
    style: str = "faceless"

class ChannelResponse(BaseModel):
    id: str
    name: str
    niche: str
    description: str
    target_audience: str
    upload_frequency: str
    video_length_range: str
    style: str
    created_at: datetime

class VideoGenerationRequest(BaseModel):
    channel_id: str
    topic: Optional[str] = None
    force_new_topic: bool = False

class VideoResponse(BaseModel):
    id: str
    channel_id: str
    title: str
    description: str
    tags: List[str]
    duration: int
    status: str
    created_at: datetime

class AnalyticsRequest(BaseModel):
    video_id: str

class MonetizationRequest(BaseModel):
    channel_id: str

class TrendResearchRequest(BaseModel):
    niche: NicheType
    limit: int = 10

# Health check endpoint
@app.get("/")
async def root():
    return {
        "message": "AI YouTube Automation API",
        "status": "running",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Channel management endpoints
@app.post("/channels", response_model=ChannelResponse)
async def create_channel(channel_data: ChannelCreate):
    try:
        channel_data_dict = channel_data.dict()
        channel_data_dict["niche"] = channel_data.niche.value
        
        result = db.insert_channel(channel_data_dict)
        
        if not result:
            raise HTTPException(status_code=500, detail="Failed to create channel")
        
        return ChannelResponse(**result)
        
    except Exception as e:
        logger.error(f"Error creating channel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/channels", response_model=List[ChannelResponse])
async def get_channels():
    try:
        channels = db.get_channels()
        return [ChannelResponse(**channel) for channel in channels]
        
    except Exception as e:
        logger.error(f"Error getting channels: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/channels/{channel_id}", response_model=ChannelResponse)
async def get_channel(channel_id: str):
    try:
        channels = db.get_channels()
        channel = next((c for c in channels if c.get('id') == channel_id), None)
        
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        return ChannelResponse(**channel)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting channel: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Video generation endpoints
@app.post("/videos/generate")
async def generate_video(request: VideoGenerationRequest, background_tasks: BackgroundTasks):
    try:
        # Start video generation in background
        background_tasks.add_task(
            automation_agent.run_daily_automation, 
            request.channel_id
        )
        
        return {
            "message": "Video generation started",
            "channel_id": request.channel_id,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Error starting video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/videos/generate-sync")
async def generate_video_sync(request: VideoGenerationRequest):
    try:
        result = await automation_agent.run_daily_automation(request.channel_id)
        
        if result.get("error"):
            raise HTTPException(status_code=500, detail=result["error"])
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos", response_model=List[VideoResponse])
async def get_videos(channel_id: Optional[str] = None, limit: int = 10):
    try:
        videos = db.get_videos(channel_id, limit)
        return [VideoResponse(**video) for video in videos]
        
    except Exception as e:
        logger.error(f"Error getting videos: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/videos/{video_id}", response_model=VideoResponse)
async def get_video(video_id: str):
    try:
        videos = db.get_videos()
        video = next((v for v in videos if v.get('id') == video_id), None)
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        return VideoResponse(**video)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting video: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Trend research endpoints
@app.post("/trends/research")
async def research_trends(request: TrendResearchRequest):
    try:
        video_ideas = await trend_agent.research_trends(request.niche)
        
        return {
            "niche": request.niche.value,
            "ideas": [
                {
                    "title": idea.title,
                    "description": idea.description,
                    "viral_score": idea.viral_score,
                    "target_audience": idea.target_audience,
                    "why_trending": idea.why_trending,
                    "search_demand": idea.search_demand,
                    "competition_level": idea.competition_level
                }
                for idea in video_ideas
            ]
        }
        
    except Exception as e:
        logger.error(f"Error researching trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trends/keywords/{niche}")
async def get_trending_keywords(niche: str):
    try:
        keywords = trend_agent.get_trending_keywords(niche)
        return {"niche": niche, "keywords": keywords}
        
    except Exception as e:
        logger.error(f"Error getting trending keywords: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Analytics endpoints
@app.post("/analytics/video")
async def analyze_video_performance(request: AnalyticsRequest):
    try:
        # Get video data
        videos = db.get_videos()
        video = next((v for v in videos if v.get('id') == request.video_id), None)
        
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        
        analytics = await analytics_agent.analyze_video_performance(video)
        return analytics
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing video performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics/channel/{channel_id}")
async def get_channel_analytics(channel_id: str):
    try:
        videos = db.get_videos(channel_id)
        
        if not videos:
            return {"message": "No videos found for this channel"}
        
        analytics_report = analytics_agent.generate_performance_report(videos)
        return analytics_report
        
    except Exception as e:
        logger.error(f"Error getting channel analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Monetization endpoints
@app.post("/monetization/analyze")
async def analyze_monetization(request: MonetizationRequest):
    try:
        # Get channel data
        channels = db.get_channels()
        channel = next((c for c in channels if c.get('id') == request.channel_id), None)
        
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Get channel stats (simplified)
        videos = db.get_videos(request.channel_id)
        channel_stats = {
            "name": channel.get('name'),
            "niche": channel.get('niche'),
            "subscribers": len(videos) * 100,  # Estimate
            "avg_views": sum(v.get('views', 0) for v in videos) / len(videos) if videos else 0,
            "engagement_rate": 5.0  # Estimate
        }
        
        monetization_analysis = await monetization_agent.analyze_monetization_potential(channel_stats)
        return monetization_analysis
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing monetization: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Automation status endpoint
@app.get("/automation/status")
async def get_automation_status():
    try:
        status = await automation_agent.get_automation_status()
        return status
        
    except Exception as e:
        logger.error(f"Error getting automation status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Daily automation trigger endpoint
@app.post("/automation/run-daily")
async def run_daily_automation(background_tasks: BackgroundTasks):
    try:
        # Get all channels
        channels = db.get_channels()
        
        if not channels:
            return {"message": "No channels found"}
        
        # Run automation for each channel
        for channel in channels:
            background_tasks.add_task(
                automation_agent.run_daily_automation,
                channel.get('id')
            )
        
        return {
            "message": f"Daily automation started for {len(channels)} channels",
            "channels": len(channels)
        }
        
    except Exception as e:
        logger.error(f"Error running daily automation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Video ideas endpoint
@app.get("/ideas", response_model=List[Dict[str, Any]])
async def get_video_ideas(limit: int = 10):
    try:
        ideas = db.get_video_ideas(limit)
        return ideas
        
    except Exception as e:
        logger.error(f"Error getting video ideas: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Utility endpoint to test API
@app.post("/test/generation")
async def test_video_generation():
    try:
        # Create a test channel if none exists
        channels = db.get_channels()
        
        if not channels:
            test_channel = {
                "name": "Test AI Tools Channel",
                "niche": "ai_tools",
                "description": "Test channel for AI automation",
                "target_audience": "Developers and tech enthusiasts",
                "upload_frequency": "daily",
                "video_length_range": "60-120",
                "style": "faceless"
            }
            
            channel_result = db.insert_channel(test_channel)
            channel_id = channel_result["id"] if channel_result else None
        else:
            channel_id = channels[0]["id"]
        
        if not channel_id:
            raise HTTPException(status_code=500, detail="Failed to create or get test channel")
        
        # Run video generation
        result = await automation_agent.run_daily_automation(channel_id)
        
        return result
        
    except Exception as e:
        logger.error(f"Error in test video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from app.scheduler import router as scheduler_router

# Include routers
app.include_router(scheduler_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize scheduler on startup"""
    try:
        scheduler.start()
        logger.info("Scheduler started on application startup")
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    try:
        scheduler.stop()
        logger.info("Scheduler stopped on application shutdown")
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
