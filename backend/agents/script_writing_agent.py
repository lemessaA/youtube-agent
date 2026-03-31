from typing import Dict, Any, List
from .base_agent_groq import BaseAgent
from models.video import Script
import logging

logger = logging.getLogger(__name__)

class ScriptWritingAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a professional YouTube script writer. Write short YouTube scripts.

Video Length: 60-120 seconds

Structure:
1. Hook (first 5 seconds) - Must grab attention immediately
2. Intro (10-15 seconds) - Brief setup
3. Main Points (30-60 seconds) - 2-3 key points
4. Conclusion (10-15 seconds) - Summary
5. Call to action (5-10 seconds) - Subscribe, like, comment

Tone:
- Simple and clear
- Engaging and energetic
- Fast paced but not rushed
- Conversational

Guidelines:
- Use short sentences
- Include visual cues for each scene
- Add timing for each section
- Make it beginner-friendly
- Include specific examples

Output as JSON:
{
    "title": "Catchy video title",
    "hook": "Attention-grabbing opening line",
    "intro": "Brief introduction",
    "main_points": ["Point 1", "Point 2", "Point 3"],
    "conclusion": "Summary and wrap-up",
    "call_to_action": "Subscribe/like/comment prompt",
    "scenes": [
        {
            "scene_number": 1,
            "visual": "Visual description",
            "duration": 15,
            "text": "Script text for this scene"
        }
    ],
    "voice_tone": "Energetic and friendly",
    "estimated_duration": 90
}"""
    
    async def write_script(self, topic: str, target_audience: str = "beginners") -> Script:
        prompt = f"""Write a YouTube script for this topic: "{topic}"

Target audience: {target_audience}
Video length: 60-120 seconds
Style: Faceless automation with stock footage/text overlays

Create an engaging script that will perform well on YouTube shorts and regular videos."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            script = Script(
                video_id="",  # Will be set when associated with video
                title=parsed_response.get("title", topic),
                hook=parsed_response.get("hook", ""),
                intro=parsed_response.get("intro", ""),
                main_points=parsed_response.get("main_points", []),
                conclusion=parsed_response.get("conclusion", ""),
                call_to_action=parsed_response.get("call_to_action", ""),
                scenes=parsed_response.get("scenes", []),
                voice_tone=parsed_response.get("voice_tone", "Energetic and friendly"),
                estimated_duration=parsed_response.get("estimated_duration", 90)
            )
            
            return script
            
        except Exception as e:
            logger.error(f"Error writing script: {e}")
            # Return basic script if AI fails
            return Script(
                video_id="",
                title=topic,
                hook=f"Want to learn about {topic}?",
                intro=f"In this video, I'll show you everything about {topic}.",
                main_points=[f"Key point 1 about {topic}", f"Key point 2 about {topic}"],
                conclusion=f"Now you know the basics of {topic}.",
                call_to_action="Like and subscribe for more content!",
                scenes=[],
                voice_tone="Friendly",
                estimated_duration=60
            )
    
    def optimize_script_for_engagement(self, script: Script) -> Script:
        prompt = f"""Optimize this YouTube script for maximum engagement:

Title: {script.title}
Hook: {script.hook}
Main Points: {script.main_points}

Make it more:
- Engaging in the first 5 seconds
- Shareable
- Comment-worthy
- Retention-focused

Return optimized script as JSON with same structure."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            # Update script with optimized content
            if "hook" in parsed_response:
                script.hook = parsed_response["hook"]
            if "main_points" in parsed_response:
                script.main_points = parsed_response["main_points"]
            if "call_to_action" in parsed_response:
                script.call_to_action = parsed_response["call_to_action"]
            
            return script
            
        except Exception as e:
            logger.error(f"Error optimizing script: {e}")
            return script
    
    def generate_scene_breakdown(self, script_text: str, estimated_duration: int) -> List[Dict[str, Any]]:
        prompt = f"""Create a scene breakdown for this YouTube script:

Script: {script_text}
Duration: {estimated_duration} seconds

Break it into 4-6 scenes with:
1. Scene number
2. Visual description (stock footage type, text overlays, animations)
3. Duration for each scene
4. Script text for that scene
5. Visual effects suggestions

Return as JSON list of scenes."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "scenes" in parsed_response:
                return parsed_response["scenes"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error generating scene breakdown: {e}")
            return []
    
    def add_timing_cues(self, script: Script) -> Script:
        """Add timing cues to script for voiceover recording"""
        total_duration = script.estimated_duration
        
        # Distribute timing across sections
        hook_duration = 5
        intro_duration = 10
        cta_duration = 10
        remaining_duration = total_duration - hook_duration - intro_duration - cta_duration
        
        main_points_duration = remaining_duration // len(script.main_points) if script.main_points else remaining_duration
        
        timing_script = f"""
[0:00-0:05] HOOK: {script.hook}
[0:05-0:15] INTRO: {script.intro}
"""
        
        current_time = 15
        for i, point in enumerate(script.main_points):
            end_time = current_time + main_points_duration
            timing_script += f"[{current_time//60}:{current_time%60:02d}-{end_time//60}:{end_time%60:02d}] POINT {i+1}: {point}\n"
            current_time = end_time
        
        timing_script += f"[{current_time//60}:{current_time%60:02d}-{total_duration//60}:{total_duration%60:02d}] CTA: {script.call_to_action}"
        
        # Store timing info in scenes
        script.scenes = [{"timing_cue": timing_script}]
        
        return script
