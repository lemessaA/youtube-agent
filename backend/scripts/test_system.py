#!/usr/bin/env python3
"""
System test script for YouTube Automation System
"""

import os
import sys
import asyncio
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents import DailyAutomationAgent, TrendResearchAgent
from models import NicheType
from config import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_trend_research():
    """Test trend research agent"""
    logger.info("Testing Trend Research Agent...")
    
    try:
        agent = TrendResearchAgent()
        ideas = await agent.research_trends(NicheType.AI_TOOLS)
        
        logger.info(f"Generated {len(ideas)} video ideas:")
        for i, idea in enumerate(ideas[:3]):  # Show first 3
            logger.info(f"  {i+1}. {idea.title} (Score: {idea.viral_score})")
        
        return True
        
    except Exception as e:
        logger.error(f"Trend research test failed: {e}")
        return False

async def test_daily_automation():
    """Test daily automation workflow"""
    logger.info("Testing Daily Automation Agent...")
    
    try:
        # Get or create a test channel
        channels = db.get_channels()
        
        if not channels:
            logger.error("No channels found. Please run setup_database.py first.")
            return False
        
        channel_id = channels[0]['id']
        logger.info(f"Using channel: {channels[0]['name']}")
        
        # Run automation
        agent = DailyAutomationAgent()
        result = await agent.run_daily_automation(channel_id)
        
        if result.get("error"):
            logger.error(f"Daily automation failed: {result['error']}")
            return False
        
        logger.info("Daily automation completed successfully!")
        logger.info(f"Status: {result.get('status')}")
        
        if result.get("video"):
            logger.info(f"Generated video: {result['video'].title}")
        
        return True
        
    except Exception as e:
        logger.error(f"Daily automation test failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    logger.info("Testing database connection...")
    
    try:
        channels = db.get_channels()
        logger.info(f"Database connection successful. Found {len(channels)} channels.")
        return True
        
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

async def run_all_tests():
    """Run all system tests"""
    logger.info("Starting YouTube Automation System tests...")
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Trend Research", test_trend_research),
        ("Daily Automation", test_daily_automation)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Running {test_name} Test ---")
        
        if asyncio.iscoroutinefunction(test_func):
            result = await test_func()
        else:
            result = test_func()
        
        results[test_name] = result
        
        if result:
            logger.info(f"✅ {test_name} test PASSED")
        else:
            logger.error(f"❌ {test_name} test FAILED")
    
    # Summary
    logger.info("\n--- Test Summary ---")
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! System is ready to use.")
        return True
    else:
        logger.error("Some tests failed. Please check the errors above.")
        return False

def check_environment():
    """Check if environment variables are set"""
    logger.info("Checking environment variables...")
    
    required_vars = ["OLLAMA_BASE_URL", "SUPABASE_URL", "SUPABASE_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing environment variables: {', '.join(missing_vars)}")
        logger.error("Please set these variables in your .env file")
        return False
    
    logger.info("✅ Environment variables check passed!")
    
    # Check Ollama connection
    try:
        import requests
        response = requests.get(f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/tags", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Ollama connection check passed!")
        else:
            logger.error("❌ Ollama is not responding")
            return False
    except Exception as e:
        logger.error(f"❌ Ollama connection failed: {e}")
        logger.error("Please make sure Ollama is running: ollama serve")
        return False
    
    return True

async def main():
    """Main test function"""
    logger.info("YouTube Automation System - Test Suite")
    logger.info("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Run tests
    success = await run_all_tests()
    
    if success:
        logger.info("\n🚀 System is ready for production use!")
        logger.info("Start the server with: python -m app.main")
    else:
        logger.error("\n❌ System tests failed. Please fix issues before using.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
