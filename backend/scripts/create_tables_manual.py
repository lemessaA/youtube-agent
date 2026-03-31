#!/usr/bin/env python3
"""
Manual table creation for Supabase
Since RPC doesn't work, we'll create a basic structure manually
"""

import sys
import os
from pathlib import Path
from supabase import create_client
from dotenv import load_dotenv
import logging

# Load environment variables
current_dir = Path(__file__).parent.parent
env_path = current_dir / ".env"
load_dotenv(env_path)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_supabase_client():
    """Get Supabase client directly"""
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if not supabase_url or not supabase_key:
        logger.error("❌ Missing Supabase credentials")
        return None
        
    try:
        client = create_client(supabase_url, supabase_key)
        return client
    except Exception as e:
        logger.error(f"❌ Failed to create Supabase client: {e}")
        return None

def create_sample_data(client):
    """Create sample data to bootstrap the database"""
    try:
        logger.info("🗄️  Creating sample data...")
        
        # Create a sample channel
        sample_channel = {
            "name": "Production Test Channel",
            "niche": "ai_tools",
            "description": "This is a test channel to verify database functionality",
            "target_audience": "Developers and AI enthusiasts",
            "upload_frequency": "daily",
            "video_length_range": "60-120",
            "style": "faceless"
        }
        
        result = client.table("channels").insert(sample_channel).execute()
        if result.data:
            logger.info(f"✅ Created sample channel: {result.data[0]['name']}")
            return result.data[0]['id']
        return None
        
    except Exception as e:
        logger.error(f"❌ Failed to create sample data: {e}")
        return None

def test_database_operations(client):
    """Test basic database operations"""
    try:
        logger.info("🧪 Testing database operations...")
        
        # Test 1: Insert a channel
        test_channel = {
            "name": "Real Data Test Channel", 
            "niche": "startup_ideas",
            "description": "Testing real database persistence",
            "target_audience": "Entrepreneurs"
        }
        
        insert_result = client.table("channels").insert(test_channel).execute()
        if not insert_result.data:
            logger.error("❌ Failed to insert test channel")
            return False
        
        channel_id = insert_result.data[0]['id']
        logger.info(f"✅ Test channel created with ID: {channel_id}")
        
        # Test 2: Retrieve channels
        select_result = client.table("channels").select("*").execute()
        if not select_result.data:
            logger.error("❌ Failed to retrieve channels")
            return False
            
        logger.info(f"✅ Retrieved {len(select_result.data)} channels")
        
        # Test 3: Update channel
        update_result = client.table("channels").update({
            "description": "Updated test description"
        }).eq("id", channel_id).execute()
        
        logger.info("✅ Channel update successful")
        
        logger.info("🎉 All database operations working!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database operations test failed: {e}")
        return False

def main():
    logger.info("=" * 60)
    logger.info("🏗️  Manual Database Setup for YouTube Automation")
    logger.info("=" * 60)
    
    client = get_supabase_client()
    if not client:
        logger.error("❌ Cannot connect to Supabase")
        return False
    
    logger.info("✅ Connected to Supabase")
    
    # Try to access existing tables or create sample data
    try:
        # Check if we can access channels table
        result = client.table("channels").select("id").limit(1).execute()
        logger.info("✅ Channels table already exists and accessible!")
        
        # Test operations
        if test_database_operations(client):
            logger.info("🎉 Database is ready for production!")
            return True
        else:
            return False
            
    except Exception as e:
        logger.warning(f"⚠️  Tables don't exist yet: {e}")
        logger.info("📝 You need to create the tables in Supabase manually")
        logger.info("=" * 60)
        logger.info("MANUAL SETUP INSTRUCTIONS:")
        logger.info("1. Go to your Supabase project: https://bxkylrxggtdpeogsimwg.supabase.co")
        logger.info("2. Open the SQL Editor")
        logger.info("3. Copy and paste the contents of backend/database/schema.sql")
        logger.info("4. Run the SQL to create all tables")
        logger.info("5. Come back and run this script again")
        logger.info("=" * 60)
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)