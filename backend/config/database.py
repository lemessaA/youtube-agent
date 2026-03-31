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
        
        # In-memory storage for mock mode
        self.mock_channels = []
        self.mock_videos = []
        self.mock_ideas = []
        
        if not self.supabase_url or not self.supabase_key or "placeholder" in self.supabase_url or "example" in self.supabase_url:
            logger.warning("Supabase credentials not configured. Database operations will use mock data.")
            self.client = None
        else:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
                # Test the connection by trying to access a table
                try:
                    self.client.table("channels").select("id").limit(1).execute()
                    logger.info("Connected to Supabase successfully")
                except Exception as table_error:
                    logger.warning(f"Supabase connected but tables not accessible: {table_error}")
                    logger.warning("Falling back to mock data mode")
                    self.client = None
            except Exception as e:
                logger.error(f"Failed to connect to Supabase: {e}")
                self.client = None

    def _check_connection(self):
        """Check if database connection is available"""
        if not self.client:
            raise Exception("Database not connected. Please configure Supabase credentials.")

    # Channels CRUD operations
    def get_channels(self) -> List[Dict[str, Any]]:
        """Get all channels"""
        if not self.client:
            logger.debug("Database not configured, returning mock data")
            return self.mock_channels.copy()
        
        try:
            response = self.client.table("channels").select("*").execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching channels: {e}")
            return []

    def create_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new channel"""
        if not self.client:
            # Create and store mock data when database not configured
            mock_channel = {
                "id": f"mock_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:17]}",  # Include microseconds for uniqueness
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                **channel_data
            }
            self.mock_channels.append(mock_channel)
            logger.info(f"Created mock channel: {mock_channel['name']}")
            return mock_channel
            
        try:
            response = self.client.table("channels").insert(channel_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error creating channel: {e}")
            raise

    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get channel by ID"""
        if not self.client:
            return {}
            
        try:
            response = self.client.table("channels").select("*").eq("id", channel_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error fetching channel {channel_id}: {e}")
            return {}

    def update_channel(self, channel_id: str, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update channel"""
        if not self.client:
            return {}
            
        try:
            response = self.client.table("channels").update(channel_data).eq("id", channel_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error updating channel {channel_id}: {e}")
            raise

    def delete_channel(self, channel_id: str) -> bool:
        """Delete channel"""
        if not self.client:
            return True
            
        try:
            self.client.table("channels").delete().eq("id", channel_id).execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting channel {channel_id}: {e}")
            return False

    # Videos CRUD operations
    def get_videos(self, channel_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get all videos or videos for specific channel"""
        if not self.client:
            logger.debug("Database not configured, returning mock videos")
            videos = self.mock_videos.copy()
            if channel_id:
                videos = [v for v in videos if v.get('channel_id') == channel_id]
            if limit:
                videos = videos[:limit]
            return videos
            
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
        if not self.client:
            mock_video = {
                "id": f"mock_video_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "created_at": datetime.now().isoformat(),
                **video_data
            }
            logger.info(f"Database not configured, returning mock video: {mock_video.get('title', 'Untitled')}")
            return mock_video
            
        try:
            response = self.client.table("videos").insert(video_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error creating video: {e}")
            raise

    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video by ID"""
        if not self.client:
            return {}
            
        try:
            response = self.client.table("videos").select("*").eq("id", video_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error fetching video {video_id}: {e}")
            return {}

    def update_video(self, video_id: str, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update video"""
        if not self.client:
            return {}
            
        try:
            response = self.client.table("videos").update(video_data).eq("id", video_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error updating video {video_id}: {e}")
            raise

    # Video Ideas CRUD operations
    def get_video_ideas(self, channel_id: str) -> List[Dict[str, Any]]:
        """Get video ideas for channel"""
        if not self.client:
            return []
            
        try:
            response = self.client.table("video_ideas").select("*").eq("channel_id", channel_id).execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching video ideas: {e}")
            return []

    def create_video_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new video idea"""
        if not self.client:
            mock_idea = {
                "id": f"mock_idea_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "created_at": datetime.now().isoformat(),
                **idea_data
            }
            return mock_idea
            
        try:
            response = self.client.table("video_ideas").insert(idea_data).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            logger.error(f"Error creating video idea: {e}")
            raise

# Global database instance
db = SupabaseDB()
