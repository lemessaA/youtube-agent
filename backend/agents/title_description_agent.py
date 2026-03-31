from typing import Dict, Any, List
from .base_agent_groq import BaseAgent
import logging

logger = logging.getLogger(__name__)

class TitleGeneratorAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are YouTube SEO expert. Generate viral video titles.

Rules:
- High CTR (Click-Through Rate)
- Short titles (under 60 characters)
- Create curiosity
- Use power words
- Include keywords
- Mobile-friendly

Title patterns that work:
1. "How to [Achieve Result] in [Time]"
2. "[Number] [Topic] Secrets"
3. "You Won't Believe [Shocking Thing]"
4. "[Topic] for Beginners"
5. "The Ultimate [Topic] Guide"

Output as JSON list of 10 titles:
{
    "titles": [
        "Title 1",
        "Title 2",
        ...
    ]
}"""
    
    async def generate_titles(self, topic: str, target_audience: str = "beginners") -> List[str]:
        prompt = f"""Generate 10 viral YouTube titles for this video:

Topic: {topic}
Target Audience: {target_audience}

Focus on:
- High click-through rate
- Curiosity gaps
- SEO keywords
- Mobile display (under 60 chars)
- Emotional triggers

Make each title compelling and clickable."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, dict) and "titles" in parsed_response:
                return parsed_response["titles"]
            elif isinstance(parsed_response, list):
                return parsed_response
            else:
                return [f"How to {topic}", f"{topic} Guide", f"Learn {topic}"]
                
        except Exception as e:
            logger.error(f"Error generating titles: {e}")
            return [f"How to {topic}", f"{topic} Tutorial", f"Learn {topic} Fast"]
    
    def optimize_title_for_seo(self, title: str, keywords: List[str]) -> str:
        prompt = f"""Optimize this YouTube title for SEO:

Title: {title}
Keywords: {', '.join(keywords)}

Make it:
- More searchable
- Higher CTR
- Under 60 characters
- Include main keyword naturally

Return optimized title as JSON: {{"title": "Optimized title"}}"""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            return parsed_response.get("title", title)
            
        except Exception as e:
            logger.error(f"Error optimizing title: {e}")
            return title
    
    def score_title_potential(self, title: str) -> Dict[str, Any]:
        prompt = f"""Score this YouTube title for viral potential:

Title: {title}

Rate each factor 1-100:
- Click-through rate potential
- SEO strength
- Curiosity factor
- Shareability
- Mobile readability

Return as JSON with scores and overall score."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error scoring title: {e}")
            return {"overall_score": 50}

class DescriptionGeneratorAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are YouTube description generator. Create engaging, SEO-optimized descriptions.

Structure:
1. Hook (first 2 lines - show in preview)
2. Video summary
3. Key points/timestamps
4. Call to action
5. Affiliate links placeholder
6. Social media links
7. Hashtags

Include:
- SEO keywords naturally
- Timestamps for longer videos
- Affiliate product placeholders
- Social media handles
- Relevant hashtags

Output as JSON:
{
    "description": "Full description text",
    "tags": ["tag1", "tag2", ...],
    "keywords": ["keyword1", "keyword2", ...],
    "timestamps": [{"time": "0:00", "title": "Introduction"}]
}"""
    
    async def generate_description(self, title: str, topic: str, script_points: List[str]) -> Dict[str, Any]:
        prompt = f"""Generate YouTube description for this video:

Title: {title}
Topic: {topic}
Key Points: {', '.join(script_points)}

Create:
1. Compelling first 2 lines (shows in preview)
2. Detailed video summary
3. Timestamps for each section
4. Call to action
5. Affiliate link placeholders
6. Relevant hashtags
7. SEO keywords

Make it engaging and optimized for YouTube search."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error generating description: {e}")
            return self._create_fallback_description(title, topic, script_points)
    
    def _create_fallback_description(self, title: str, topic: str, script_points: List[str]) -> Dict[str, Any]:
        """Create basic description if AI fails"""
        description = f"""Learn all about {topic} in this comprehensive guide!

In this video, we cover:
{chr(10).join([f"• {point}" for point in script_points])}

🔔 Subscribe for more content on {topic}!
👍 Like if you found this helpful!

#YouTube #{topic.replace(' ', '')} #Tutorial

---
AFFILIATE DISCLOSURE:
[Insert relevant affiliate links here]

SOCIAL MEDIA:
Twitter: @[yourhandle]
Instagram: @[yourhandle]
"""
        
        return {
            "description": description,
            "tags": [topic, "tutorial", "how to", "guide", "learn"],
            "keywords": [topic, "tutorial", "guide", "how to"],
            "timestamps": []
        }
    
    def generate_tags(self, topic: str, title: str, niche: str) -> List[str]:
        prompt = f"""Generate 15 YouTube tags for this video:

Topic: {topic}
Title: {title}
Niche: {niche}

Include:
- Broad tags
- Specific tags
- Long-tail tags
- Competitor tags
- Trending tags

Return as JSON list of tags."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "tags" in parsed_response:
                return parsed_response["tags"]
            else:
                return [topic, niche, "tutorial", "how to"]
                
        except Exception as e:
            logger.error(f"Error generating tags: {e}")
            return [topic, niche, "tutorial", "guide", "learn"]
    
    def create_timestamps(self, script_points: List[str], estimated_duration: int) -> List[Dict[str, str]]:
        """Generate timestamps for video sections"""
        timestamps = []
        current_time = 0
        
        # Add intro
        timestamps.append({"time": "0:00", "title": "Introduction"})
        current_time += 10
        
        # Add main points
        if script_points:
            duration_per_point = (estimated_duration - 30) // len(script_points)
            for i, point in enumerate(script_points):
                minutes = current_time // 60
                seconds = current_time % 60
                timestamps.append({
                    "time": f"{minutes}:{seconds:02d}",
                    "title": point[:30] + "..." if len(point) > 30 else point
                })
                current_time += duration_per_point
        
        # Add outro
        minutes = current_time // 60
        seconds = current_time % 60
        timestamps.append({"time": f"{minutes}:{seconds:02d}", "title": "Conclusion"})
        
        return timestamps
    
    def optimize_for_search(self, description: str, keywords: List[str]) -> str:
        prompt = f"""Optimize this YouTube description for search:

Description: {description}
Target Keywords: {', '.join(keywords)}

Make it more SEO-friendly by:
- Naturally including keywords
- Adding relevant terms
- Improving readability
- Maintaining engagement

Return optimized description."""
        
        try:
            response = self.invoke_llm(prompt)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error optimizing description: {e}")
            return description
