import os
import logging
from typing import Dict, Any, List, Optional, Tuple
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import *
import tempfile
import json

logger = logging.getLogger(__name__)

class VideoProcessor:
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        
    def create_text_overlay_video(self, text: str, duration: int, output_path: str, 
                               background_color: str = "#000000", text_color: str = "#FFFFFF",
                               font_size: int = 60) -> str:
        """Create a simple video with text overlay"""
        try:
            # Video settings
            width, height = 1920, 1080
            fps = 24
            
            # Create background
            bg_color = background_color.lstrip('#')
            bg_rgb = tuple(int(bg_color[i:i+2], 16) for i in (0, 2, 4))
            
            # Create image with text
            img = Image.new('RGB', (width, height), bg_rgb)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font, fallback to default if not available
            try:
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position (center)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Draw text
            draw.text((x, y), text, fill=text_color, font=font)
            
            # Save temporary image
            temp_img_path = os.path.join(self.temp_dir, "temp_frame.png")
            img.save(temp_img_path)
            
            # Create video from image
            clip = ImageClip(temp_img_path, duration=duration)
            clip.write_videofile(output_path, fps=fps)
            clip.close()
            
            # Clean up
            if os.path.exists(temp_img_path):
                os.remove(temp_img_path)
            
            logger.info(f"Text overlay video created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating text overlay video: {e}")
            raise
    
    def create_scene_video(self, scenes: List[Dict[str, Any]], output_path: str) -> str:
        """Create video from multiple scenes"""
        try:
            clips = []
            
            for i, scene in enumerate(scenes):
                scene_duration = scene.get('duration', 5)
                text = scene.get('on_screen_text', '')
                visual_type = scene.get('visual_type', 'text_overlay')
                
                # Create clip based on visual type
                if visual_type == 'text_overlay':
                    clip_path = os.path.join(self.temp_dir, f"scene_{i}.mp4")
                    self.create_text_overlay_video(
                        text=text,
                        duration=scene_duration,
                        output_path=clip_path
                    )
                    clip = VideoFileClip(clip_path)
                else:
                    # For other types, create a simple text overlay as fallback
                    clip_path = os.path.join(self.temp_dir, f"scene_{i}.mp4")
                    self.create_text_overlay_video(
                        text=text,
                        duration=scene_duration,
                        output_path=clip_path
                    )
                    clip = VideoFileClip(clip_path)
                
                clips.append(clip)
            
            # Concatenate all clips
            if clips:
                final_clip = concatenate_videoclips(clips)
                final_clip.write_videofile(output_path, fps=24)
                final_clip.close()
                
                # Clean up temporary clips
                for clip in clips:
                    clip.close()
                    clip_path = os.path.join(self.temp_dir, f"scene_{clips.index(clip)}.mp4")
                    if os.path.exists(clip_path):
                        os.remove(clip_path)
            
            logger.info(f"Scene video created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating scene video: {e}")
            raise
    
    def add_audio_to_video(self, video_path: str, audio_path: str, output_path: str) -> str:
        """Add audio track to video"""
        try:
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)
            
            # Trim or loop audio to match video duration
            if audio.duration < video.duration:
                # Loop audio
                audio = audio.loop(duration=video.duration)
            elif audio.duration > video.duration:
                # Trim audio
                audio = audio.subclip(0, video.duration)
            
            # Add audio to video
            final_video = video.set_audio(audio)
            final_video.write_videofile(output_path, fps=24)
            
            # Clean up
            video.close()
            audio.close()
            final_video.close()
            
            logger.info(f"Audio added to video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adding audio to video: {e}")
            raise
    
    def create_thumbnail_from_frame(self, video_path: str, output_path: str, 
                                  timestamp: float = 1.0) -> str:
        """Extract thumbnail from video frame"""
        try:
            video = VideoFileClip(video_path)
            
            # Get frame at timestamp
            frame = video.get_frame(timestamp)
            
            # Convert to PIL Image
            img = Image.fromarray(frame)
            img.save(output_path)
            
            video.close()
            
            logger.info(f"Thumbnail created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating thumbnail: {e}")
            raise
    
    def optimize_video_for_youtube(self, input_path: str, output_path: str) -> str:
        """Optimize video for YouTube requirements"""
        try:
            video = VideoFileClip(input_path)
            
            # YouTube optimization settings
            # Resolution: 1080p (1920x1080)
            # Frame rate: 24-30 fps
            # Codec: H.264
            
            # Resize if necessary
            if video.size != (1920, 1080):
                video = video.resize((1920, 1080))
            
            # Write optimized video
            video.write_videofile(
                output_path,
                fps=24,
                codec='libx264',
                audio_codec='aac',
                bitrate='4000k'
            )
            
            video.close()
            
            logger.info(f"Video optimized for YouTube: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error optimizing video: {e}")
            raise
    
    def add_subtitles(self, video_path: str, subtitles: List[Dict[str, Any]], 
                     output_path: str, font_size: int = 48) -> str:
        """Add subtitles to video"""
        try:
            video = VideoFileClip(video_path)
            
            # Create subtitle clips
            subtitle_clips = []
            
            for subtitle in subtitles:
                start_time = subtitle.get('start_time', 0)
                end_time = subtitle.get('end_time', 5)
                text = subtitle.get('text', '')
                
                # Create text clip
                txt_clip = TextClip(
                    text,
                    fontsize=font_size,
                    color='white',
                    font='Arial',
                    stroke_color='black',
                    stroke_width=2
                ).set_position(('center', 'bottom')).set_start(start_time).set_end(end_time)
                
                subtitle_clips.append(txt_clip)
            
            # Composite video with subtitles
            final_video = CompositeVideoClip([video] + subtitle_clips)
            final_video.write_videofile(output_path, fps=24)
            
            # Clean up
            video.close()
            final_video.close()
            for clip in subtitle_clips:
                clip.close()
            
            logger.info(f"Subtitles added to video: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error adding subtitles: {e}")
            raise
    
    def create_video_from_images(self, image_paths: List[str], output_path: str, 
                               duration_per_image: float = 3.0) -> str:
        """Create video from sequence of images"""
        try:
            clips = []
            
            for img_path in image_paths:
                if os.path.exists(img_path):
                    clip = ImageClip(img_path, duration=duration_per_image)
                    clips.append(clip)
            
            if clips:
                final_clip = concatenate_videoclips(clips)
                final_clip.write_videofile(output_path, fps=24)
                final_clip.close()
                
                # Clean up
                for clip in clips:
                    clip.close()
            
            logger.info(f"Video created from images: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating video from images: {e}")
            raise
    
    def get_video_info(self, video_path: str) -> Dict[str, Any]:
        """Get video information"""
        try:
            video = VideoFileClip(video_path)
            
            info = {
                'duration': video.duration,
                'fps': video.fps,
                'size': video.size,
                'width': video.size[0],
                'height': video.size[1],
                'has_audio': video.audio is not None
            }
            
            video.close()
            return info
            
        except Exception as e:
            logger.error(f"Error getting video info: {e}")
            return {}
    
    def trim_video(self, input_path: str, output_path: str, start_time: float, end_time: float) -> str:
        """Trim video to specific duration"""
        try:
            video = VideoFileClip(input_path)
            
            # Trim video
            trimmed_video = video.subclip(start_time, end_time)
            trimmed_video.write_videofile(output_path, fps=24)
            
            # Clean up
            video.close()
            trimmed_video.close()
            
            logger.info(f"Video trimmed: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error trimming video: {e}")
            raise

# Global video processor instance
video_processor = VideoProcessor()
