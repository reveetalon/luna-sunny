"""
Visual and Audio Generation Systems
Handles AI-powered generation of visual assets and audio content
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import os

class VisualStyle(Enum):
    BRIGHT_COLORFUL = "bright_colorful"
    SOFT_PASTEL = "soft_pastel"
    BOLD_CARTOON = "bold_cartoon"
    EDUCATIONAL_CLEAN = "educational_clean"

class AudioStyle(Enum):
    UPBEAT_CHEERFUL = "upbeat_cheerful"
    CALM_SOOTHING = "calm_soothing"
    PLAYFUL_ENERGETIC = "playful_energetic"
    EDUCATIONAL_FOCUSED = "educational_focused"

@dataclass
class VisualAsset:
    asset_id: str
    asset_type: str  # character, background, object, text_overlay
    description: str
    style: VisualStyle
    file_path: str
    metadata: Dict[str, Any]

@dataclass
class AudioAsset:
    asset_id: str
    asset_type: str  # music, voice, sound_effect
    description: str
    style: AudioStyle
    file_path: str
    duration_seconds: float
    metadata: Dict[str, Any]

class VisualGenerator:
    """Generates visual assets for educational videos"""
    
    def __init__(self):
        self.style_templates = self._load_style_templates()
        self.character_library = self._load_character_library()
        self.background_library = self._load_background_library()
    
    def generate_character(self, character_name: str, style: VisualStyle, 
                          age_group: str) -> VisualAsset:
        """Generate character visual asset"""
        
        # Character generation prompt based on style and age group
        character_prompt = self._build_character_prompt(character_name, style, age_group)
        
        # In production, this would call actual AI image generation
        # For now, creating mock asset
        asset = VisualAsset(
            asset_id=f"char_{character_name}_{style.value}",
            asset_type="character",
            description=f"{character_name} character in {style.value} style for {age_group}",
            style=style,
            file_path=f"/assets/characters/{character_name}_{style.value}.png",
            metadata={
                "character_name": character_name,
                "age_group": age_group,
                "generation_prompt": character_prompt,
                "dimensions": "1920x1080",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_background(self, scene_description: str, style: VisualStyle) -> VisualAsset:
        """Generate background visual asset"""
        
        background_prompt = self._build_background_prompt(scene_description, style)
        
        asset = VisualAsset(
            asset_id=f"bg_{hash(scene_description)}_{style.value}",
            asset_type="background",
            description=f"Background for: {scene_description}",
            style=style,
            file_path=f"/assets/backgrounds/bg_{hash(scene_description)}.png",
            metadata={
                "scene_description": scene_description,
                "generation_prompt": background_prompt,
                "dimensions": "1920x1080",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_educational_object(self, object_type: str, content_topic: str, 
                                   style: VisualStyle) -> VisualAsset:
        """Generate educational object (letters, numbers, shapes, etc.)"""
        
        object_prompt = self._build_object_prompt(object_type, content_topic, style)
        
        asset = VisualAsset(
            asset_id=f"obj_{object_type}_{content_topic}_{style.value}",
            asset_type="object",
            description=f"{object_type} for {content_topic} in {style.value} style",
            style=style,
            file_path=f"/assets/objects/{object_type}_{content_topic}.png",
            metadata={
                "object_type": object_type,
                "content_topic": content_topic,
                "generation_prompt": object_prompt,
                "dimensions": "512x512",
                "format": "PNG"
            }
        )
        
        return asset
    
    def generate_text_overlay(self, text: str, style: VisualStyle, 
                             position: str = "center") -> VisualAsset:
        """Generate text overlay for educational content"""
        
        asset = VisualAsset(
            asset_id=f"text_{hash(text)}_{style.value}",
            asset_type="text_overlay",
            description=f"Text overlay: {text[:50]}...",
            style=style,
            file_path=f"/assets/text/text_{hash(text)}.png",
            metadata={
                "text_content": text,
                "position": position,
                "font_style": self._get_font_style(style),
                "dimensions": "1920x200",
                "format": "PNG"
            }
        )
        
        return asset
    
    def _load_style_templates(self) -> Dict[VisualStyle, Dict[str, Any]]:
        """Load visual style templates"""
        
        return {
            VisualStyle.BRIGHT_COLORFUL: {
                "color_palette": ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"],
                "brightness": "high",
                "saturation": "high",
                "contrast": "medium",
                "style_keywords": ["vibrant", "cheerful", "energetic", "playful"]
            },
            VisualStyle.SOFT_PASTEL: {
                "color_palette": ["#FFB3BA", "#BAFFC9", "#BAE1FF", "#FFFFBA", "#FFD1DC"],
                "brightness": "medium",
                "saturation": "low",
                "contrast": "low",
                "style_keywords": ["gentle", "soothing", "calm", "soft"]
            },
            VisualStyle.BOLD_CARTOON: {
                "color_palette": ["#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#FF00FF"],
                "brightness": "high",
                "saturation": "maximum",
                "contrast": "high",
                "style_keywords": ["bold", "cartoon", "animated", "fun"]
            },
            VisualStyle.EDUCATIONAL_CLEAN: {
                "color_palette": ["#2E86AB", "#A23B72", "#F18F01", "#C73E1D", "#6A994E"],
                "brightness": "medium",
                "saturation": "medium",
                "contrast": "medium",
                "style_keywords": ["clean", "educational", "professional", "clear"]
            }
        }
    
    def _load_character_library(self) -> Dict[str, Dict[str, Any]]:
        """Load character design specifications"""
        
        return {
            "Sunny": {
                "type": "child",
                "age": "preschool",
                "personality": "curious",
                "appearance": "blonde hair, blue eyes, yellow shirt",
                "expressions": ["happy", "excited", "thinking", "surprised"]
            },
            "Luna": {
                "type": "child", 
                "age": "preschool",
                "personality": "helpful",
                "appearance": "brown hair, green eyes, purple dress",
                "expressions": ["kind", "encouraging", "patient", "proud"]
            },
            "Max": {
                "type": "child",
                "age": "toddler", 
                "personality": "energetic",
                "appearance": "red hair, brown eyes, blue overalls",
                "expressions": ["playful", "active", "laughing", "jumping"]
            },
            "Teacher Emma": {
                "type": "adult",
                "role": "educator",
                "appearance": "brown hair in bun, glasses, colorful cardigan",
                "expressions": ["teaching", "encouraging", "patient", "proud"]
            }
        }
    
    def _load_background_library(self) -> Dict[str, Dict[str, Any]]:
        """Load background scene specifications"""
        
        return {
            "classroom": {
                "elements": ["desks", "whiteboard", "alphabet_chart", "colorful_decorations"],
                "lighting": "bright_natural",
                "mood": "educational_friendly"
            },
            "playground": {
                "elements": ["swings", "slide", "sandbox", "trees", "blue_sky"],
                "lighting": "sunny_outdoor",
                "mood": "playful_active"
            },
            "home_living_room": {
                "elements": ["couch", "coffee_table", "bookshelf", "toys", "family_photos"],
                "lighting": "warm_indoor",
                "mood": "cozy_familiar"
            },
            "magical_forest": {
                "elements": ["tall_trees", "colorful_flowers", "friendly_animals", "sparkles"],
                "lighting": "magical_soft",
                "mood": "wonder_adventure"
            }
        }
    
    def _build_character_prompt(self, character_name: str, style: VisualStyle, 
                               age_group: str) -> str:
        """Build AI prompt for character generation"""
        
        character_info = self.character_library.get(character_name, {})
        style_info = self.style_templates.get(style, {})
        
        prompt = f"""
        Create a {style.value} illustration of {character_name}, a {character_info.get('type', 'child')} character.
        
        Character details:
        - Age: {character_info.get('age', age_group)}
        - Personality: {character_info.get('personality', 'friendly')}
        - Appearance: {character_info.get('appearance', 'cheerful child')}
        
        Style requirements:
        - Color palette: {', '.join(style_info.get('color_palette', []))}
        - Style keywords: {', '.join(style_info.get('style_keywords', []))}
        - Brightness: {style_info.get('brightness', 'medium')}
        - Target audience: {age_group} children
        
        The character should be engaging, child-friendly, and appropriate for educational content.
        High quality, professional illustration suitable for children's educational videos.
        """
        
        return prompt.strip()
    
    def _build_background_prompt(self, scene_description: str, style: VisualStyle) -> str:
        """Build AI prompt for background generation"""
        
        style_info = self.style_templates.get(style, {})
        
        prompt = f"""
        Create a {style.value} background illustration for: {scene_description}
        
        Style requirements:
        - Color palette: {', '.join(style_info.get('color_palette', []))}
        - Style keywords: {', '.join(style_info.get('style_keywords', []))}
        - Brightness: {style_info.get('brightness', 'medium')}
        - Saturation: {style_info.get('saturation', 'medium')}
        
        The background should be:
        - Child-friendly and engaging
        - Not too busy or distracting
        - Suitable for educational content
        - High quality illustration
        - 1920x1080 resolution
        """
        
        return prompt.strip()
    
    def _build_object_prompt(self, object_type: str, content_topic: str, 
                            style: VisualStyle) -> str:
        """Build AI prompt for educational object generation"""
        
        style_info = self.style_templates.get(style, {})
        
        prompt = f"""
        Create a {style.value} illustration of {object_type} for teaching {content_topic}.
        
        Object requirements:
        - Clear and easily recognizable
        - Educational and child-appropriate
        - Large and bold for easy viewing
        - {object_type} related to {content_topic}
        
        Style requirements:
        - Color palette: {', '.join(style_info.get('color_palette', []))}
        - Style keywords: {', '.join(style_info.get('style_keywords', []))}
        - High contrast for visibility
        - Clean and simple design
        """
        
        return prompt.strip()
    
    def _get_font_style(self, style: VisualStyle) -> Dict[str, str]:
        """Get font style specifications for text overlays"""
        
        font_styles = {
            VisualStyle.BRIGHT_COLORFUL: {
                "font_family": "Comic Sans MS",
                "font_weight": "bold",
                "font_size": "72px",
                "color": "#FFFFFF",
                "stroke": "#000000",
                "stroke_width": "3px"
            },
            VisualStyle.SOFT_PASTEL: {
                "font_family": "Arial Rounded",
                "font_weight": "normal",
                "font_size": "64px",
                "color": "#4A4A4A",
                "stroke": "#FFFFFF",
                "stroke_width": "2px"
            },
            VisualStyle.BOLD_CARTOON: {
                "font_family": "Impact",
                "font_weight": "bold",
                "font_size": "80px",
                "color": "#FFFF00",
                "stroke": "#000000",
                "stroke_width": "4px"
            },
            VisualStyle.EDUCATIONAL_CLEAN: {
                "font_family": "Open Sans",
                "font_weight": "semibold",
                "font_size": "68px",
                "color": "#2E86AB",
                "stroke": "#FFFFFF",
                "stroke_width": "2px"
            }
        }
        
        return font_styles.get(style, font_styles[VisualStyle.EDUCATIONAL_CLEAN])

class AudioGenerator:
    """Generates audio assets for educational videos"""
    
    def __init__(self):
        self.music_templates = self._load_music_templates()
        self.voice_settings = self._load_voice_settings()
        self.sound_effect_library = self._load_sound_effect_library()
    
    def generate_background_music(self, content_type: str, age_group: str, 
                                 duration_seconds: float, style: AudioStyle) -> AudioAsset:
        """Generate background music for educational content"""
        
        music_prompt = self._build_music_prompt(content_type, age_group, style)
        
        asset = AudioAsset(
            asset_id=f"music_{content_type}_{age_group}_{style.value}",
            asset_type="music",
            description=f"Background music for {content_type} content ({age_group})",
            style=style,
            file_path=f"/assets/audio/music_{content_type}_{style.value}.mp3",
            duration_seconds=duration_seconds,
            metadata={
                "content_type": content_type,
                "age_group": age_group,
                "generation_prompt": music_prompt,
                "tempo": self._get_tempo_for_style(style),
                "key": self._get_key_for_content(content_type),
                "format": "MP3",
                "bitrate": "320kbps"
            }
        )
        
        return asset
    
    def generate_voice_narration(self, script_text: str, character_name: str, 
                                age_group: str) -> AudioAsset:
        """Generate voice narration for script"""
        
        voice_settings = self._get_voice_settings(character_name, age_group)
        
        asset = AudioAsset(
            asset_id=f"voice_{character_name}_{hash(script_text)}",
            asset_type="voice",
            description=f"Voice narration by {character_name}",
            style=AudioStyle.EDUCATIONAL_FOCUSED,
            file_path=f"/assets/audio/voice_{character_name}_{hash(script_text)}.mp3",
            duration_seconds=self._estimate_speech_duration(script_text),
            metadata={
                "character_name": character_name,
                "script_text": script_text,
                "voice_settings": voice_settings,
                "age_group": age_group,
                "format": "MP3",
                "bitrate": "320kbps"
            }
        )
        
        return asset
    
    def generate_sound_effect(self, effect_type: str, context: str) -> AudioAsset:
        """Generate sound effect for specific context"""
        
        effect_spec = self.sound_effect_library.get(effect_type, {})
        
        asset = AudioAsset(
            asset_id=f"sfx_{effect_type}_{hash(context)}",
            asset_type="sound_effect",
            description=f"Sound effect: {effect_type} for {context}",
            style=AudioStyle.PLAYFUL_ENERGETIC,
            file_path=f"/assets/audio/sfx_{effect_type}.mp3",
            duration_seconds=effect_spec.get("duration", 2.0),
            metadata={
                "effect_type": effect_type,
                "context": context,
                "volume_level": effect_spec.get("volume", 0.7),
                "format": "MP3"
            }
        )
        
        return asset
    
    def _load_music_templates(self) -> Dict[AudioStyle, Dict[str, Any]]:
        """Load music generation templates"""
        
        return {
            AudioStyle.UPBEAT_CHEERFUL: {
                "tempo": "120-140 BPM",
                "instruments": ["piano", "xylophone", "acoustic_guitar", "light_drums"],
                "mood": "happy, energetic, motivating",
                "key_signatures": ["C major", "G major", "D major"]
            },
            AudioStyle.CALM_SOOTHING: {
                "tempo": "60-80 BPM", 
                "instruments": ["soft_piano", "strings", "flute", "gentle_bells"],
                "mood": "peaceful, relaxing, comforting",
                "key_signatures": ["F major", "Bb major", "Eb major"]
            },
            AudioStyle.PLAYFUL_ENERGETIC: {
                "tempo": "140-160 BPM",
                "instruments": ["bouncy_synth", "kazoo", "triangle", "wood_blocks"],
                "mood": "fun, silly, exciting",
                "key_signatures": ["C major", "F major", "G major"]
            },
            AudioStyle.EDUCATIONAL_FOCUSED: {
                "tempo": "90-110 BPM",
                "instruments": ["clean_piano", "soft_strings", "light_percussion"],
                "mood": "focused, encouraging, supportive",
                "key_signatures": ["C major", "Am", "F major"]
            }
        }
    
    def _load_voice_settings(self) -> Dict[str, Dict[str, Any]]:
        """Load voice generation settings for characters"""
        
        return {
            "Sunny": {
                "voice_type": "child_female",
                "age": "6-8 years",
                "pitch": "medium-high",
                "speed": "moderate",
                "emotion": "curious_excited"
            },
            "Luna": {
                "voice_type": "child_female", 
                "age": "7-9 years",
                "pitch": "medium",
                "speed": "calm",
                "emotion": "kind_helpful"
            },
            "Max": {
                "voice_type": "child_male",
                "age": "4-6 years", 
                "pitch": "high",
                "speed": "energetic",
                "emotion": "playful_excited"
            },
            "Teacher Emma": {
                "voice_type": "adult_female",
                "age": "25-35 years",
                "pitch": "medium",
                "speed": "clear_measured",
                "emotion": "warm_encouraging"
            }
        }
    
    def _load_sound_effect_library(self) -> Dict[str, Dict[str, Any]]:
        """Load sound effect specifications"""
        
        return {
            "success_chime": {
                "duration": 1.5,
                "volume": 0.8,
                "description": "Positive reinforcement sound"
            },
            "page_turn": {
                "duration": 0.8,
                "volume": 0.6,
                "description": "Scene transition sound"
            },
            "magic_sparkle": {
                "duration": 2.0,
                "volume": 0.7,
                "description": "Magical appearance effect"
            },
            "applause": {
                "duration": 3.0,
                "volume": 0.9,
                "description": "Celebration and achievement"
            },
            "gentle_pop": {
                "duration": 0.5,
                "volume": 0.5,
                "description": "Object appearance sound"
            }
        }
    
    def _build_music_prompt(self, content_type: str, age_group: str, 
                           style: AudioStyle) -> str:
        """Build AI prompt for music generation"""
        
        template = self.music_templates.get(style, {})
        
        prompt = f"""
        Generate {style.value} background music for {content_type} educational content for {age_group} children.
        
        Musical requirements:
        - Tempo: {template.get('tempo', '100-120 BPM')}
        - Instruments: {', '.join(template.get('instruments', []))}
        - Mood: {template.get('mood', 'educational and engaging')}
        - Key signature: {random.choice(template.get('key_signatures', ['C major']))}
        
        The music should:
        - Support learning without being distracting
        - Be appropriate for {age_group} attention spans
        - Loop seamlessly for extended content
        - Maintain consistent energy level
        - Be copyright-free and original
        """
        
        return prompt.strip()
    
    def _get_voice_settings(self, character_name: str, age_group: str) -> Dict[str, Any]:
        """Get voice settings for character"""
        
        settings = self.voice_settings.get(character_name, {})
        
        # Adjust settings based on age group
        if age_group == "toddler":
            settings = settings.copy()
            settings["speed"] = "slower"
            settings["clarity"] = "extra_clear"
        
        return settings
    
    def _estimate_speech_duration(self, script_text: str) -> float:
        """Estimate speech duration for script text"""
        
        word_count = len(script_text.split())
        # Average 2 words per second for child-appropriate pacing
        duration_seconds = word_count / 2.0
        
        return duration_seconds
    
    def _get_tempo_for_style(self, style: AudioStyle) -> str:
        """Get tempo specification for audio style"""
        
        tempo_map = {
            AudioStyle.UPBEAT_CHEERFUL: "130 BPM",
            AudioStyle.CALM_SOOTHING: "70 BPM", 
            AudioStyle.PLAYFUL_ENERGETIC: "150 BPM",
            AudioStyle.EDUCATIONAL_FOCUSED: "100 BPM"
        }
        
        return tempo_map.get(style, "100 BPM")
    
    def _get_key_for_content(self, content_type: str) -> str:
        """Get musical key based on content type"""
        
        key_map = {
            "alphabet": "C major",
            "numbers": "G major", 
            "colors": "F major",
            "behavior": "D major",
            "social": "A major"
        }
        
        return key_map.get(content_type, "C major")

class VideoAssembler:
    """Assembles visual and audio assets into final video"""
    
    def __init__(self):
        self.rendering_settings = self._load_rendering_settings()
    
    def assemble_video(self, script_data: Dict[str, Any], visual_assets: List[VisualAsset],
                      audio_assets: List[AudioAsset]) -> Dict[str, Any]:
        """Assemble final video from assets"""
        
        # Create video assembly plan
        assembly_plan = self._create_assembly_plan(script_data, visual_assets, audio_assets)
        
        # Generate video file (mock implementation)
        video_file_path = f"/assets/videos/video_{hash(str(script_data))}.mp4"
        
        # Video metadata
        video_metadata = {
            "title": script_data.get("title", "Educational Video"),
            "duration_seconds": script_data.get("duration_minutes", 5) * 60,
            "resolution": "1920x1080",
            "framerate": "30fps",
            "format": "MP4",
            "file_path": video_file_path,
            "assembly_plan": assembly_plan,
            "asset_count": {
                "visual_assets": len(visual_assets),
                "audio_assets": len(audio_assets)
            }
        }
        
        return video_metadata
    
    def _create_assembly_plan(self, script_data: Dict[str, Any], 
                             visual_assets: List[VisualAsset],
                             audio_assets: List[AudioAsset]) -> Dict[str, Any]:
        """Create detailed plan for video assembly"""
        
        scenes = script_data.get("scene_descriptions", [])
        audio_cues = script_data.get("audio_cues", [])
        
        assembly_plan = {
            "scenes": [],
            "audio_timeline": [],
            "transitions": [],
            "effects": []
        }
        
        # Plan each scene
        for i, scene in enumerate(scenes):
            scene_plan = {
                "scene_number": i + 1,
                "duration_seconds": scene.get("duration_seconds", 30),
                "visual_elements": scene.get("visual_elements", []),
                "character_actions": scene.get("character_actions", []),
                "background": f"background_{i}",
                "characters": script_data.get("character_list", []),
                "text_overlays": []
            }
            
            assembly_plan["scenes"].append(scene_plan)
        
        # Plan audio timeline
        for audio_cue in audio_cues:
            audio_plan = {
                "audio_type": audio_cue.get("type", "music"),
                "start_time": audio_cue.get("start_time", 0),
                "duration": audio_cue.get("duration", 30),
                "volume": audio_cue.get("volume", 0.7),
                "fade_in": audio_cue.get("fade_in", False),
                "fade_out": audio_cue.get("fade_out", False)
            }
            
            assembly_plan["audio_timeline"].append(audio_plan)
        
        return assembly_plan
    
    def _load_rendering_settings(self) -> Dict[str, Any]:
        """Load video rendering settings"""
        
        return {
            "resolution": "1920x1080",
            "framerate": 30,
            "bitrate": "5000k",
            "audio_bitrate": "320k",
            "format": "MP4",
            "codec": "H.264",
            "quality": "high",
            "optimization": "web"
        }

