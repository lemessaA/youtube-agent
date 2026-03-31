#!/usr/bin/env python3
"""
Database setup script for YouTube Automation System
Sets up all required tables in Supabase
"""

import sys
import os
from pathlib import Path

# Add parent directory to Python path
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from config.database import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_schema_file():
    """Read the SQL schema file"""
    schema_path = current_dir / "database" / "schema.sql"
    with open(schema_path, 'r') as file:
        return file.read()

def setup_database():
    """Set up the database tables"""
    try:
        if not db.client:
            logger.error("❌ Supabase client not initialized")
            logger.error("Please check your SUPABASE_URL and SUPABASE_KEY in .env file")
            return False

        logger.info("🚀 Setting up database tables...")
        
        # Read schema SQL
        schema_sql = read_schema_file()
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip() and not stmt.strip().startswith('--')]
        
        logger.info(f"📝 Found {len(statements)} SQL statements to execute")
        
        # Execute each statement
        for i, statement in enumerate(statements):
            try:
                if statement.strip():
                    logger.info(f"⏳ Executing statement {i+1}/{len(statements)}")
                    db.client.rpc('exec_sql', {'sql': statement}).execute()
                    logger.info(f"✅ Statement {i+1} executed successfully")
            except Exception as e:
                logger.warning(f"⚠️  Statement {i+1} failed (might already exist): {e}")
                continue
        
        logger.info("🎉 Database setup completed!")
        
        # Test the setup by creating a test channel
        test_channel = {
            "name": "Database Test Channel",
            "niche": "ai_tools",
            "description": "Testing real database connection",
            "target_audience": "Database testers"
        }
        
        logger.info("🧪 Testing database with sample channel...")
        result = db.create_channel(test_channel)
        
        if result and 'id' in result:
            logger.info(f"✅ Database test successful! Created channel: {result['name']}")
            
            # Test retrieval
            channels = db.get_channels()
            logger.info(f"✅ Retrieved {len(channels)} channels from database")
            
            return True
        else:
            logger.error("❌ Database test failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Database setup failed: {e}")
        return False

def verify_tables():
    """Verify all tables exist"""
    required_tables = [
        'channels', 'videos', 'video_ideas', 'scripts', 
        'thumbnails', 'analytics', 'trending_topics', 
        'monetization_strategies', 'automation_logs'
    ]
    
    try:
        for table in required_tables:
            try:
                db.client.table(table).select("id").limit(1).execute()
                logger.info(f"✅ Table '{table}' exists and accessible")
            except Exception as e:
                logger.error(f"❌ Table '{table}' not accessible: {e}")
                return False
        
        logger.info("🎉 All required tables are accessible!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Table verification failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🏗️  YouTube Automation System - Database Setup")
    logger.info("=" * 60)
    
    # Check connection first
    if not db.client:
        logger.error("❌ Database connection failed")
        logger.error("Please verify your Supabase credentials in backend/.env:")
        logger.error("  - SUPABASE_URL=https://your-project.supabase.co")
        logger.error("  - SUPABASE_KEY=your_supabase_key")
        sys.exit(1)
    
    logger.info("✅ Supabase connection established")
    
    # Setup database
    success = setup_database()
    
    if success:
        logger.info("=" * 60)
        logger.info("🎉 Database setup completed successfully!")
        logger.info("🚀 Your app is now ready for production with persistent data!")
        logger.info("=" * 60)
        logger.info("Next steps:")
        logger.info("1. Restart your backend server: python run.py")
        logger.info("2. Visit your frontend: http://localhost:3000")
        logger.info("3. Create channels - they will be saved permanently!")
    else:
        logger.error("=" * 60)
        logger.error("❌ Database setup failed!")
        logger.error("Please check the error messages above and try again.")
        sys.exit(1)