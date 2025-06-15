
"""
Video Generation and Assembly Service
Creates complete educational videos using AI-generated assets
"""

import os
import json
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import hashlib

from src.services.media_generation_service import MediaGenerationService
from src.models.media_generator import VisualStyle, AudioStyle

@dataclass
class VideoScene:
    scene_id: str
    duration_seconds: float
    background_image: str
    characters: List[Dict[str, Any]]
    educational_objects: List[str]
    text_overlays: List[Dict[str, Any]]
    audio_narration: str
    scene_description: str

@dataclass
class VideoProject:
    project_id: str
    title: str
    content_type: str
    age_group: str
    total_duration: float
    scenes: List[VideoScene]
    background_music: str
    output_path: str
    metadata: Dict[str, Any]

class VideoGenerationService:
    """Service for creating complete educational videos"""
    
    def __init__(self, assets_dir: Optional[str] = None):
        if assets_dir is None:
            assets_dir = os.path.join(os.getcwd(), "generated-assets")
        self.assets_dir = assets_dir
        self.media_service = MediaGenerationService(assets_dir)
        self.video_output_dir = os.path.join(self.assets_dir, "videos")
        self.temp_dir = os.path.join(self.assets_dir, "temp")
        
        os.makedirs(self.video_output_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)

        self.visual_style = VisualStyle.BRIGHT_COLORFUL
        self.audio_style = AudioStyle.UPBEAT_CHEERFUL
        
        self.main_characters = {
            "Luna": {
                "type": "child_female",
                "age": "5-6 years",
                "personality": "friendly and helpful",
                "appearance": "brown curly hair, green eyes, purple dress with stars",
                "voice_type": "friendly_female_child",
                "role": "main_teacher"
            },
            "Sunny": {
                "type": "child_female",
                "age": "4-5 years",
                "personality": "curious and excited",
                "appearance": "blonde hair, blue eyes, yellow shirt with sun design",
                "voice_type": "friendly_female_child",
                "role": "learning_companion"
            },
            "Melody": {
                "type": "child_female",
                "age": "6-7 years",
                "personality": "musical and encouraging",
                "appearance": "red hair in pigtails, brown eyes, rainbow striped shirt",
                "voice_type": "friendly_female_child",
                "role": "music_guide"
            }
        }
