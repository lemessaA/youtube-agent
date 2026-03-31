import os
from typing import Dict, Any, List, Optional
from supabase import create_client, Client
import logging
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseDB:
    def __init__(self):
        self.supabase_url: str = os.getenv("SUPABASE_URL")
        self.supabase_key: str = os.getenv("SUPABASE_KEY")
        self.storage_mode: str = os.getenv("STORAGE_MODE", "auto")  # auto, supabase, file
        
        # Initialize storage backend
        self.client = None
        self.file_storage = None
        
        self._initialize_storage()
        
    def _initialize_storage(self):
        """Initialize storage backend based on configuration"""
        from .enhanced_storage import EnhancedFileStorage
        
        # Force file storage mode or auto-detect
        if self.storage_mode == "file":
            logger.info("🗄️  Using file-based storage (forced)")
            self.file_storage = EnhancedFileStorage()
            return
        
        # Try Supabase first
        if self.supabase_url and self.supabase_key and "placeholder" not in self.supabase_url:
            try:
                self.client = create_client(self.supabase_url, self.supabase_key)
                
                # Test database access
                self.client.table("channels").select("id").limit(1).execute()
                logger.info("✅ Connected to Supabase with real database tables")
                return
                
            except Exception as e:
                if "schema cache" in str(e) or "not find the table" in str(e):
                    logger.warning("⚠️  Supabase connected but tables don't exist")
                    logger.info("📝 Run the setup script or check PRODUCTION_SETUP.md")
                else:
                    logger.warning(f"⚠️  Supabase connection failed: {e}")
        
        # Fallback to enhanced file storage
        logger.info("📁 Using enhanced file-based storage for production")
        self.file_storage = EnhancedFileStorage()
        
    def _use_file_storage(self) -> bool:
        """Check if using file storage"""
        return self.file_storage is not None
        
    def _check_connection(self):
        """Check if any storage backend is available"""
        if not self.client and not self.file_storage:
            raise Exception("No storage backend available")

    def _check_connection(self):
        """Check if database connection is available"""
        if not self.client:
            raise Exception("Database not connected. Please configure Supabase credentials.")

    # Channels CRUD operations
    def get_channels(self) -> List[Dict[str, Any]]:
        """Get all channels"""
        if self._use_file_storage():
            return self.file_storage.get_channels()
        
        try:
            response = self.client.table("channels").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching channels: {e}")
            return []

    def create_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new channel"""
        if self._use_file_storage():
            return self.file_storage.create_channel(channel_data)
            
        try:
            response = self.client.table("channels").insert(channel_data).execute()
            result = response.data[0] if response.data else {}
            logger.info(f"Created channel in Supabase: {result.get('name')}")
            return result
        except Exception as e:
            logger.error(f"Error creating channel: {e}")
            raise

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get channel by ID"""
        if self._use_file_storage():
            return self.file_storage.get_channel(channel_id)
            
        try:
            response = self.client.table("channels").select("*").eq("id", channel_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error fetching channel {channel_id}: {e}")
            return {}

    def update_channel(self, channel_id: str, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update channel"""
        if self._use_file_storage():
            return self.file_storage.update_channel(channel_id, channel_data)
            
        try:
            response = self.client.table("channels").update(channel_data).eq("id", channel_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error updating channel {channel_id}: {e}")
            raise

    def delete_channel(self, channel_id: str) -> bool:
        """Delete channel"""
        if self._use_file_storage():
            return self.file_storage.delete_channel(channel_id)
            
        try:
            self.client.table("channels").delete().eq("id", channel_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting channel {channel_id}: {e}")
            return False

    # Videos CRUD operations
    def get_videos(self, channel_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all videos or videos for specific channel"""
        if self._use_file_storage():
            return self.file_storage.get_videos(channel_id, limit)
            
        try:
            query = self.client.table("videos").select("*")
            if channel_id:
                query = query.eq("channel_id", channel_id)
            if limit:
                query = query.limit(limit)
            response = query.execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []

    def create_video(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new video"""
        if self._use_file_storage():
            return self.file_storage.create_video(video_data)
            
        try:
            response = self.client.table("videos").insert(video_data).execute()
            result = response.data[0] if response.data else {}
            logger.info(f"Created video in Supabase: {result.get('title')}")
            return result
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video by ID"""
        if self._use_file_storage():
            return self.file_storage.get_video(video_id)
            
        try:
            response = self.client.table("videos").select("*").eq("id", video_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error fetching video {video_id}: {e}")
            return {}

    def update_video(self, video_id: str, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update video"""
        if self._use_file_storage():
            return self.file_storage.update_video(video_id, video_data)
            
        try:
            response = self.client.table("videos").update(video_data).eq("id", video_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error updating video {video_id}: {e}")
            raise

    # Video Ideas CRUD operations
    def get_video_ideas(self, channel_id: str) -> List[Dict[str, Any]]:
        """Get video ideas for channel"""
        if self._use_file_storage():
            return self.file_storage.get_video_ideas(channel_id)
            
        try:
            response = self.client.table("video_ideas").select("*").eq("channel_id", channel_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching video ideas: {e}")
            return []

    def create_video_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new video idea"""
        if self._use_file_storage():
            return self.file_storage.create_video_idea(idea_data)
            
        try:
            response = self.client.table("video_ideas").insert(idea_data).execute()
            result = response.data[0] if response.data else {}
            logger.info(f"Created video idea in Supabase: {result.get('title')}")
            return result
        except Exception as e:
            logger.error(f"Error creating video idea: {e}")
            raise
    
    # Utility methods
    def get_storage_info(self) -> Dict[str, Any]:
        """Get information about current storage backend"""
        if self._use_file_storage():
            stats = self.file_storage.get_storage_stats()
            return {
                "mode": "file_storage",
                "persistent": True,
                "location": str(self.file_storage.storage_dir),
                "stats": stats
            }
        else:
            return {
                "mode": "supabase",
                "persistent": True,
                "location": self.supabase_url,
                "connected": self.client is not None
            }
    
    def create_backup(self) -> str:
        """Create a backup of current data"""
        if self._use_file_storage():
            return self.file_storage.create_full_backup()
        else:
            # For Supabase, we could implement export functionality
            logger.warning("Backup not implemented for Supabase mode")
            return "Backup not available for Supabase mode"

# Global database instance
db = SupabaseDB()
