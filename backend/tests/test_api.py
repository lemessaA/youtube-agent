import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json
from app.main import app

client = TestClient(app)

class TestAPI:
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "running"
        assert "version" in data

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    @patch('app.main.db.insert_channel')
    def test_create_channel(self, mock_insert):
        mock_insert.return_value = {
            "id": "test-id",
            "name": "Test Channel",
            "niche": "ai_tools",
            "description": "Test description",
            "target_audience": "Test audience",
            "created_at": "2024-01-01T00:00:00Z"
        }
        
        channel_data = {
            "name": "Test Channel",
            "niche": "ai_tools",
            "description": "Test description",
            "target_audience": "Test audience"
        }
        
        response = client.post("/channels", json=channel_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Channel"
        assert data["niche"] == "ai_tools"

    @patch('app.main.db.get_channels')
    def test_get_channels(self, mock_get):
        mock_get.return_value = [
            {
                "id": "test-id",
                "name": "Test Channel",
                "niche": "ai_tools",
                "description": "Test description",
                "target_audience": "Test audience",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        response = client.get("/channels")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["name"] == "Test Channel"

    @patch('app.main.db.get_channels')
    def test_get_channel_not_found(self, mock_get):
        mock_get.return_value = []
        
        response = client.get("/channels/nonexistent")
        assert response.status_code == 404

    @patch('app.main.automation_agent.run_daily_automation')
    def test_generate_video_background(self, mock_automation):
        mock_automation.return_value = {"status": "completed"}
        
        request_data = {"channel_id": "test-channel-id"}
        response = client.post("/videos/generate", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "processing"

    @patch('app.main.automation_agent.run_daily_automation')
    async def test_generate_video_sync(self, mock_automation):
        mock_automation.return_value = {
            "status": "completed",
            "video": {"id": "test-video-id", "title": "Test Video"}
        }
        
        request_data = {"channel_id": "test-channel-id"}
        response = client.post("/videos/generate-sync", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"

    @patch('app.main.db.get_videos')
    def test_get_videos(self, mock_get):
        mock_get.return_value = [
            {
                "id": "test-video-id",
                "channel_id": "test-channel-id",
                "title": "Test Video",
                "description": "Test description",
                "tags": ["tag1", "tag2"],
                "duration": 60,
                "status": "completed",
                "created_at": "2024-01-01T00:00:00Z"
            }
        ]
        
        response = client.get("/videos")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Video"

    @patch('app.main.trend_agent.research_trends')
    async def test_research_trends(self, mock_research):
        from models import VideoIdea, NicheType
        
        mock_idea = VideoIdea(
            title="Test AI Tools",
            description="Test description",
            niche=NicheType.AI_TOOLS,
            viral_score=85,
            target_audience="Tech enthusiasts",
            why_trending="AI is trending",
            search_demand="high",
            competition_level="medium"
        )
        mock_research.return_value = [mock_idea]
        
        request_data = {"niche": "ai_tools", "limit": 10}
        response = client.post("/trends/research", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["ideas"]) == 1
        assert data["ideas"][0]["title"] == "Test AI Tools"

    @patch('app.main.trend_agent.get_trending_keywords')
    def test_get_trending_keywords(self, mock_keywords):
        mock_keywords.return_value = ["AI tools", "machine learning", "automation"]
        
        response = client.get("/trends/keywords/ai_tools")
        assert response.status_code == 200
        data = response.json()
        assert len(data["keywords"]) == 3
        assert "AI tools" in data["keywords"]

    @patch('app.main.db.get_videos')
    @patch('app.main.analytics_agent.analyze_video_performance')
    async def test_analyze_video_performance(self, mock_analytics, mock_get_videos):
        mock_get_videos.return_value = [
            {
                "id": "test-video-id",
                "title": "Test Video",
                "views": 1000,
                "likes": 50,
                "comments": 10,
                "watch_time": 500,
                "ctr": 5.0,
                "duration": 60
            }
        ]
        
        mock_analytics.return_value = {
            "performance_summary": "Good performance",
            "performance_score": 80
        }
        
        request_data = {"video_id": "test-video-id"}
        response = client.post("/analytics/video", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert data["performance_score"] == 80

    @patch('app.main.db.get_videos')
    def test_get_channel_analytics_no_videos(self, mock_get):
        mock_get.return_value = []
        
        response = client.get("/analytics/channel/test-channel")
        assert response.status_code == 200
        data = response.json()
        assert "No videos found" in data["message"]

    @patch('app.main.db.get_channels')
    @patch('app.main.db.get_videos')
    @patch('app.main.monetization_agent.analyze_monetization_potential')
    async def test_analyze_monetization(self, mock_monetization, mock_get_videos, mock_get_channels):
        mock_get_channels.return_value = [
            {
                "id": "test-channel-id",
                "name": "Test Channel",
                "niche": "ai_tools"
            }
        ]
        
        mock_get_videos.return_value = [
            {"views": 1000, "likes": 50}
        ]
        
        mock_monetization.return_value = {
            "revenue_ideas": [{"method": "Affiliate Marketing"}],
            "affiliate_ideas": ["AI software"]
        }
        
        request_data = {"channel_id": "test-channel-id"}
        response = client.post("/monetization/analyze", json=request_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data["revenue_ideas"]) == 1

    @patch('app.main.automation_agent.get_automation_status')
    async def test_get_automation_status(self, mock_status):
        mock_status.return_value = {
            "status": "ready",
            "total_videos_created": 10,
            "success_rate": 95.0
        }
        
        response = client.get("/automation/status")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ready"
        assert data["total_videos_created"] == 10

    @patch('app.main.db.get_channels')
    def test_run_daily_automation_no_channels(self, mock_get):
        mock_get.return_value = []
        
        response = client.post("/automation/run-daily")
        assert response.status_code == 200
        data = response.json()
        assert "No channels found" in data["message"]

    @patch('app.main.db.get_channels')
    @patch('app.main.automation_agent.run_daily_automation')
    def test_run_daily_automation_with_channels(self, mock_automation, mock_get):
        mock_get.return_value = [
            {"id": "test-channel-1"},
            {"id": "test-channel-2"}
        ]
        
        mock_automation.return_value = {"status": "completed"}
        
        response = client.post("/automation/run-daily")
        assert response.status_code == 200
        data = response.json()
        assert data["channels"] == 2

    @patch('app.main.db.get_video_ideas')
    def test_get_video_ideas(self, mock_get):
        mock_get.return_value = [
            {
                "id": "test-idea-id",
                "title": "Test Video Idea",
                "viral_score": 85,
                "niche": "ai_tools"
            }
        ]
        
        response = client.get("/ideas")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Video Idea"

if __name__ == "__main__":
    pytest.main([__file__])
