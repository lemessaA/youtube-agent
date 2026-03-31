import os
import re
import hashlib
import uuid
import json
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)

def generate_unique_id() -> str:
    """Generate a unique ID"""
    return str(uuid.uuid4())

def generate_hash(text: str) -> str:
    """Generate SHA-256 hash of text"""
    return hashlib.sha256(text.encode()).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe file system usage"""
    # Remove or replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = re.sub(r'\s+', '_', filename)
    filename = filename.strip('._')
    
    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename

def format_duration(seconds: int) -> str:
    """Format duration in seconds to human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        return f"{hours}h {remaining_minutes}m"

def parse_duration(duration_str: str) -> int:
    """Parse duration string to seconds"""
    if not duration_str:
        return 0
    
    # Handle ISO 8601 duration format (PT1M30S)
    if duration_str.startswith('PT'):
        seconds = 0
        hours_match = re.search(r'(\d+)H', duration_str)
        minutes_match = re.search(r'(\d+)M', duration_str)
        seconds_match = re.search(r'(\d+)S', duration_str)
        
        if hours_match:
            seconds += int(hours_match.group(1)) * 3600
        if minutes_match:
            seconds += int(minutes_match.group(1)) * 60
        if seconds_match:
            seconds += int(seconds_match.group(1))
        
        return seconds
    
    # Handle simple format (1:30, 1:30:00)
    parts = duration_str.split(':')
    if len(parts) == 2:  # MM:SS
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:  # HH:MM:SS
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    
    return 0

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """Extract keywords from text"""
    # Simple keyword extraction - can be enhanced with NLP
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy', 'did', 'does', 'let', 'put', 'say', 'she', 'too', 'use'}
    words = [word for word in words if word not in stop_words]
    
    # Count frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def calculate_engagement_rate(likes: int, comments: int, views: int) -> float:
    """Calculate engagement rate"""
    if views == 0:
        return 0.0
    
    engagement = (likes + comments) / views * 100
    return round(engagement, 2)

def calculate_viral_score(views: int, likes: int, comments: int, shares: int = 0) -> int:
    """Calculate viral score based on engagement metrics"""
    if views == 0:
        return 0
    
    # Weight different engagement types
    weighted_engagement = (likes * 1) + (comments * 5) + (shares * 10)
    engagement_rate = weighted_engagement / views
    
    # Scale to 1-100
    viral_score = min(100, int(engagement_rate * 1000))
    return viral_score

def format_number(num: int) -> str:
    """Format large numbers with K, M, B suffixes"""
    if num < 1000:
        return str(num)
    elif num < 1000000:
        return f"{num/1000:.1f}K"
    elif num < 1000000000:
        return f"{num/1000000:.1f}M"
    else:
        return f"{num/1000000000:.1f}B"

def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL"""
    patterns = [
        r'https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+',
        r'https?://(?:www\.)?youtube\.com/embed/[\w-]+',
        r'https?://youtu\.be/[\w-]+'
    ]
    
    return any(re.match(pattern, url) for pattern in patterns)

def extract_video_id_from_url(url: str) -> Optional[str]:
    """Extract video ID from YouTube URL"""
    patterns = [
        r'youtube\.com/watch\?v=([\w-]+)',
        r'youtube\.com/embed/([\w-]+)',
        r'youtu\.be/([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def safe_json_loads(json_str: str, default: Any = None) -> Any:
    """Safely load JSON string"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return default

def safe_json_dumps(obj: Any, default: str = "{}") -> str:
    """Safely dump object to JSON string"""
    try:
        return json.dumps(obj)
    except (TypeError, ValueError):
        return default

def retry_async(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying async functions"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        await asyncio.sleep(delay * (backoff ** attempt))
                        logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}")
                    else:
                        logger.error(f"All {max_attempts} attempts failed for {func.__name__}: {e}")
            
            raise last_exception
        
        return wrapper
    return decorator

def get_time_range(period: str) -> tuple:
    """Get start and end time for a given period"""
    now = datetime.now()
    
    if period == "today":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == "yesterday":
        start = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = now.replace(hour=0, minute=0, second=0, microsecond=0)
    elif period == "week":
        start = now - timedelta(days=7)
        end = now
    elif period == "month":
        start = now - timedelta(days=30)
        end = now
    elif period == "year":
        start = now - timedelta(days=365)
        end = now
    else:
        start = now - timedelta(days=1)
        end = now
    
    return start, end

def calculate_growth_rate(current: float, previous: float) -> float:
    """Calculate growth rate percentage"""
    if previous == 0:
        return 0.0
    
    growth = ((current - previous) / previous) * 100
    return round(growth, 2)

def is_valid_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_slug(text: str) -> str:
    """Generate URL-friendly slug from text"""
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special characters
    slug = re.sub(r'[\s_-]+', '-', slug)  # Replace spaces and underscores with hyphens
    slug = slug.strip('-')  # Remove leading/trailing hyphens
    
    return slug

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """Merge two dictionaries recursively"""
    result = dict1.copy()
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result

def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split list into chunks"""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary"""
    items = []
    
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    
    return dict(items)

def get_env_bool(key: str, default: bool = False) -> bool:
    """Get boolean value from environment variable"""
    value = os.getenv(key, str(default)).lower()
    return value in ('true', '1', 'yes', 'on')

def get_env_int(key: str, default: int = 0) -> int:
    """Get integer value from environment variable"""
    try:
        return int(os.getenv(key, str(default)))
    except ValueError:
        return default

def get_env_float(key: str, default: float = 0.0) -> float:
    """Get float value from environment variable"""
    try:
        return float(os.getenv(key, str(default)))
    except ValueError:
        return default
