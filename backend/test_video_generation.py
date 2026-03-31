#!/usr/bin/env python3
"""
Test script for real video generation
"""

import sys
import os
import asyncio
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from agents.video_generation_agent import VideoGenerationAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_real_video_generation():
    """Test creating a real video file"""
    try:
        # Create video generation agent
        video_agent = VideoGenerationAgent()
        
        # Create test video plan
        video_plan = {
            "scenes": [
                {
                    "scene_number": 1,
                    "duration": 3,
                    "visual_type": "title_screen",
                    "on_screen_text": "TEST VIDEO",
                    "voiceover": "This is a test"
                },
                {
                    "scene_number": 2,
                    "duration": 5,
                    "visual_type": "content",
                    "on_screen_text": "Real Video Generation Working!",
                    "voiceover": "Testing real video creation"
                },
                {
                    "scene_number": 3,
                    "duration": 2,
                    "visual_type": "end",
                    "on_screen_text": "SUCCESS!",
                    "voiceover": "Video generation complete"
                }
            ],
            "color_scheme": ["#1d4ed8", "#000000", "#ffffff"]
        }
        
        # Generate video
        output_path = "/home/lemessa-ahmed/youtube-agent/backend/videos/test_real_video.mp4"
        logger.info(f"🎬 Creating real video file: {output_path}")
        
        result_path = await video_agent.create_video_file(video_plan, output_path)
        
        # Check if file was created
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            logger.info(f"✅ SUCCESS! Video file created:")
            logger.info(f"   📁 Path: {result_path}")
            logger.info(f"   📏 Size: {file_size / (1024*1024):.2f} MB")
            logger.info(f"   🎞️ Duration: ~10 seconds")
            return True
        else:
            logger.error(f"❌ Video file not found at: {result_path}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Video generation test failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🎬 TESTING REAL VIDEO GENERATION")
    logger.info("=" * 60)
    
    # Run the test
    result = asyncio.run(test_real_video_generation())
    
    if result:
        logger.info("=" * 60)
        logger.info("🎉 SUCCESS: Real video generation is working!")
        logger.info("🚀 Your app can now create actual MP4 video files!")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ FAILED: Real video generation needs debugging")
        logger.error("=" * 60)