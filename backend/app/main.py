import sys
import os
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import os

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

# Mount static files for videos and thumbnails
videos_dir = os.path.join(os.path.dirname(__file__), "..", "videos")
thumbnails_dir = os.path.join(os.path.dirname(__file__), "..", "thumbnails")
os.makedirs(videos_dir, exist_ok=True)
os.makedirs(thumbnails_dir, exist_ok=True)

app.mount("/videos", StaticFiles(directory=videos_dir), name="videos")
app.mount("/thumbnails", StaticFiles(directory=thumbnails_dir), name="thumbnails")

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
    script: Optional[str] = ""
    status: str
    tags: Optional[List[str]] = []
    duration: Optional[int] = 0
    views: Optional[int] = 0
    likes: Optional[int] = 0
    comments: Optional[int] = 0
    revenue: Optional[float] = 0.0
    created_at: datetime
    updated_at: Optional[datetime] = None

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
        
        result = db.create_channel(channel_data_dict)
        
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
        # Get channel info
        channel = db.get_channel(request.channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Create video record immediately with "generating" status
        video_data = {
            "channel_id": request.channel_id,
            "title": f"AI Generated Video for {channel['name']}",
            "description": "Video being generated by AI automation system...",
            "script": "",
            "status": "generating",
            "views": 0,
            "likes": 0,
            "comments": 0,
            "revenue": 0.0,
            "duration": 0,
            "tags": []
        }
        
        video_record = db.create_video(video_data)
        
        # Start video generation in background
        background_tasks.add_task(
            _generate_video_content, 
            video_record["id"], 
            request.channel_id
        )
        
        return {
            "message": "Video generation started",
            "video_id": video_record["id"],
            "channel_id": request.channel_id,
            "status": "generating"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def _generate_video_content(video_id: str, channel_id: str):
    """Background task to generate actual video content"""
    try:
        import asyncio
        from random import choice, randint
        
        # Simulate video generation process (2-5 seconds)
        await asyncio.sleep(randint(2, 5))
        
        # Get channel for context
        channel = db.get_channel(channel_id)
        niche = channel.get('niche', 'ai_tools')
        
        # Generate realistic content based on niche
        title_templates = {
            'ai_tools': [
                "5 AI Tools That Will Blow Your Mind in 2024",
                "ChatGPT vs Claude: The Ultimate AI Showdown", 
                "Free AI Tool Better Than Paid Alternatives?",
                "How I Built a $10K/Month Business with AI"
            ],
            'startup_ideas': [
                "3 Startup Ideas No One Is Talking About",
                "$100K Business You Can Start This Weekend",
                "Why 99% of Startups Fail (And How to Win)",
                "I Found the Next Billion Dollar Opportunity"
            ],
            'tech_explained': [
                "Why Everyone Gets This Technology Wrong",
                "The Future of Tech in 60 Seconds", 
                "How This Changes Everything Forever",
                "Technology That Will Replace Your Job"
            ],
            'make_money': [
                "How I Made $5K Online This Month",
                "Secret Strategy No One Shares",
                "From $0 to $10K in 30 Days",
                "The Method That Actually Works"
            ],
            'side_hustles': [
                "Side Hustle That Made Me $2K This Week",
                "5 Apps That Pay You Real Money",
                "Weekend Business That Changed My Life",
                "Work 2 Hours, Earn $500/Day"
            ]
        }
        
        # Generate content
        titles = title_templates.get(niche, title_templates['ai_tools'])
        generated_title = choice(titles)
        
        # Create engaging script
        script_templates = {
            'ai_tools': f"Did you know there's an AI tool that can {choice(['automate your entire workflow', 'write better code than humans', 'design like a pro', 'analyze data instantly'])}? I've been testing this for weeks and the results are incredible...",
            'startup_ideas': f"I just discovered a business opportunity that {choice(['makes $10K monthly', 'requires zero investment', 'anyone can start today', 'scales automatically'])}. Here's exactly how it works...",
            'tech_explained': f"Everyone thinks {choice(['AI', 'blockchain', 'quantum computing', 'neural networks'])} is complicated, but it's actually simple. Let me show you...",
            'make_money': f"I found a way to make {choice(['$100/day', '$50/hour', '$1K/week', '$5K/month'])} online and it's not what you think...",
            'side_hustles': f"This side hustle is making people {choice(['$500 extra per month', '$2K on weekends', '$100 per day', '$1K in their spare time'])}. Here's the step by step..."
        }
        
        script = script_templates.get(niche, script_templates['ai_tools'])
        
        # Generate tags based on niche
        tag_templates = {
            'ai_tools': ['AI', 'technology', 'productivity', 'automation', 'tools'],
            'startup_ideas': ['business', 'entrepreneur', 'startup', 'ideas', 'money'],
            'tech_explained': ['technology', 'explained', 'tutorial', 'learning', 'science'],
            'make_money': ['money', 'income', 'online', 'business', 'financial'],
            'side_hustles': ['side hustle', 'extra income', 'part time', 'money', 'business']
        }
        
        tags = tag_templates.get(niche, ['video', 'content', 'tutorial'])
        
        # Create real video file
        video_filename = f"{video_id}_video.mp4"
        video_path = f"/home/lemessa-ahmed/youtube-agent/backend/videos/{video_filename}"
        
        # Create a video plan for generation
        video_plan = {
            "scenes": [
                {
                    "scene_number": 1,
                    "duration": 8,
                    "visual_type": "title_screen",
                    "visual_description": "Eye-catching title screen",
                    "voiceover": f"Welcome to {generated_title}",
                    "on_screen_text": generated_title,
                    "background_music": "Upbeat intro"
                },
                {
                    "scene_number": 2, 
                    "duration": 45,
                    "visual_type": "main_content",
                    "visual_description": "Main content with key points",
                    "voiceover": script,
                    "on_screen_text": "Key insights inside...",
                    "background_music": "Ambient"
                },
                {
                    "scene_number": 3,
                    "duration": 7,
                    "visual_type": "call_to_action",
                    "visual_description": "Subscribe call to action",
                    "voiceover": "Subscribe for more content like this!",
                    "on_screen_text": "SUBSCRIBE FOR MORE!",
                    "background_music": "Outro"
                }
            ],
            "color_scheme": ["#1d4ed8", "#000000", "#ffffff"],
            "font_style": "Arial Bold"
        }
        
        # Import video generation agent and create real video
        from agents.video_generation_agent import VideoGenerationAgent
        video_agent = VideoGenerationAgent()
        
        try:
            # Create the actual video file
            await video_agent.create_video_file(video_plan, video_path)
            logger.info(f"✅ Real video file created: {video_path}")
            
            # Verify file was created and has content
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path)
                logger.info(f"📁 Video file size: {file_size / (1024*1024):.3f} MB")
                
                # Only consider it successful if file has reasonable size
                if file_size > 1000:  # At least 1KB
                    video_url_path = f"/videos/{video_filename}"
                else:
                    logger.warning(f"Video file too small ({file_size} bytes), treating as failed")
                    video_path = None
                    video_url_path = None
            else:
                video_path = None
                video_url_path = None
            
        except Exception as video_error:
            logger.warning(f"Video file creation failed: {video_error}")
            video_path = None
            video_url_path = None
        
        # Update video with generated content
        updated_video_data = {
            "title": generated_title,
            "description": f"Discover {generated_title.lower()}. This video breaks down everything you need to know in under 2 minutes. Perfect for {channel.get('target_audience', 'everyone')}.",
            "script": script,
            "status": "ready" if video_path else "ready_no_file",
            "views": randint(100, 5000),  # Simulate some initial views
            "likes": randint(10, 200),
            "comments": randint(5, 50),
            "revenue": round(randint(1, 100) + randint(0, 99)/100, 2),  # Random revenue $1-100
            "duration": 60,  # Total duration from plan
            "tags": tags[:3],  # First 3 tags
            "thumbnail_url": f"/thumbnails/{video_id}_thumbnail.jpg",
            "video_url": video_url_path if video_path else None
        }
        
        db.update_video(video_id, updated_video_data)
        logger.info(f"✅ Generated video: {generated_title}")
        
    except Exception as e:
        logger.error(f"❌ Background video generation failed: {e}")
        # Mark video as failed
        try:
            db.update_video(video_id, {"status": "failed"})
        except:
            pass

@app.post("/videos/generate/sync")
async def generate_video_sync(request: VideoGenerationRequest):
    try:
        # Get channel info
        channel = db.get_channel(request.channel_id)
        if not channel:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        # Create and generate video synchronously
        video_data = {
            "channel_id": request.channel_id,
            "title": "Generating...",
            "description": "Video being generated...",
            "script": "",
            "status": "generating"
        }
        
        video_record = db.create_video(video_data)
        
        # Generate content immediately
        await _generate_video_content(video_record["id"], request.channel_id)
        
        # Return updated video
        updated_video = db.get_video(video_record["id"])
        return updated_video
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in synchronous video generation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/video")
async def simple_generate_video(request: Dict[str, str]):
    """Simplified video generation endpoint for frontend"""
    try:
        channel_id = request.get("channel_id")
        if not channel_id:
            raise HTTPException(status_code=400, detail="channel_id required")
        
        # Create VideoGenerationRequest
        generation_request = VideoGenerationRequest(channel_id=channel_id)
        
        # Use the sync generation for immediate results
        result = await generate_video_sync(generation_request)
        
        return {
            "success": True,
            "message": "Video generated successfully",
            "video": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in simple video generation: {e}")
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

@app.get("/analytics")
async def get_analytics(channel_id: Optional[str] = None):
    """Get general analytics or analytics for specific channel"""
    try:
        # Get all videos or videos for specific channel
        videos = db.get_videos(channel_id) if channel_id else db.get_videos()
        channels = db.get_channels()
        
        # Calculate basic analytics
        total_videos = len(videos)
        total_views = sum(video.get('views', 0) for video in videos)
        total_revenue = sum(video.get('revenue', 0) for video in videos)
        
        # Mock some additional metrics
        avg_ctr = 3.2  # Mock click-through rate
        avg_retention = 67.8  # Mock retention rate
        
        # Find top performing video
        top_video = max(videos, key=lambda x: x.get('views', 0)) if videos else None
        
        # Mock recent performance data
        recent_performance = [
            {"date": "2024-01-01", "views": 1200, "revenue": 24.50},
            {"date": "2024-01-02", "views": 1850, "revenue": 37.20},
            {"date": "2024-01-03", "views": 2100, "revenue": 42.80},
            {"date": "2024-01-04", "views": 1650, "revenue": 31.90},
            {"date": "2024-01-05", "views": 2800, "revenue": 58.40},
        ]
        
        return {
            "total_videos": total_videos,
            "total_views": total_views,
            "total_revenue": total_revenue,
            "avg_ctr": avg_ctr,
            "avg_retention": avg_retention,
            "top_performing_video": top_video,
            "recent_performance": recent_performance
        }
        
    except Exception as e:
        logger.error(f"Error getting analytics: {e}")
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
            
            channel_result = db.create_channel(test_channel)
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
