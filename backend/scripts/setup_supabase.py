#!/usr/bin/env python3
"""
Direct Supabase setup script
Creates tables directly using the Supabase client
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

def create_tables_sql():
    """Return the SQL commands to create tables"""
    return [
        # Channels table
        """
        CREATE TABLE IF NOT EXISTS channels (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            niche VARCHAR(50) NOT NULL,
            youtube_channel_id VARCHAR(100),
            description TEXT,
            target_audience TEXT,
            upload_frequency VARCHAR(20) DEFAULT 'daily',
            video_length_range VARCHAR(20) DEFAULT '60-120',
            style VARCHAR(50) DEFAULT 'faceless',
            monetization_enabled BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """,
        
        # Video ideas table
        """
        CREATE TABLE IF NOT EXISTS video_ideas (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            hook TEXT,
            call_to_action TEXT,
            tags JSONB DEFAULT '[]',
            estimated_views INTEGER DEFAULT 0,
            confidence_score INTEGER DEFAULT 50,
            trend_source VARCHAR(100),
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """,
        
        # Videos table
        """
        CREATE TABLE IF NOT EXISTS videos (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            channel_id UUID REFERENCES channels(id) ON DELETE CASCADE,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            script TEXT,
            thumbnail_url TEXT,
            video_url TEXT,
            status VARCHAR(20) DEFAULT 'draft',
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            revenue DECIMAL(10,2) DEFAULT 0.0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
            published_at TIMESTAMP WITH TIME ZONE
        )
        """,
        
        # Analytics table
        """
        CREATE TABLE IF NOT EXISTS analytics (
            id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
            video_id UUID REFERENCES videos(id) ON DELETE CASCADE,
            date DATE NOT NULL,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            watch_time INTEGER DEFAULT 0,
            ctr DECIMAL(5,2) DEFAULT 0.0,
            audience_retention DECIMAL(5,2) DEFAULT 0.0,
            revenue DECIMAL(10,2) DEFAULT 0.0,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
        )
        """
    ]

def setup_database():
    """Set up the database tables"""
    client = get_supabase_client()
    if not client:
        return False
        
    try:
        logger.info("🚀 Setting up Supabase database tables...")
        
        sql_commands = create_tables_sql()
        
        for i, sql in enumerate(sql_commands):
            try:
                logger.info(f"⏳ Creating table {i+1}/{len(sql_commands)}...")
                
                # Execute SQL using Supabase RPC
                result = client.rpc('exec_sql', {'sql': sql.strip()}).execute()
                logger.info(f"✅ Table {i+1} created successfully")
                
            except Exception as e:
                if "already exists" in str(e):
                    logger.info(f"✅ Table {i+1} already exists")
                else:
                    logger.error(f"❌ Failed to create table {i+1}: {e}")
                    return False
        
        # Test the setup
        logger.info("🧪 Testing database setup...")
        
        # Test channels table
        test_result = client.table("channels").select("id").limit(1).execute()
        logger.info("✅ Channels table accessible")
        
        # Test videos table
        test_result = client.table("videos").select("id").limit(1).execute() 
        logger.info("✅ Videos table accessible")
        
        logger.info("🎉 Database setup completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🗄️  YouTube Automation - Database Setup")
    logger.info("=" * 60)
    
    success = setup_database()
    
    if success:
        logger.info("=" * 60) 
        logger.info("🎉 SUCCESS: Database is ready for production!")
        logger.info("🔄 Next: Restart your backend server to use real data")
        logger.info("=" * 60)
    else:
        logger.error("=" * 60)
        logger.error("❌ FAILED: Database setup incomplete")
        logger.error("Please check your Supabase project settings")
        logger.error("=" * 60)
        sys.exit(1)