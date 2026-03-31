import os
from typing import Dict, Any, List, Optional
from supabase import create_client, Client
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseDB:
    def __init__(self):
        self.supabase_url: str = os.getenv("SUPABASE_URL")
        self.supabase_key: str = os.getenv("SUPABASE_KEY")
        
        if not self.supabase_url or not self.supabase_key or "placeholder" in self.supabase_url:
            logger.warning("Supabase credentials not configured. Database operations will be disabled.")
            self.client = None
        else:
            self.client: Client = create_client(self.supabase_url, self.supabase_key)

# Global database instance
db = SupabaseDB()
