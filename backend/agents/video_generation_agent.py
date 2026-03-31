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
            logger.info(f"🎬 Creating REAL video file at {output_path}")
            logger.info(f"📋 Video plan: {len(video_plan.get('scenes', []))} scenes")
            
            # Create the actual video file
            await self._create_real_video(video_plan, output_path)
            
            logger.info(f"✅ Real video file created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"❌ Error creating video file: {e}")
            raise
    
    async def _create_real_video(self, video_plan: Dict[str, Any], output_path: str):
        """Create a real video file with professional quality"""
        try:
            # Professional video settings
            width, height = 1920, 1080
            
            # Create background colors based on plan
            bg_color = video_plan.get("color_scheme", ["#1a1a1a"])[0]
            bg_color = bg_color.lstrip('#')
            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Enhanced color scheme for professional look
            primary_color = (29, 78, 216)    # Blue
            secondary_color = (255, 255, 255)  # White
            accent_color = (34, 197, 94)       # Green
            
            # Create professional clips for each scene
            clips = []
            temp_files = []
            
            for scene_idx, scene in enumerate(video_plan.get("scenes", [])):
                scene_duration = scene.get("duration", 5)
                text = scene.get("on_screen_text", "")
                voiceover = scene.get("voiceover", "")
                
                # Create professional-looking image for scene
                img = Image.new('RGB', (width, height), primary_color if scene_idx % 2 == 0 else bg_rgb)
                draw = ImageDraw.Draw(img)
                
                # Add gradient effect (simple version)
                for y in range(height):
                    gradient_factor = y / height
                    color = tuple(int(primary_color[i] * (1 - gradient_factor) + bg_rgb[i] * gradient_factor) for i in range(3))
                    draw.line([(0, y), (width, y)], fill=color)
                
                # Add professional text with multiple font sizes
                if text:
                    try:
                        # Try to use a better font (fallback to default if not available)
                        try:
                            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 72)
                            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
                        except:
                            font_large = ImageFont.load_default()
                            font_small = ImageFont.load_default()
                        
                        # Split text into title and subtitle if long
                        if len(text) > 30:
                            title_text = text[:30] + "..."
                            subtitle_text = text[30:60] + "..." if len(text) > 60 else text[30:]
                        else:
                            title_text = text
                            subtitle_text = ""
                        
                        # Draw title
                        title_bbox = draw.textbbox((0, 0), title_text, font=font_large)
                        title_width = title_bbox[2] - title_bbox[0]
                        title_height = title_bbox[3] - title_bbox[1]
                        title_x = (width - title_width) // 2
                        title_y = height // 2 - 100
                        
                        # Add text shadow for better readability
                        draw.text((title_x + 3, title_y + 3), title_text, font=font_large, fill=(0, 0, 0, 128))
                        draw.text((title_x, title_y), title_text, font=font_large, fill=secondary_color)
                        
                        # Draw subtitle if exists
                        if subtitle_text:
                            sub_bbox = draw.textbbox((0, 0), subtitle_text, font=font_small)
                            sub_width = sub_bbox[2] - sub_bbox[0]
                            sub_x = (width - sub_width) // 2
                            sub_y = title_y + title_height + 20
                            
                            draw.text((sub_x + 2, sub_y + 2), subtitle_text, font=font_small, fill=(0, 0, 0, 128))
                            draw.text((sub_x, sub_y), subtitle_text, font=font_small, fill=secondary_color)
                    
                    except Exception as font_error:
                        # Fallback text rendering
                        bbox = draw.textbbox((0, 0), text)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]
                        x = (width - text_width) // 2
                        y = (height - text_height) // 2
                        draw.text((x + 2, y + 2), text, fill=(0, 0, 0))  # Shadow
                        draw.text((x, y), text, fill=secondary_color)
                
                # Save image
                img_path = f"/tmp/scene_{scene.get('scene_number', scene_idx)}.png"
                img.save(img_path)
                temp_files.append(img_path)
                
                # Create video clip from image
                clip = ImageClip(img_path, duration=scene_duration)
                
                # Add fade transitions (removing fade effects for now to fix compatibility)
                clips.append(clip)
            
            # Concatenate clips into final video
            if clips:
                logger.info(f"🎥 Assembling {len(clips)} scenes into final video...")
                
                try:
                    final_clip = concatenate_videoclips(clips)
                    
                    # Write the video file with simple settings that work
                    logger.info(f"🎞️ Writing video file to: {output_path}")
                    final_clip.write_videofile(output_path, fps=24)
                    
                    # Close clips to free memory
                    final_clip.close()
                    for clip in clips:
                        clip.close()
                    
                    logger.info(f"✅ Video file created successfully: {output_path}")
                    
                except Exception as video_error:
                    logger.error(f"MoviePy concatenation error: {video_error}")
                    # Try creating a single scene video as fallback
                    if clips:
                        logger.info("🔄 Trying single scene fallback...")
                        clips[0].write_videofile(output_path, fps=24)
                        clips[0].close()
                        logger.info(f"✅ Single scene video created: {output_path}")
                    else:
                        raise Exception("No clips available for video creation")
                
            # Clean up temporary images
            for img_path in temp_files:
                if os.path.exists(img_path):
                    os.remove(img_path)
                    
        except Exception as e:
            logger.error(f"Error creating real video: {e}")
            raise
                
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
