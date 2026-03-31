from typing import Dict, Any, List
from .base_agent_groq import BaseAgent
from models.video import Thumbnail
import logging

logger = logging.getLogger(__name__)

class ThumbnailGeneratorAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a YouTube Thumbnail Expert. Generate 5 clickable thumbnails.

Rules:
- Max 4 words per thumbnail
- High curiosity factor
- High CTR potential
- Bold, readable text
- Eye-catching colors

For each thumbnail provide:
- Thumbnail text (max 4 words)
- Background idea
- Color scheme
- Visual concept
- Emotional appeal

Output as JSON:
{
    "thumbnails": [
        {
            "text": "Thumbnail text",
            "background_idea": "Background description",
            "colors": ["#FF0000", "#000000"],
            "visual_concept": "Visual concept description",
            "emotional_appeal": "curiosity/shock/excitement"
        }
    ]
}"""
    
    async def generate_thumbnails(self, topic: str, title: str) -> Thumbnail:
        prompt = f"""Generate 5 clickable YouTube thumbnails for this video:

Topic: {topic}
Title: {title}

Focus on:
- High click-through rate
- Mobile-friendly design
- Bold, readable text
- Emotional triggers
- Curiosity gaps

Create thumbnails that will stand out in YouTube's feed."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            thumbnail = Thumbnail(
                video_id="",  # Will be set when associated with video
                thumbnail_text=parsed_response.get("thumbnails", [{}])[0].get("text", title[:20]),
                background_idea=parsed_response.get("thumbnails", [{}])[0].get("background_idea", "Abstract tech background"),
                colors=parsed_response.get("thumbnails", [{}])[0].get("colors", ["#FF0000", "#000000"]),
                visual_concept=parsed_response.get("thumbnails", [{}])[0].get("visual_concept", "Bold text on contrasting background"),
                thumbnail_variations=[thumb.get("text", "") for thumb in parsed_response.get("thumbnails", [])]
            )
            
            return thumbnail
            
        except Exception as e:
            logger.error(f"Error generating thumbnails: {e}")
            # Return basic thumbnail if AI fails
            return Thumbnail(
                video_id="",
                thumbnail_text=title[:20],
                background_idea="Tech background",
                colors=["#FF0000", "#000000"],
                visual_concept="Bold text",
                thumbnail_variations=[title[:20]]
            )
    
    def get_thumbnail_trends(self, niche: str) -> List[str]:
        prompt = f"""What are the current thumbnail design trends for {niche} YouTube channels?

Analyze:
- Color schemes that work best
- Font styles
- Image types
- Layout patterns
- Emotional triggers

Return as JSON list of trend descriptions."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "trends" in parsed_response:
                return parsed_response["trends"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting thumbnail trends: {e}")
            return []
    
    def optimize_thumbnail_text(self, title: str, max_words: int = 4) -> str:
        prompt = f"""Optimize this YouTube title for thumbnail text (max {max_words} words):

Title: {title}

Make it:
- Short and punchy
- High curiosity
- Click-worthy
- Easy to read

Return just the optimized text as JSON: {{"text": "Optimized text"}}"""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            return parsed_response.get("text", title.split()[:max_words])
            
        except Exception as e:
            logger.error(f"Error optimizing thumbnail text: {e}")
            return " ".join(title.split()[:max_words])
    
    def generate_color_palette(self, topic: str, emotional_tone: str = "energetic") -> List[str]:
        prompt = f"""Generate a color palette for YouTube thumbnail about: {topic}

Emotional tone: {emotional_tone}

Provide:
- Primary color (bold, attention-grabbing)
- Secondary color (contrast)
- Accent color (highlights)
- Background color

Return as JSON list of hex colors: {{"colors": ["#FF0000", "#000000", "#FFFFFF", "#333333"]}}"""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            return parsed_response.get("colors", ["#FF0000", "#000000", "#FFFFFF", "#333333"])
            
        except Exception as e:
            logger.error(f"Error generating color palette: {e}")
            return ["#FF0000", "#000000", "#FFFFFF", "#333333"]
    
    def analyze_competitor_thumbnails(self, niche: str) -> Dict[str, Any]:
        prompt = f"""Analyze successful thumbnail designs in the {niche} niche:

Identify:
- Common patterns
- Color schemes
- Text placement
- Image styles
- What makes them clickable

Return analysis as JSON with actionable insights."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error analyzing competitor thumbnails: {e}")
            return {}
    
    async def create_thumbnail_spec(self, topic: str, title: str, target_audience: str) -> Dict[str, Any]:
        """Create detailed thumbnail specification for design team"""
        
        # Generate thumbnail variations
        thumbnail = await self.generate_thumbnails(topic, title)
        
        # Get trends
        trends = self.get_thumbnail_trends(topic)
        
        # Generate color palette
        colors = self.generate_color_palette(topic)
        
        spec = {
            "topic": topic,
            "title": title,
            "target_audience": target_audience,
            "main_text": thumbnail.thumbnail_text,
            "variations": thumbnail.thumbnail_variations,
            "background_idea": thumbnail.background_idea,
            "color_palette": colors,
            "visual_concept": thumbnail.visual_concept,
            "trends": trends,
            "design_requirements": {
                "max_words": 4,
                "readability": "high",
                "mobile_optimized": True,
                "contrast_ratio": "high"
            }
        }
        
        return spec
