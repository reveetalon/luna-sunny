"""
AI-Powered Visual Generation Service
Integrates with media generation tools to create educational visual assets
"""

import os
import json
import hashlib
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

# Import the media generation models from our pipeline
from src.models.media_generator import (
    VisualGenerator, VisualStyle, VisualAsset,
    AudioGenerator, AudioStyle, AudioAsset,
    VideoAssembler
)

class MediaGenerationService:
    """Service for generating visual and audio assets using AI tools"""

    def __init__(self, assets_dir: str = None):
        if assets_dir is None:
            assets_dir = os.path.join(os.getcwd(), "generated-assets")
        self.assets_dir = assets_dir
        self.visual_generator = VisualGenerator()
        self.audio_generator = AudioGenerator()
        self.video_assembler = VideoAssembler()
        # Create asset directories
        self._create_asset_directories()
    
    def _create_asset_directories(self):
        """Create directory structure for generated assets"""
        directories = [
            f"{self.assets_dir}/characters",
            f"{self.assets_dir}/backgrounds", 
            f"{self.assets_dir}/objects",
            f"{self.assets_dir}/text",
            f"{self.assets_dir}/audio/music",
            f"{self.assets_dir}/audio/voice",
            f"{self.assets_dir}/audio/effects",
            f"{self.assets_dir}/videos",
            f"{self.assets_dir}/thumbnails"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_character_image(self, character_name: str, style: VisualStyle, 
                                age_group: str, expression: str = "happy") -> VisualAsset:
        """Generate character image using AI image generation"""
        
        # Build detailed prompt for character generation
        character_info = self.visual_generator.character_library.get(character_name, {})
        style_info = self.visual_generator.style_templates.get(style, {})
        
        prompt = f"""
        Create a high-quality {style.value} illustration of {character_name}, a friendly {character_info.get('type', 'child')} character for educational children's content.
        
        Character Details:
        - Age: {character_info.get('age', age_group)}
        - Personality: {character_info.get('personality', 'friendly and curious')}
        - Appearance: {character_info.get('appearance', 'cheerful child')}
        - Expression: {expression}
        - Target audience: {age_group} children
        
        Visual Style:
        - Style: {style.value}
        - Color palette: {', '.join(style_info.get('color_palette', ['bright', 'cheerful']))}
        - Mood: {', '.join(style_info.get('style_keywords', ['friendly', 'educational']))}
        - Brightness: {style_info.get('brightness', 'medium')}
        
        Requirements:
        - Child-friendly and engaging
        - Clear, simple design suitable for educational videos
        - High contrast for visibility
        - Professional illustration quality
        - Suitable for animation and video use
        - Safe and appropriate for young children
        """
        
        # Generate unique filename
        file_hash = hashlib.md5(f"{character_name}_{style.value}_{expression}_{age_group}".encode()).hexdigest()[:8]
        file_path = f"{self.assets_dir}/characters/{character_name}_{style.value}_{expression}_{file_hash}.png"
        
        # Use media generation tool to create image
        try:
            from src.utils.media_tools import generate_image
            generate_image(prompt, file_path, aspect_ratio="square")
        except ImportError:
            # Fallback: create placeholder or use mock generation
            self._create_placeholder_image(file_path, f"{character_name} Character")
        
        # Create asset metadata
        asset = VisualAsset(
            asset_id=f"char_{character_name}_{style.value}_{file_hash}",
            asset_type="character",
            description=f"{character_name} character in {style.value} style with {expression} expression",
            style=style,
            file_path=file_path,
            metadata={
                "character_name": character_name,
                "expression": expression,
                "age_group": age_group,
                "generation_prompt": prompt.strip(),
                "generation_timestamp": datetime.now().isoformat(),
                "dimensions": "512x512",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_background_image(self, scene_description: str, style: VisualStyle,
                                 content_type: str = "educational") -> VisualAsset:
        """Generate background image for educational scenes"""
        
        style_info = self.visual_generator.style_templates.get(style, {})
        
        prompt = f"""
        Create a beautiful {style.value} background illustration for children's educational content.
        
        Scene Description: {scene_description}
        Content Type: {content_type}
        
        Visual Requirements:
        - Style: {style.value}
        - Color palette: {', '.join(style_info.get('color_palette', ['bright', 'cheerful']))}
        - Mood: {', '.join(style_info.get('style_keywords', ['educational', 'friendly']))}
        - Brightness: {style_info.get('brightness', 'medium')}
        
        Design Guidelines:
        - Child-friendly and engaging environment
        - Not too busy or distracting from main content
        - Suitable for educational video background
        - Clear areas for character placement
        - High quality illustration
        - Safe and appropriate for young children
        - Supports learning atmosphere
        """
        
        # Generate unique filename
        file_hash = hashlib.md5(f"{scene_description}_{style.value}_{content_type}".encode()).hexdigest()[:8]
        file_path = f"{self.assets_dir}/backgrounds/bg_{content_type}_{style.value}_{file_hash}.png"
        
        # Generate image
        try:
            from src.utils.media_tools import generate_image
            generate_image(prompt, file_path, aspect_ratio="landscape")
        except ImportError:
            self._create_placeholder_image(file_path, f"Background: {scene_description}")
        
        asset = VisualAsset(
            asset_id=f"bg_{content_type}_{style.value}_{file_hash}",
            asset_type="background",
            description=f"Background for {scene_description}",
            style=style,
            file_path=file_path,
            metadata={
                "scene_description": scene_description,
                "content_type": content_type,
                "generation_prompt": prompt.strip(),
                "generation_timestamp": datetime.now().isoformat(),
                "dimensions": "1920x1080",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_educational_object(self, object_type: str, topic: str, 
                                   style: VisualStyle) -> VisualAsset:
        """Generate educational objects like letters, numbers, shapes"""
        
        style_info = self.visual_generator.style_templates.get(style, {})
        
        prompt = f"""
        Create a clear, educational illustration of {object_type} for teaching {topic} to children.
        
        Object Details:
        - Type: {object_type}
        - Topic: {topic}
        - Style: {style.value}
        
        Visual Requirements:
        - Large, bold, and easily recognizable
        - High contrast for excellent visibility
        - Child-friendly design
        - Educational and clear presentation
        - Color palette: {', '.join(style_info.get('color_palette', ['bright']))}
        - Style keywords: {', '.join(style_info.get('style_keywords', ['educational']))}
        
        Design Guidelines:
        - Perfect for educational videos
        - Simple and uncluttered
        - Engaging for young learners
        - Professional quality
        - Suitable for animation
        """
        
        file_hash = hashlib.md5(f"{object_type}_{topic}_{style.value}".encode()).hexdigest()[:8]
        file_path = f"{self.assets_dir}/objects/{object_type}_{topic}_{style.value}_{file_hash}.png"
        
        try:
            from src.utils.media_tools import generate_image
            generate_image(prompt, file_path, aspect_ratio="square")
        except ImportError:
            self._create_placeholder_image(file_path, f"{object_type}: {topic}")
        
        asset = VisualAsset(
            asset_id=f"obj_{object_type}_{topic}_{file_hash}",
            asset_type="educational_object",
            description=f"{object_type} for teaching {topic}",
            style=style,
            file_path=file_path,
            metadata={
                "object_type": object_type,
                "topic": topic,
                "generation_prompt": prompt.strip(),
                "generation_timestamp": datetime.now().isoformat(),
                "dimensions": "512x512",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_background_music(self, content_type: str, age_group: str,
                                 duration_minutes: float, style: AudioStyle) -> AudioAsset:
        """Generate background music for educational content"""
        
        template = self.audio_generator.music_templates.get(style, {})
        
        prompt = f"""
        Compose original {style.value} background music for {content_type} educational content targeting {age_group} children.
        
        Musical Specifications:
        - Duration: {duration_minutes} minutes
        - Tempo: {template.get('tempo', '100-120 BPM')}
        - Instruments: {', '.join(template.get('instruments', ['piano', 'light percussion']))}
        - Mood: {template.get('mood', 'educational and engaging')}
        - Key: {template.get('key_signatures', ['C major'])[0] if template.get('key_signatures') else 'C major'}
        
        Requirements:
        - Child-appropriate and engaging
        - Supports learning without distraction
        - Seamless looping capability
        - Consistent energy level
        - Copyright-free original composition
        - High quality audio production
        - Suitable for {age_group} attention spans
        """
        
        file_hash = hashlib.md5(f"{content_type}_{age_group}_{style.value}_{duration_minutes}".encode()).hexdigest()[:8]
        file_path = f"{self.assets_dir}/audio/music/music_{content_type}_{style.value}_{file_hash}.mp3"
        
        try:
            from src.utils.media_tools import generate_audio
            generate_audio(prompt, file_path, duration_seconds=duration_minutes * 60)
        except ImportError:
            self._create_placeholder_audio(file_path, duration_minutes * 60)
        
        asset = AudioAsset(
            asset_id=f"music_{content_type}_{style.value}_{file_hash}",
            asset_type="background_music",
            description=f"Background music for {content_type} content ({age_group})",
            style=style,
            file_path=file_path,
            duration_seconds=duration_minutes * 60,
            metadata={
                "content_type": content_type,
                "age_group": age_group,
                "generation_prompt": prompt.strip(),
                "generation_timestamp": datetime.now().isoformat(),
                "format": "MP3",
                "bitrate": "320kbps"
            }
        )
        
        return asset
    
    def generate_voice_narration(self, script_text: str, character_name: str,
                                age_group: str) -> AudioAsset:
        """Generate voice narration for educational scripts"""
        
        voice_settings = self.audio_generator._get_voice_settings(character_name, age_group)
        
        prompt = f"""
        Generate clear, engaging voice narration for children's educational content.
        
        Script: {script_text}
        Character: {character_name}
        Target Audience: {age_group} children
        
        Voice Characteristics:
        - Voice type: {voice_settings.get('voice_type', 'child_friendly')}
        - Age: {voice_settings.get('age', '6-8 years')}
        - Pitch: {voice_settings.get('pitch', 'medium')}
        - Speed: {voice_settings.get('speed', 'moderate')}
        - Emotion: {voice_settings.get('emotion', 'friendly')}
        
        Requirements:
        - Clear pronunciation for educational content
        - Engaging and expressive delivery
        - Appropriate pacing for {age_group}
        - Warm and encouraging tone
        - Professional audio quality
        - Child-safe and appropriate
        """
        
        file_hash = hashlib.md5(f"{character_name}_{script_text[:50]}_{age_group}".encode()).hexdigest()[:8]
        file_path = f"{self.assets_dir}/audio/voice/voice_{character_name}_{file_hash}.mp3"
        
        # Estimate duration (approximately 2 words per second for child-appropriate pacing)
        word_count = len(script_text.split())
        duration_seconds = word_count / 2.0
        
        try:
            from src.utils.media_tools import generate_speech
            generate_speech(script_text, file_path, voice_settings)
        except ImportError:
            self._create_placeholder_audio(file_path, duration_seconds)
        
        asset = AudioAsset(
            asset_id=f"voice_{character_name}_{file_hash}",
            asset_type="voice_narration",
            description=f"Voice narration by {character_name}",
            style=AudioStyle.EDUCATIONAL_FOCUSED,
            file_path=file_path,
            duration_seconds=duration_seconds,
            metadata={
                "character_name": character_name,
                "script_text": script_text,
                "voice_settings": voice_settings,
                "age_group": age_group,
                "generation_timestamp": datetime.now().isoformat(),
                "format": "MP3",
                "bitrate": "320kbps"
            }
        )
        
        return asset
    
    def _create_placeholder_image(self, file_path: str, text: str):
        """Create placeholder image when AI generation is not available"""
        
        # Create a simple placeholder using PIL or similar
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (512, 512), color='lightblue')
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Calculate text position
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (512 - text_width) // 2
            y = (512 - text_height) // 2
            
            draw.text((x, y), text, fill='darkblue', font=font)
            
            # Save image
            img.save(file_path)
            
        except ImportError:
            # Create empty file as fallback
            with open(file_path, 'w') as f:
                f.write(f"Placeholder for: {text}")
    
    def _create_placeholder_audio(self, file_path: str, duration_seconds: float):
        """Create placeholder audio when AI generation is not available"""
        
        try:
            import numpy as np
            from scipy.io.wavfile import write
            
            # Generate simple tone
            sample_rate = 44100
            samples = int(sample_rate * duration_seconds)
            frequency = 440  # A note
            
            # Generate sine wave
            t = np.linspace(0, duration_seconds, samples, False)
            audio = np.sin(2 * np.pi * frequency * t) * 0.1  # Low volume
            
            # Save as WAV (can be converted to MP3 later)
            wav_path = file_path.replace('.mp3', '.wav')
            write(wav_path, sample_rate, (audio * 32767).astype(np.int16))
            
        except ImportError:
            # Create empty file as fallback
            with open(file_path, 'w') as f:
                f.write(f"Placeholder audio: {duration_seconds} seconds")
    
    def get_asset_info(self, asset_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a generated asset"""
        
        # In production, this would query a database
        # For now, return mock data
        return {
            "asset_id": asset_id,
            "status": "generated",
            "file_exists": True,
            "generation_timestamp": datetime.now().isoformat()
        }
    
    def cleanup_old_assets(self, days_old: int = 30):
        """Clean up assets older than specified days"""
        
        import time
        current_time = time.time()
        cutoff_time = current_time - (days_old * 24 * 60 * 60)
        
        for root, dirs, files in os.walk(self.assets_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.getmtime(file_path) < cutoff_time:
                    try:
                        os.remove(file_path)
                        print(f"Cleaned up old asset: {file_path}")
                    except OSError:
                        pass

