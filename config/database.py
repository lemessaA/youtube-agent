from supabase import create_client, Client
from typing import Optional, Dict, Any, List
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseDB:
    def __init__(self):
        self.supabase_url: str = os.getenv("SUPABASE_URL")
        self.supabase_key: str = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        
        self.client: Client = create_client(self.supabase_url, self.supabase_key)
    
    def insert_video_idea(self, video_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            result = self.client.table("video_ideas").insert(video_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting video idea: {e}")
            return None
    
    def get_video_ideas(self, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            result = self.client.table("video_ideas").select("*").limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting video ideas: {e}")
            return []
    
    def insert_video(self, video_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            result = self.client.table("videos").insert(video_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting video: {e}")
            return None
    
    def get_videos(self, channel_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            query = self.client.table("videos").select("*")
            if channel_id:
                query = query.eq("channel_id", channel_id)
            result = query.limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting videos: {e}")
            return []
    
    def update_video_analytics(self, video_id: str, analytics_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            result = self.client.table("videos").update(analytics_data).eq("id", video_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error updating video analytics: {e}")
            return None
    
    def insert_channel(self, channel_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        try:
            result = self.client.table("channels").insert(channel_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            logger.error(f"Error inserting channel: {e}")
            return None
    
    def get_channels(self) -> List[Dict[str, Any]]:
        try:
            result = self.client.table("channels").select("*").execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting channels: {e}")
            return []
    
    def get_trending_topics(self, niche: str, limit: int = 10) -> List[Dict[str, Any]]:
        try:
            result = self.client.table("trending_topics").select("*").eq("niche", niche).limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []

# Global database instance
db = SupabaseDB()
