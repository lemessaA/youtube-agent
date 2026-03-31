"""
Enhanced file-based storage system for production deployment
Provides persistent data storage without external dependencies
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging
import fcntl
import shutil

logger = logging.getLogger(__name__)

class EnhancedFileStorage:
    """Production-ready file-based storage with atomic operations and backups"""
    
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Create subdirectories for different data types
        self.channels_file = self.storage_dir / "channels.json"
        self.videos_file = self.storage_dir / "videos.json"
        self.video_ideas_file = self.storage_dir / "video_ideas.json" 
        self.analytics_file = self.storage_dir / "analytics.json"
        self.backup_dir = self.storage_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Initialize files if they don't exist
        self._init_files()
        
        logger.info(f"Enhanced file storage initialized at: {self.storage_dir}")
    
    def _init_files(self):
        """Initialize JSON files if they don't exist"""
        files_to_init = [
            self.channels_file,
            self.videos_file, 
            self.video_ideas_file,
            self.analytics_file
        ]
        
        for file_path in files_to_init:
            if not file_path.exists():
                self._safe_write_json(file_path, [])
    
    def _safe_write_json(self, file_path: Path, data: Any):
        """Atomic write operation with backup"""
        try:
            # Create backup if file exists
            if file_path.exists():
                backup_name = f"{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_path = self.backup_dir / backup_name
                shutil.copy2(file_path, backup_path)
            
            # Write to temporary file first
            temp_file = file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)  # Exclusive lock
                json.dump(data, f, indent=2, default=str, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())  # Force write to disk
            
            # Atomic move
            temp_file.replace(file_path)
            
        except Exception as e:
            logger.error(f"Failed to write {file_path}: {e}")
            raise
    
    def _safe_read_json(self, file_path: Path) -> List[Dict[str, Any]]:
        """Safe read operation with error handling"""
        try:
            if not file_path.exists():
                return []
                
            with open(file_path, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)  # Shared lock
                data = json.load(f)
                return data if isinstance(data, list) else []
                
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logger.warning(f"Error reading {file_path}: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error reading {file_path}: {e}")
            return []
    
    # Channel operations
    def get_channels(self) -> List[Dict[str, Any]]:
        """Get all channels"""
        return self._safe_read_json(self.channels_file)
    
    def create_channel(self, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new channel"""
        channels = self.get_channels()
        
        new_channel = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            **channel_data
        }
        
        channels.append(new_channel)
        self._safe_write_json(self.channels_file, channels)
        
        logger.info(f"Created channel: {new_channel['name']}")
        return new_channel
    
    def get_channel(self, channel_id: str) -> Dict[str, Any]:
        """Get channel by ID"""
        channels = self.get_channels()
        return next((c for c in channels if c['id'] == channel_id), {})
    
    def update_channel(self, channel_id: str, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update channel"""
        channels = self.get_channels()
        
        for i, channel in enumerate(channels):
            if channel['id'] == channel_id:
                updated_channel = {
                    **channel,
                    **channel_data,
                    "updated_at": datetime.now().isoformat()
                }
                channels[i] = updated_channel
                self._safe_write_json(self.channels_file, channels)
                logger.info(f"Updated channel: {updated_channel['name']}")
                return updated_channel
        
        return {}
    
    def delete_channel(self, channel_id: str) -> bool:
        """Delete channel"""
        channels = self.get_channels()
        original_count = len(channels)
        
        channels = [c for c in channels if c['id'] != channel_id]
        
        if len(channels) < original_count:
            self._safe_write_json(self.channels_file, channels)
            logger.info(f"Deleted channel: {channel_id}")
            return True
        return False
    
    # Video operations
    def get_videos(self, channel_id: Optional[str] = None, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get videos with optional filtering"""
        videos = self._safe_read_json(self.videos_file)
        
        if channel_id:
            videos = [v for v in videos if v.get('channel_id') == channel_id]
        
        if limit:
            videos = videos[:limit]
            
        return videos
    
    def create_video(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new video"""
        videos = self.get_videos()
        
        new_video = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            **video_data
        }
        
        videos.append(new_video)
        self._safe_write_json(self.videos_file, videos)
        
        logger.info(f"Created video: {new_video['title']}")
        return new_video
    
    def get_video(self, video_id: str) -> Dict[str, Any]:
        """Get video by ID"""
        videos = self.get_videos()
        return next((v for v in videos if v['id'] == video_id), {})
    
    def update_video(self, video_id: str, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update video"""
        videos = self.get_videos()
        
        for i, video in enumerate(videos):
            if video['id'] == video_id:
                updated_video = {
                    **video,
                    **video_data,
                    "updated_at": datetime.now().isoformat()
                }
                videos[i] = updated_video
                self._safe_write_json(self.videos_file, videos)
                logger.info(f"Updated video: {updated_video['title']}")
                return updated_video
        
        return {}
    
    # Video ideas operations
    def get_video_ideas(self, channel_id: str) -> List[Dict[str, Any]]:
        """Get video ideas for channel"""
        ideas = self._safe_read_json(self.video_ideas_file)
        return [idea for idea in ideas if idea.get('channel_id') == channel_id]
    
    def create_video_idea(self, idea_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new video idea"""
        ideas = self._safe_read_json(self.video_ideas_file)
        
        new_idea = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            **idea_data
        }
        
        ideas.append(new_idea)
        self._safe_write_json(self.video_ideas_file, ideas)
        
        logger.info(f"Created video idea: {new_idea['title']}")
        return new_idea
    
    # Analytics operations
    def create_analytics(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create analytics entry"""
        analytics = self._safe_read_json(self.analytics_file)
        
        new_analytics = {
            "id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            **analytics_data
        }
        
        analytics.append(new_analytics)
        self._safe_write_json(self.analytics_file, analytics)
        return new_analytics
    
    # Backup operations
    def create_full_backup(self) -> str:
        """Create a complete backup of all data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"full_backup_{timestamp}"
        backup_path = self.backup_dir / backup_name
        backup_path.mkdir()
        
        files_to_backup = [
            self.channels_file,
            self.videos_file,
            self.video_ideas_file,
            self.analytics_file
        ]
        
        for file_path in files_to_backup:
            if file_path.exists():
                shutil.copy2(file_path, backup_path / file_path.name)
        
        logger.info(f"Created full backup: {backup_name}")
        return str(backup_path)
    
    # Statistics
    def get_storage_stats(self) -> Dict[str, Any]:
        """Get storage statistics"""
        stats = {}
        
        for name, file_path in [
            ('channels', self.channels_file),
            ('videos', self.videos_file), 
            ('video_ideas', self.video_ideas_file),
            ('analytics', self.analytics_file)
        ]:
            data = self._safe_read_json(file_path)
            stats[name] = {
                'count': len(data),
                'file_size': file_path.stat().st_size if file_path.exists() else 0
            }
        
        return stats