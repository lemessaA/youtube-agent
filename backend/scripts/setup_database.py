#!/usr/bin/env python3
"""
Database setup script for YouTube Automation System
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config.database import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_database():
    """Set up the database with required tables"""
    try:
        logger.info("Setting up database...")
        
        # Test database connection
        logger.info("Testing database connection...")
        channels = db.get_channels()
        logger.info(f"Database connection successful. Found {len(channels)} channels.")
        
        # Create test channel if none exists
        if not channels:
            logger.info("Creating test channel...")
            test_channel = {
                "name": "AI Tools Daily",
                "niche": "ai_tools",
                "description": "Daily AI tools and tips for developers",
                "target_audience": "Developers and tech enthusiasts",
                "upload_frequency": "daily",
                "video_length_range": "60-120",
                "style": "faceless",
                "monetization_enabled": False
            }
            
            result = db.insert_channel(test_channel)
            if result:
                logger.info(f"Test channel created with ID: {result['id']}")
            else:
                logger.error("Failed to create test channel")
        
        logger.info("Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Database setup failed: {e}")
        return False

def check_environment():
    """Check if environment variables are set"""
    required_vars = ["OLLAMA_BASE_URL", "SUPABASE_URL", "SUPABASE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file")
        return False
    
    logger.info("Environment variables check passed!")
    return True

def main():
    """Main setup function"""
    logger.info("Starting YouTube Automation System setup...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    logger.info("Setup completed successfully!")
    logger.info("You can now start the application with: python -m app.main")

if __name__ == "__main__":
    main()
