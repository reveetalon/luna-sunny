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

    def __init__(self, assets_dir: Optional[str] = None):
        if assets_dir is None:
            assets_dir = os.path.join(os.getcwd(), "generated-assets")
        self.assets_dir = assets_dir
        self.visual_generator = VisualGenerator()
        self.audio_generator = AudioGenerator()
        self.video_assembler = VideoAssembler()
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

    def generate_character_image(self, character_name: str, style: VisualStyle, age_group: str, expression: str = "happy") -> VisualAsset:
        """Generate character image using AI image generation"""
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
        """

        return self.visual_generator.generate_image(
            prompt=prompt,
            character_name=character_name
        )
