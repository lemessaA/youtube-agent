from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from typing import Dict, Any, List
from utils.scheduler import scheduler
from utils.exceptions import create_not_found_exception, create_internal_server_exception
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/scheduler", tags=["scheduler"])

@router.get("/status")
async def get_scheduler_status():
    """Get scheduler status and jobs"""
    try:
        status = scheduler.get_status()
        return status
        
    except Exception as e:
        logger.error(f"Error getting scheduler status: {e}")
        raise create_internal_server_exception("Failed to get scheduler status")

@router.post("/start")
async def start_scheduler():
    """Start the scheduler"""
    try:
        scheduler.start()
        return {"message": "Scheduler started successfully"}
        
    except Exception as e:
        logger.error(f"Error starting scheduler: {e}")
        raise create_internal_server_exception("Failed to start scheduler")

@router.post("/stop")
async def stop_scheduler():
    """Stop the scheduler"""
    try:
        scheduler.stop()
        return {"message": "Scheduler stopped successfully"}
        
    except Exception as e:
        logger.error(f"Error stopping scheduler: {e}")
        raise create_internal_server_exception("Failed to stop scheduler")

@router.get("/jobs")
async def get_scheduled_jobs():
    """Get all scheduled jobs"""
    try:
        jobs = scheduler.get_jobs()
        return {"jobs": jobs}
        
    except Exception as e:
        logger.error(f"Error getting scheduled jobs: {e}")
        raise create_internal_server_exception("Failed to get scheduled jobs")

@router.post("/jobs/{job_id}/run")
async def run_job_now(job_id: str):
    """Run a specific job immediately"""
    try:
        scheduler.run_job_now(job_id)
        return {"message": f"Job {job_id} scheduled to run now"}
        
    except Exception as e:
        logger.error(f"Error running job {job_id}: {e}")
        raise create_internal_server_exception(f"Failed to run job {job_id}")

@router.delete("/jobs/{job_id}")
async def remove_job(job_id: str):
    """Remove a scheduled job"""
    try:
        scheduler.remove_job(job_id)
        return {"message": f"Job {job_id} removed successfully"}
        
    except Exception as e:
        logger.error(f"Error removing job {job_id}: {e}")
        raise create_internal_server_exception(f"Failed to remove job {job_id}")

@router.post("/jobs/{job_id}/run-daily")
async def run_daily_automation_now(background_tasks: BackgroundTasks):
    """Run daily automation immediately"""
    try:
        background_tasks.add_task(scheduler._run_daily_automation)
        return {"message": "Daily automation started"}
        
    except Exception as e:
        logger.error(f"Error running daily automation: {e}")
        raise create_internal_server_exception("Failed to run daily automation")

@router.post("/jobs/{job_id}/run-trends")
async def run_trend_research_now(background_tasks: BackgroundTasks):
    """Run trend research immediately"""
    try:
        background_tasks.add_task(scheduler._run_trend_research)
        return {"message": "Trend research started"}
        
    except Exception as e:
        logger.error(f"Error running trend research: {e}")
        raise create_internal_server_exception("Failed to run trend research")

@router.post("/jobs/{job_id}/run-analytics")
async def run_analytics_update_now(background_tasks: BackgroundTasks):
    """Run analytics update immediately"""
    try:
        background_tasks.add_task(scheduler._run_analytics_update)
        return {"message": "Analytics update started"}
        
    except Exception as e:
        logger.error(f"Error running analytics update: {e}")
        raise create_internal_server_exception("Failed to run analytics update")
