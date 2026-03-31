#!/usr/bin/env python3
"""
Production runner for YouTube Automation System
"""

import os
import sys
import asyncio
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.main import app
from utils.scheduler import scheduler
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_production_config():
    """Check production configuration"""
    logger.info("Checking production configuration...")
    
    # Check required environment variables
    required_vars = ["OPENAI_API_KEY", "SUPABASE_URL", "SUPABASE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    # Check production settings
    debug_mode = os.getenv("DEBUG", "false").lower() in ["true", "1", "yes"]
    if debug_mode:
        logger.warning("⚠️  DEBUG mode is enabled in production!")
    
    # Check if we have a secret key
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key or secret_key == "your_secret_key_here":
        logger.error("SECRET_KEY is not set or is using default value!")
        return False
    
    logger.info("✅ Production configuration check passed!")
    return True

def setup_logging():
    """Setup production logging"""
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure file logging
    file_handler = logging.FileHandler(log_dir / "youtube_automation.log")
    file_handler.setLevel(log_level)
    
    # Configure console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(log_level)

async def start_scheduler():
    """Start the scheduler"""
    try:
        logger.info("Starting scheduler...")
        scheduler.start()
        logger.info("Scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to start scheduler: {e}")
        return False
    
    return True

def get_server_config():
    """Get server configuration"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    
    return {
        "host": host,
        "port": port,
        "workers": workers,
        "reload": False,  # Never reload in production
        "log_level": os.getenv("LOG_LEVEL", "info").lower()
    }

def run_production_server():
    """Run the production server"""
    logger.info("Starting YouTube Automation System in Production Mode")
    logger.info("=" * 60)
    
    # Check configuration
    if not check_production_config():
        sys.exit(1)
    
    # Setup logging
    setup_logging()
    
    # Get server config
    config = get_server_config()
    
    logger.info(f"Server configuration: {config}")
    
    try:
        # Start scheduler
        scheduler.start()
        logger.info("Scheduler started")
        
        # Run server
        logger.info(f"Starting server on {config['host']}:{config['port']}")
        
        uvicorn.run(
            app,
            host=config["host"],
            port=config["port"],
            workers=config["workers"],
            reload=config["reload"],
            log_level=config["log_level"]
        )
        
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        scheduler.stop()
        logger.info("Server stopped gracefully")
        
    except Exception as e:
        logger.error(f"Server error: {e}")
        scheduler.stop()
        sys.exit(1)

if __name__ == "__main__":
    run_production_server()
