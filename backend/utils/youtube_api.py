import os
import logging
from typing import Dict, Any, List, Optional
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import io
import json

logger = logging.getLogger(__name__)

class YouTubeAPI:
    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        self.client_secrets_file = 'client_secrets.json'
        self.credentials_file = 'youtube_credentials.json'
        self.youtube = None
        
        if self.api_key:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def authenticate(self):
        """Authenticate with YouTube API"""
        try:
            creds = None
            
            # Check if we have existing credentials
            if os.path.exists(self.credentials_file):
                creds = Credentials.from_authorized_user_file(self.credentials_file, self.scopes)
            
            # If there are no (valid) credentials available, let the user log in
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    if not os.path.exists(self.client_secrets_file):
                        raise FileNotFoundError("client_secrets.json not found. Please download from Google Cloud Console.")
                    
                    flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.scopes)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open(self.credentials_file, 'w') as token:
                    token.write(creds.to_json())
            
            # Build the service object
            self.youtube = build('youtube', 'v3', credentials=creds)
            logger.info("YouTube API authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"YouTube API authentication failed: {e}")
            return False
    
    def upload_video(self, video_path: str, title: str, description: str, tags: List[str], category_id: str = "22") -> Optional[str]:
        """Upload video to YouTube"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return None
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags,
                    'categoryId': category_id
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False
                }
            }
            
            # Create MediaFileUpload object
            media = MediaIoBaseUpload(
                io.FileIO(video_path, 'rb'),
                mimetype='video/*',
                resumable=True
            )
            
            # Call the API's videos.insert method to create and upload the video
            request = self.youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            logger.info(f"Starting video upload: {title}")
            
            # Upload the video
            response = request.execute()
            video_id = response['id']
            
            logger.info(f"Video uploaded successfully! Video ID: {video_id}")
            return video_id
            
        except Exception as e:
            logger.error(f"Error uploading video: {e}")
            return None
    
    def update_video_metadata(self, video_id: str, title: str = None, description: str = None, tags: List[str] = None) -> bool:
        """Update video metadata"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return False
            
            # Get current video details
            video_response = self.youtube.videos().list(
                part='snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                logger.error(f"Video not found: {video_id}")
                return False
            
            # Update snippet
            snippet = video_response['items'][0]['snippet']
            
            if title:
                snippet['title'] = title
            if description:
                snippet['description'] = description
            if tags:
                snippet['tags'] = tags
            
            # Update the video
            self.youtube.videos().update(
                part='snippet',
                body={
                    'id': video_id,
                    'snippet': snippet
                }
            ).execute()
            
            logger.info(f"Video metadata updated: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating video metadata: {e}")
            return False
    
    def get_video_analytics(self, video_id: str) -> Optional[Dict[str, Any]]:
        """Get video analytics"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return None
            
            # Get video statistics
            video_response = self.youtube.videos().list(
                part='statistics,snippet',
                id=video_id
            ).execute()
            
            if not video_response['items']:
                logger.error(f"Video not found: {video_id}")
                return None
            
            video = video_response['items'][0]
            stats = video.get('statistics', {})
            snippet = video.get('snippet', {})
            
            analytics = {
                'video_id': video_id,
                'title': snippet.get('title', ''),
                'views': int(stats.get('viewCount', 0)),
                'likes': int(stats.get('likeCount', 0)),
                'comments': int(stats.get('commentCount', 0)),
                'published_at': snippet.get('publishedAt', ''),
                'duration': video.get('contentDetails', {}).get('duration', '')
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting video analytics: {e}")
            return None
    
    def get_channel_analytics(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get channel analytics"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return None
            
            # Get channel statistics
            channel_response = self.youtube.channels().list(
                part='statistics,snippet',
                id=channel_id
            ).execute()
            
            if not channel_response['items']:
                logger.error(f"Channel not found: {channel_id}")
                return None
            
            channel = channel_response['items'][0]
            stats = channel.get('statistics', {})
            snippet = channel.get('snippet', {})
            
            analytics = {
                'channel_id': channel_id,
                'title': snippet.get('title', ''),
                'subscribers': int(stats.get('subscriberCount', 0)),
                'total_views': int(stats.get('viewCount', 0)),
                'total_videos': int(stats.get('videoCount', 0)),
                'description': snippet.get('description', '')
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting channel analytics: {e}")
            return None
    
    def search_trending_videos(self, niche: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for trending videos in a niche"""
        try:
            if not self.youtube and not self.api_key:
                logger.error("YouTube API not initialized")
                return []
            
            # Search for videos
            search_response = self.youtube.search().list(
                part='snippet',
                q=niche,
                type='video',
                order='viewCount',
                maxResults=max_results,
                publishedAfter='2024-01-01T00:00:00Z'
            ).execute()
            
            videos = []
            for item in search_response['items']:
                video_data = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'channel_title': item['snippet']['channelTitle'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_data)
            
            logger.info(f"Found {len(videos)} trending videos for niche: {niche}")
            return videos
            
        except Exception as e:
            logger.error(f"Error searching trending videos: {e}")
            return []
    
    def get_trending_topics(self, region_code: str = 'US', max_results: int = 10) -> List[Dict[str, Any]]:
        """Get trending topics from YouTube"""
        try:
            if not self.youtube and not self.api_key:
                logger.error("YouTube API not initialized")
                return []
            
            # Get trending videos
            trending_response = self.youtube.videos().list(
                part='snippet,statistics',
                chart='mostPopular',
                regionCode=region_code,
                maxResults=max_results,
                categoryId='22'  # Technology category
            ).execute()
            
            topics = []
            for item in trending_response['items']:
                topic_data = {
                    'video_id': item['id'],
                    'title': item['snippet']['title'],
                    'tags': item['snippet'].get('tags', []),
                    'views': int(item['statistics'].get('viewCount', 0)),
                    'likes': int(item['statistics'].get('likeCount', 0)),
                    'comments': int(item['statistics'].get('commentCount', 0))
                }
                topics.append(topic_data)
            
            logger.info(f"Retrieved {len(topics)} trending topics")
            return topics
            
        except Exception as e:
            logger.error(f"Error getting trending topics: {e}")
            return []
    
    def delete_video(self, video_id: str) -> bool:
        """Delete a video"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return False
            
            self.youtube.videos().delete(id=video_id).execute()
            logger.info(f"Video deleted: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error deleting video: {e}")
            return False
    
    def add_video_to_playlist(self, video_id: str, playlist_id: str) -> bool:
        """Add video to playlist"""
        try:
            if not self.youtube:
                if not self.authenticate():
                    return False
            
            self.youtube.playlistItems().insert(
                part='snippet',
                body={
                    'snippet': {
                        'playlistId': playlist_id,
                        'resourceId': {
                            'kind': 'youtube#video',
                            'videoId': video_id
                        }
                    }
                }
            ).execute()
            
            logger.info(f"Video added to playlist: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding video to playlist: {e}")
            return False

# Global YouTube API instance
youtube_api = YouTubeAPI()
