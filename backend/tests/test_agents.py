import pytest
import asyncio
from unittest.mock import Mock, patch
from agents import (
    TrendResearchAgent, ScriptWritingAgent, ThumbnailGeneratorAgent,
    VideoGenerationAgent, TitleGeneratorAgent, DescriptionGeneratorAgent,
    AnalyticsAgent, MonetizationAgent, DailyAutomationAgent
)
from models import NicheType, VideoIdea, Script, Thumbnail

class TestTrendResearchAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return TrendResearchAgent()
    
    @pytest.mark.asyncio
    async def test_research_trends(self, agent):
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "ideas": [
                    {
                        "title": "10 AI Tools That Will Blow Your Mind",
                        "why_trending": "AI is hot topic",
                        "target_audience": "Tech enthusiasts",
                        "viral_score": 85,
                        "search_demand": "high",
                        "competition_level": "medium"
                    }
                ]
            }'''
            
            ideas = await agent.research_trends(NicheType.AI_TOOLS)
            assert len(ideas) == 1
            assert ideas[0].title == "10 AI Tools That Will Blow Your Mind"
            assert ideas[0].viral_score == 85

class TestScriptWritingAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return ScriptWritingAgent()
    
    @pytest.mark.asyncio
    async def test_write_script(self, agent):
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "title": "AI Tools Guide",
                "hook": "Want to discover amazing AI tools?",
                "intro": "In this video...",
                "main_points": ["Point 1", "Point 2"],
                "conclusion": "Now you know...",
                "call_to_action": "Subscribe for more!",
                "scenes": [],
                "voice_tone": "Energetic",
                "estimated_duration": 90
            }'''
            
            script = await agent.write_script("AI Tools", "beginners")
            assert script.title == "AI Tools Guide"
            assert script.estimated_duration == 90

class TestThumbnailGeneratorAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return ThumbnailGeneratorAgent()
    
    @pytest.mark.asyncio
    async def test_generate_thumbnails(self, agent):
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "thumbnails": [
                    {
                        "text": "AI Tools",
                        "background_idea": "Tech background",
                        "colors": ["#FF0000", "#000000"],
                        "visual_concept": "Modern design"
                    }
                ]
            }'''
            
            thumbnail = await agent.generate_thumbnails("AI Tools", "AI Tools Guide")
            assert thumbnail.thumbnail_text == "AI Tools"
            assert len(thumbnail.colors) == 2

class TestVideoGenerationAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return VideoGenerationAgent()
    
    @pytest.mark.asyncio
    async def test_generate_video_plan(self, agent):
        script = Script(
            video_id="test",
            title="Test Video",
            hook="Test hook",
            intro="Test intro",
            main_points=["Point 1"],
            conclusion="Test conclusion",
            call_to_action="Subscribe",
            scenes=[],
            voice_tone="Energetic",
            estimated_duration=60
        )
        
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "scenes": [
                    {
                        "scene_number": 1,
                        "duration": 15,
                        "visual_type": "text_overlay",
                        "visual_description": "Test scene",
                        "voiceover": "Test voiceover",
                        "on_screen_text": "Test text",
                        "background_music": "Upbeat",
                        "transition": "fade"
                    }
                ],
                "overall_style": "Modern",
                "color_scheme": ["#FF0000", "#000000"],
                "font_style": "Arial",
                "music_suggestions": ["Upbeat tech"]
            }'''
            
            plan = await agent.generate_video_plan(script)
            assert len(plan["scenes"]) == 1
            assert plan["overall_style"] == "Modern"

class TestTitleGeneratorAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return TitleGeneratorAgent()
    
    @pytest.mark.asyncio
    async def test_generate_titles(self, agent):
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "titles": [
                    "10 AI Tools You Need Now",
                    "Best AI Tools for 2024",
                    "AI Tools That Change Everything"
                ]
            }'''
            
            titles = await agent.generate_titles("AI Tools", "beginners")
            assert len(titles) == 3
            assert "AI Tools" in titles[0]

class TestDescriptionGeneratorAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return DescriptionGeneratorAgent()
    
    @pytest.mark.asyncio
    async def test_generate_description(self, agent):
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "description": "Learn about the best AI tools...",
                "tags": ["AI", "tools", "technology"],
                "keywords": ["AI tools", "artificial intelligence"],
                "timestamps": []
            }'''
            
            desc = await agent.generate_description("AI Tools Guide", "AI Tools", ["Point 1", "Point 2"])
            assert "AI tools" in desc["description"]
            assert len(desc["tags"]) == 3

class TestAnalyticsAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return AnalyticsAgent()
    
    @pytest.mark.asyncio
    async def test_analyze_video_performance(self, agent):
        video_data = {
            "title": "Test Video",
            "views": 1000,
            "likes": 50,
            "comments": 10,
            "watch_time": 500,
            "ctr": 5.0,
            "duration": 60
        }
        
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "performance_summary": "Great performance!",
                "success_factors": ["Good title", "Engaging content"],
                "improvement_suggestions": ["Better thumbnail"],
                "next_video_ideas": ["Follow-up content"],
                "trend_insights": ["AI topic trending"],
                "performance_score": 85
            }'''
            
            analysis = await agent.analyze_video_performance(video_data)
            assert analysis["performance_score"] == 85
            assert len(analysis["success_factors"]) == 2

class TestMonetizationAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return MonetizationAgent()
    
    @pytest.mark.asyncio
    async def test_analyze_monetization_potential(self, agent):
        channel_data = {
            "name": "AI Tools Channel",
            "niche": "ai_tools",
            "subscribers": 1000,
            "avg_views": 500,
            "engagement_rate": 5.0
        }
        
        with patch.object(agent, 'invoke_llm') as mock_llm:
            mock_llm.return_value = '''{
                "revenue_ideas": [
                    {
                        "method": "Affiliate Marketing",
                        "potential": "high",
                        "difficulty": "easy",
                        "time_to_results": "1-3months",
                        "min_audience": "500 subscribers",
                        "implementation": "Join affiliate programs",
                        "expected_monthly": "$100-500"
                    }
                ],
                "affiliate_ideas": ["AI software", "Tech gadgets"],
                "sponsor_ideas": ["Tech companies"],
                "product_ideas": ["AI course"]
            }'''
            
            analysis = await agent.analyze_monetization_potential(channel_data)
            assert len(analysis["revenue_ideas"]) == 1
            assert analysis["revenue_ideas"][0]["method"] == "Affiliate Marketing"

class TestDailyAutomationAgent:
    @pytest.fixture
    def agent(self):
        with patch('agents.base_agent.ChatOpenAI'):
            return DailyAutomationAgent()
    
    @pytest.mark.asyncio
    async def test_get_automation_status(self, agent):
        status = await agent.get_automation_status()
        assert status["status"] == "ready"
        assert "total_videos_created" in status

if __name__ == "__main__":
    pytest.main([__file__])
