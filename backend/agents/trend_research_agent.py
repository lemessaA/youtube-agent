from typing import Dict, Any, List
from .base_agent_groq import BaseAgent
from models.video import NicheType, VideoIdea, TrendingTopic
import requests
import json
import logging

logger = logging.getLogger(__name__)

class TrendResearchAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a YouTube Trend Research Agent. Your job is to find trending YouTube video ideas.

Focus niches:
- AI tools
- Startup ideas
- Make money online
- Tech explainers
- Side hustles

Generate 10 trending ideas. For each idea provide:
- Title
- Why trending
- Target audience
- Viral score (1-100)

Constraints:
- High search demand
- Low competition
- Beginner friendly

Output format as JSON:
{
    "ideas": [
        {
            "title": "Title here",
            "why_trending": "Why it's trending",
            "target_audience": "Target audience",
            "viral_score": 85,
            "search_demand": "high/medium/low",
            "competition_level": "low/medium/high"
        }
    ]
}"""
    
    async def research_trends(self, niche: NicheType) -> List[VideoIdea]:
        prompt = f"""Research trending YouTube video ideas for the {niche.value} niche.

Focus on:
1. Current trending topics in this niche
2. What's popular on YouTube right now
3. What people are searching for
4. Topics with high engagement but low competition

Generate 10 video ideas with viral potential."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            video_ideas = []
            if "ideas" in parsed_response:
                for idea_data in parsed_response["ideas"]:
                    video_idea = VideoIdea(
                        title=idea_data.get("title", ""),
                        description=idea_data.get("why_trending", ""),
                        niche=niche,
                        viral_score=idea_data.get("viral_score", 50),
                        target_audience=idea_data.get("target_audience", ""),
                        why_trending=idea_data.get("why_trending", ""),
                        search_demand=idea_data.get("search_demand", "medium"),
                        competition_level=idea_data.get("competition_level", "medium")
                    )
                    video_ideas.append(video_idea)
            
            return video_ideas
            
        except Exception as e:
            logger.error(f"Error researching trends: {e}")
            return []
    
    def get_trending_keywords(self, niche: str) -> List[str]:
        prompt = f"""Generate 20 trending keywords and search terms for the {niche} niche on YouTube.

Focus on:
- High volume search terms
- Currently trending topics
- Keywords with good monetization potential
- Terms beginners would search for

Return as JSON list of strings."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif isinstance(parsed_response, dict) and "keywords" in parsed_response:
                return parsed_response["keywords"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting trending keywords: {e}")
            return []
    
    def analyze_competition(self, topic: str) -> Dict[str, Any]:
        prompt = f"""Analyze the competition level for this YouTube topic: "{topic}"

Provide analysis on:
1. How many videos exist on this topic
2. Average views for similar videos
3. Competition level (low/medium/high)
4. Difficulty ranking for new creators
5. Monetization potential

Return as JSON with detailed analysis."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error analyzing competition: {e}")
            return {}
    
    def get_viral_potential_score(self, title: str, description: str) -> int:
        prompt = f"""Rate the viral potential of this YouTube video idea:

Title: {title}
Description: {description}

Score from 1-100 based on:
- Clickbait potential
- Trend alignment
- Audience interest
- Shareability
- Search demand

Return just the number as JSON: {{"score": 85}}"""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            return parsed_response.get("score", 50)
            
        except Exception as e:
            logger.error(f"Error scoring viral potential: {e}")
            return 50
