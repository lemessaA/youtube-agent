import asyncio
import logging
from datetime import datetime, time
from typing import List, Dict, Any
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from agents import DailyAutomationAgent
from config import db

logger = logging.getLogger(__name__)

class YouTubeScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.automation_agent = DailyAutomationAgent()
        self.is_running = False
        
    def start(self):
        """Start the scheduler"""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("YouTube scheduler started")
            
            # Schedule daily automation for all channels
            self.schedule_daily_automation()
            
            # Schedule trend research (every 6 hours)
            self.schedule_trend_research()
            
            # Schedule analytics update (every hour)
            self.schedule_analytics_update()
    
    def stop(self):
        """Stop the scheduler"""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("YouTube scheduler stopped")
    
    def schedule_daily_automation(self):
        """Schedule daily video generation for all channels"""
        try:
            # Run daily at 9:00 AM
            self.scheduler.add_job(
                func=self._run_daily_automation,
                trigger=CronTrigger(hour=9, minute=0),
                id="daily_automation",
                name="Daily Video Generation",
                replace_existing=True
            )
            logger.info("Scheduled daily automation for 9:00 AM")
            
        except Exception as e:
            logger.error(f"Error scheduling daily automation: {e}")
    
    def schedule_trend_research(self):
        """Schedule trend research every 6 hours"""
        try:
            self.scheduler.add_job(
                func=self._run_trend_research,
                trigger=CronTrigger(hour="*/6"),
                id="trend_research",
                name="Trend Research",
                replace_existing=True
            )
            logger.info("Scheduled trend research every 6 hours")
            
        except Exception as e:
            logger.error(f"Error scheduling trend research: {e}")
    
    def schedule_analytics_update(self):
        """Schedule analytics update every hour"""
        try:
            self.scheduler.add_job(
                func=self._run_analytics_update,
                trigger=CronTrigger(minute=0),
                id="analytics_update",
                name="Analytics Update",
                replace_existing=True
            )
            logger.info("Scheduled analytics update every hour")
            
        except Exception as e:
            logger.error(f"Error scheduling analytics update: {e}")
    
    async def _run_daily_automation(self):
        """Run daily automation for all channels"""
        try:
            logger.info("Starting daily automation for all channels")
            
            # Get all channels
            channels = db.get_channels()
            
            if not channels:
                logger.warning("No channels found for daily automation")
                return
            
            # Run automation for each channel
            for channel in channels:
                try:
                    channel_id = channel.get('id')
                    channel_name = channel.get('name', 'Unknown')
                    
                    logger.info(f"Running daily automation for channel: {channel_name}")
                    
                    result = await self.automation_agent.run_daily_automation(channel_id)
                    
                    if result.get("error"):
                        logger.error(f"Daily automation failed for {channel_name}: {result['error']}")
                    else:
                        logger.info(f"Daily automation completed for {channel_name}")
                        
                except Exception as e:
                    logger.error(f"Error running automation for channel {channel.get('name')}: {e}")
            
            logger.info("Daily automation completed for all channels")
            
        except Exception as e:
            logger.error(f"Error in daily automation: {e}")
    
    async def _run_trend_research(self):
        """Run trend research for all niches"""
        try:
            logger.info("Starting trend research")
            
            from models import NicheType
            from agents import TrendResearchAgent
            
            trend_agent = TrendResearchAgent()
            
            # Research trends for each niche
            for niche in NicheType:
                try:
                    logger.info(f"Researching trends for niche: {niche.value}")
                    
                    video_ideas = await trend_agent.research_trends(niche)
                    
                    # Store ideas in database
                    for idea in video_ideas:
                        idea_data = {
                            "title": idea.title,
                            "description": idea.description,
                            "niche": idea.niche.value,
                            "viral_score": idea.viral_score,
                            "target_audience": idea.target_audience,
                            "why_trending": idea.why_trending,
                            "search_demand": idea.search_demand,
                            "competition_level": idea.competition_level,
                            "status": "idea"
                        }
                        db.insert_video_idea(idea_data)
                    
                    logger.info(f"Researched {len(video_ideas)} ideas for {niche.value}")
                    
                except Exception as e:
                    logger.error(f"Error researching trends for {niche.value}: {e}")
            
            logger.info("Trend research completed")
            
        except Exception as e:
            logger.error(f"Error in trend research: {e}")
    
    async def _run_analytics_update(self):
        """Update analytics for all videos"""
        try:
            logger.info("Starting analytics update")
            
            from agents import AnalyticsAgent
            
            analytics_agent = AnalyticsAgent()
            
            # Get all videos
            videos = db.get_videos()
            
            for video in videos:
                try:
                    video_id = video.get('id')
                    video_title = video.get('title', 'Unknown')
                    
                    # Skip if video doesn't have views yet
                    if video.get('views', 0) == 0:
                        continue
                    
                    logger.debug(f"Updating analytics for video: {video_title}")
                    
                    # Analyze video performance
                    analytics = await analytics_agent.analyze_video_performance(video)
                    
                    # Update video with analytics data
                    if analytics:
                        analytics_data = {
                            "views": video.get('views', 0),
                            "likes": video.get('likes', 0),
                            "comments": video.get('comments', 0),
                            "watch_time": video.get('watch_time', 0),
                            "ctr": video.get('ctr', 0.0)
                        }
                        
                        db.update_video_analytics(video_id, analytics_data)
                    
                except Exception as e:
                    logger.error(f"Error updating analytics for video {video.get('title')}: {e}")
            
            logger.info("Analytics update completed")
            
        except Exception as e:
            logger.error(f"Error in analytics update: {e}")
    
    def add_custom_job(self, func, trigger, job_id: str, name: str = None):
        """Add a custom scheduled job"""
        try:
            self.scheduler.add_job(
                func=func,
                trigger=trigger,
                id=job_id,
                name=name or job_id,
                replace_existing=True
            )
            logger.info(f"Added custom job: {job_id}")
            
        except Exception as e:
            logger.error(f"Error adding custom job {job_id}: {e}")
    
    def remove_job(self, job_id: str):
        """Remove a scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Removed job: {job_id}")
            
        except Exception as e:
            logger.error(f"Error removing job {job_id}: {e}")
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        return jobs
    
    def run_job_now(self, job_id: str):
        """Run a job immediately"""
        try:
            job = self.scheduler.get_job(job_id)
            if job:
                job.modify(next_run_time=datetime.now())
                logger.info(f"Scheduled job {job_id} to run now")
            else:
                logger.warning(f"Job {job_id} not found")
                
        except Exception as e:
            logger.error(f"Error running job {job_id}: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get scheduler status"""
        return {
            "running": self.is_running,
            "jobs_count": len(self.scheduler.get_jobs()),
            "jobs": self.get_jobs()
        }

# Global scheduler instance
scheduler = YouTubeScheduler()
