from typing import Dict, Any, List, Optional
from .base_agent_groq import BaseAgent
from models.video import Script
import logging
import os
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip, TextClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont
import asyncio

logger = logging.getLogger(__name__)

class VideoGenerationAgent(BaseAgent):
    def get_system_prompt(self) -> str:
        return """You are a Video Generation Agent. Convert scripts into engaging faceless videos.

Generate:
- Scene breakdown with visuals
- Voiceover timing
- Background music suggestions
- Subtitle timing
- Transition effects

Constraints:
- Short scenes (5-15 seconds each)
- Fast paced editing
- Engaging visuals
- Clear subtitles
- Professional quality

Output as JSON:
{
    "scenes": [
        {
            "scene_number": 1,
            "duration": 15,
            "visual_type": "stock_footage/animation/text_overlay",
            "visual_description": "Description of visuals",
            "voiceover": "Voiceover text",
            "on_screen_text": "Text to display",
            "background_music": "Music style",
            "transition": "Transition to next scene"
        }
    ],
    "overall_style": "Video style description",
    "color_scheme": ["#FF0000", "#000000"],
    "font_style": "Modern sans-serif",
    "music_suggestions": ["Upbeat tech", "Corporate ambient"]
}"""
    
    async def generate_video_plan(self, script: Script) -> Dict[str, Any]:
        prompt = f"""Create a detailed video production plan for this script:

Title: {script.title}
Hook: {script.hook}
Main Points: {script.main_points}
Conclusion: {script.conclusion}
Call to Action: {script.call_to_action}
Estimated Duration: {script.estimated_duration} seconds

Generate:
1. Scene-by-scene breakdown
2. Visual suggestions for each scene
3. Voiceover timing
4. Background music recommendations
5. Subtitle placement
6. Transition effects

Make it engaging and suitable for faceless YouTube automation."""
        
        try:
            response = self.invoke_llm(prompt)
            return self.parse_response(response)
            
        except Exception as e:
            logger.error(f"Error generating video plan: {e}")
            return self._create_fallback_video_plan(script)
    
    def _create_fallback_video_plan(self, script: Script) -> Dict[str, Any]:
        """Create basic video plan if AI fails"""
        scenes = []
        total_duration = script.estimated_duration
        
        # Create scenes from script parts
        scenes.append({
            "scene_number": 1,
            "duration": 5,
            "visual_type": "text_overlay",
            "visual_description": "Bold text with hook",
            "voiceover": script.hook,
            "on_screen_text": script.hook,
            "background_music": "Upbeat intro",
            "transition": "fade"
        })
        
        for i, point in enumerate(script.main_points):
            scene_duration = (total_duration - 20) // len(script.main_points)
            scenes.append({
                "scene_number": i + 2,
                "duration": scene_duration,
                "visual_type": "stock_footage",
                "visual_description": "Tech/business footage",
                "voiceover": point,
                "on_screen_text": point[:50] + "..." if len(point) > 50 else point,
                "background_music": "Ambient tech",
                "transition": "cut"
            })
        
        scenes.append({
            "scene_number": len(scenes) + 1,
            "duration": 10,
            "visual_type": "text_overlay",
            "visual_description": "Call to action screen",
            "voiceover": script.call_to_action,
            "on_screen_text": "Subscribe for more!",
            "background_music": "Outro music",
            "transition": "fade_out"
        })
        
        return {
            "scenes": scenes,
            "overall_style": "Modern tech presentation",
            "color_scheme": ["#2563eb", "#000000", "#ffffff"],
            "font_style": "Arial Bold",
            "music_suggestions": ["Upbeat tech", "Corporate ambient"]
        }
    
    async def create_video_file(self, video_plan: Dict[str, Any], output_path: str) -> str:
        """Create actual video file from plan"""
        try:
            # This would integrate with video generation services
            # For now, return a placeholder implementation
            logger.info(f"Creating video at {output_path} with plan: {len(video_plan.get('scenes', []))} scenes")
            
            # Placeholder: In real implementation, this would:
            # 1. Generate or fetch stock footage
            # 2. Create text overlays
            # 3. Generate voiceover (using TTS)
            # 4. Add background music
            # 5. Combine everything with transitions
            
            # Create a simple video for demonstration
            await self._create_placeholder_video(video_plan, output_path)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating video file: {e}")
            raise
    
    async def _create_placeholder_video(self, video_plan: Dict[str, Any], output_path: str):
        """Create a placeholder video for testing"""
        try:
            # Create a simple color video with text
            width, height = 1920, 1080
            duration = video_plan.get("scenes", [{}])[0].get("duration", 30)
            
            # Create background
            bg_color = video_plan.get("color_scheme", ["#000000"])[0]
            bg_color = bg_color.lstrip('#')
            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Create clips for each scene
            clips = []
            for scene in video_plan.get("scenes", []):
                # Create image for scene
                img = Image.new('RGB', (width, height), bg_rgb)
                draw = ImageDraw.Draw(img)
                
                # Add text
                text = scene.get("on_screen_text", "")
                if text:
                    # Center text
                    bbox = draw.textbbox((0, 0), text)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (width - text_width) // 2
                    y = (height - text_height) // 2
                    draw.text((x, y), text, fill="white")
                
                # Save image
                img_path = f"/tmp/scene_{scene['scene_number']}.png"
                img.save(img_path)
                
                # Create clip
                clip = ImageClip(img_path, duration=scene.get("duration", 5))
                clips.append(clip)
            
            # Concatenate clips
            if clips:
                final_clip = concatenate_videoclips(clips)
                final_clip.write_videofile(output_path, fps=24, codec='libx264')
                final_clip.close()
            
            # Clean up temporary images
            import glob
            for img_path in glob.glob("/tmp/scene_*.png"):
                os.remove(img_path)
                
        except Exception as e:
            logger.error(f"Error creating placeholder video: {e}")
            raise
    
    def generate_voiceover_script(self, video_plan: Dict[str, Any]) -> str:
        """Generate complete voiceover script"""
        voiceover_parts = []
        
        for scene in video_plan.get("scenes", []):
            voiceover_text = scene.get("voiceover", "")
            if voiceover_text:
                voiceover_parts.append(f"Scene {scene['scene_number']}: {voiceover_text}")
        
        return "\n\n".join(voiceover_parts)
    
    def generate_subtitle_timing(self, video_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate subtitle timing for video"""
        subtitles = []
        current_time = 0
        
        for scene in video_plan.get("scenes", []):
            duration = scene.get("duration", 5)
            text = scene.get("on_screen_text", "")
            
            if text:
                subtitles.append({
                    "start_time": current_time,
                    "end_time": current_time + duration,
                    "text": text
                })
            
            current_time += duration
        
        return subtitles
    
    def get_background_music_suggestions(self, topic: str, tone: str = "energetic") -> List[str]:
        prompt = f"""Suggest background music for YouTube video about: {topic}

Tone: {tone}

Provide 5 music suggestions with:
- Genre/style
- Mood
- Why it works
- Where to find it

Return as JSON list."""
        
        try:
            response = self.invoke_llm(prompt)
            parsed_response = self.parse_response(response)
            
            if isinstance(parsed_response, list):
                return parsed_response
            elif "suggestions" in parsed_response:
                return parsed_response["suggestions"]
            else:
                return []
                
        except Exception as e:
            logger.error(f"Error getting music suggestions: {e}")
            return ["Upbeat corporate music", "Tech ambient", "Motivational instrumental"]
    
    async def optimize_video_for_youtube(self, video_path: str) -> str:
        """Optimize video for YouTube requirements"""
        try:
            # YouTube optimization:
            # - Resolution: 1080p or 4K
            # - Aspect ratio: 16:9
            # - Frame rate: 24-60 fps
            # - Codec: H.264
            # - Audio: AAC
            
            optimized_path = video_path.replace(".mp4", "_optimized.mp4")
            
            # This would use ffmpeg to optimize
            # For now, just return the original path
            logger.info(f"Optimizing video for YouTube: {video_path}")
            
            return video_path
            
        except Exception as e:
            logger.error(f"Error optimizing video: {e}")
            return video_path
