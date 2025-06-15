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
    self.media_service = MediaGenerationService(self.assets_dir)
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

    
    def create_educational_video(self, content_data: Dict[str, Any]) -> VideoProject:
        """Create complete educational video from content data"""
        
        # Extract content information
        topic = content_data.get('topic', 'learning')
        content_type = content_data.get('content_type', 'alphabet')
        age_group = content_data.get('age_group', 'preschool')
        title = content_data.get('title', f'Learning {topic}')
        script_text = content_data.get('script_text', '')
        scene_descriptions = content_data.get('scene_descriptions', [])
        duration_minutes = content_data.get('duration_minutes', 3)
        
        # Generate unique project ID
        project_hash = hashlib.md5(f"{topic}_{content_type}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
        project_id = f"video_{content_type}_{topic}_{project_hash}"
        
        print(f"Creating educational video: {title}")
        print(f"Project ID: {project_id}")
        
        # Step 1: Generate all visual assets
        print("Generating visual assets...")
        visual_assets = self._generate_visual_assets(content_data)
        
        # Step 2: Generate all audio assets
        print("Generating audio assets...")
        audio_assets = self._generate_audio_assets(content_data)
        
        # Step 3: Create video scenes
        print("Creating video scenes...")
        scenes = self._create_video_scenes(content_data, visual_assets, audio_assets)
        
        # Step 4: Assemble final video
        print("Assembling final video...")
        output_path = f"{self.video_output_dir}/{project_id}.mp4"
        
        # Create video project
        video_project = VideoProject(
            project_id=project_id,
            title=title,
            content_type=content_type,
            age_group=age_group,
            total_duration=duration_minutes * 60,
            scenes=scenes,
            background_music=audio_assets.get('background_music', {}).get('file_path', ''),
            output_path=output_path,
            metadata={
                "topic": topic,
                "generation_timestamp": datetime.now().isoformat(),
                "visual_style": self.visual_style.value,
                "audio_style": self.audio_style.value,
                "characters_used": list(self.main_characters.keys()),
                "total_assets": len(visual_assets) + len(audio_assets)
            }
        )
        
        # Assemble the video
        success = self._assemble_video_file(video_project, visual_assets, audio_assets)
        
        if success:
            print(f"Video created successfully: {output_path}")
        else:
            print(f"Video creation failed for project: {project_id}")
        
        return video_project
    
    def _generate_visual_assets(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate all visual assets needed for the video"""
        
        topic = content_data.get('topic', 'learning')
        content_type = content_data.get('content_type', 'alphabet')
        age_group = content_data.get('age_group', 'preschool')
        scene_descriptions = content_data.get('scene_descriptions', [])
        
        visual_assets = {
            'characters': {},
            'backgrounds': [],
            'educational_objects': [],
            'text_overlays': []
        }
        
        # Generate main character (Luna as primary teacher)
        try:
            luna_asset = self.media_service.generate_character_image(
                character_name="Luna",
                style=self.visual_style,
                age_group=age_group,
                expression="friendly"
            )
            visual_assets['characters']['Luna'] = {
                'asset_id': luna_asset.asset_id,
                'file_path': luna_asset.file_path,
                'character_info': self.main_characters['Luna']
            }
        except Exception as e:
            print(f"Failed to generate Luna character: {e}")
        
        # Generate companion character (Sunny)
        try:
            sunny_asset = self.media_service.generate_character_image(
                character_name="Sunny", 
                style=self.visual_style,
                age_group=age_group,
                expression="excited"
            )
            visual_assets['characters']['Sunny'] = {
                'asset_id': sunny_asset.asset_id,
                'file_path': sunny_asset.file_path,
                'character_info': self.main_characters['Sunny']
            }
        except Exception as e:
            print(f"Failed to generate Sunny character: {e}")
        
        # Generate backgrounds for each scene
        for i, scene in enumerate(scene_descriptions):
            try:
                scene_desc = scene.get('description', f'Educational scene for {topic}')
                background_asset = self.media_service.generate_background_image(
                    scene_description=scene_desc,
                    style=self.visual_style,
                    content_type=content_type
                )
                visual_assets['backgrounds'].append({
                    'scene_number': i + 1,
                    'asset_id': background_asset.asset_id,
                    'file_path': background_asset.file_path,
                    'description': scene_desc
                })
            except Exception as e:
                print(f"Failed to generate background for scene {i+1}: {e}")
        
        # Generate educational object for the topic
        try:
            object_asset = self.media_service.generate_educational_object(
                object_type='educational_element',
                topic=topic,
                style=self.visual_style
            )
            visual_assets['educational_objects'].append({
                'asset_id': object_asset.asset_id,
                'file_path': object_asset.file_path,
                'topic': topic
            })
        except Exception as e:
            print(f"Failed to generate educational object: {e}")
        
        return visual_assets
    
    def _generate_audio_assets(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate all audio assets needed for the video"""
        
        content_type = content_data.get('content_type', 'alphabet')
        age_group = content_data.get('age_group', 'preschool')
        script_text = content_data.get('script_text', '')
        duration_minutes = content_data.get('duration_minutes', 3)
        
        audio_assets = {
            'background_music': None,
            'voice_narration': None,
            'sound_effects': []
        }
        
        # Generate nursery-style background music
        try:
            music_asset = self.media_service.generate_background_music(
                content_type=content_type,
                age_group=age_group,
                duration_minutes=duration_minutes,
                style=self.audio_style
            )
            audio_assets['background_music'] = {
                'asset_id': music_asset.asset_id,
                'file_path': music_asset.file_path,
                'duration_seconds': music_asset.duration_seconds
            }
        except Exception as e:
            print(f"Failed to generate background music: {e}")
        
        # Generate friendly female child voice narration
        if script_text:
            try:
                voice_asset = self.media_service.generate_voice_narration(
                    script_text=script_text,
                    character_name="Luna",  # Use Luna as primary narrator
                    age_group=age_group
                )
                audio_assets['voice_narration'] = {
                    'asset_id': voice_asset.asset_id,
                    'file_path': voice_asset.file_path,
                    'duration_seconds': voice_asset.duration_seconds,
                    'character': 'Luna'
                }
            except Exception as e:
                print(f"Failed to generate voice narration: {e}")
        
        return audio_assets
    
    def _create_video_scenes(self, content_data: Dict[str, Any], 
                           visual_assets: Dict[str, Any], 
                           audio_assets: Dict[str, Any]) -> List[VideoScene]:
        """Create video scenes from content and assets"""
        
        scene_descriptions = content_data.get('scene_descriptions', [])
        topic = content_data.get('topic', 'learning')
        
        scenes = []
        
        # If no scene descriptions, create default scenes
        if not scene_descriptions:
            scene_descriptions = [
                {
                    'description': f'Introduction to {topic}',
                    'duration_seconds': 30,
                    'content': f'Welcome! Today we\'re learning about {topic}!'
                },
                {
                    'description': f'Exploring {topic}',
                    'duration_seconds': 60,
                    'content': f'Let\'s discover more about {topic} together!'
                },
                {
                    'description': f'Practice with {topic}',
                    'duration_seconds': 60,
                    'content': f'Now let\'s practice what we learned about {topic}!'
                },
                {
                    'description': f'Conclusion about {topic}',
                    'duration_seconds': 30,
                    'content': f'Great job learning about {topic}! See you next time!'
                }
            ]
        
        for i, scene_desc in enumerate(scene_descriptions):
            scene_id = f"scene_{i+1}"
            
            # Get background for this scene
            background_path = ""
            if i < len(visual_assets.get('backgrounds', [])):
                background_path = visual_assets['backgrounds'][i]['file_path']
            elif visual_assets.get('backgrounds'):
                background_path = visual_assets['backgrounds'][0]['file_path']
            
            # Create scene
            scene = VideoScene(
                scene_id=scene_id,
                duration_seconds=scene_desc.get('duration_seconds', 45),
                background_image=background_path,
                characters=[
                    {
                        'name': 'Luna',
                        'file_path': visual_assets.get('characters', {}).get('Luna', {}).get('file_path', ''),
                        'position': 'center_left',
                        'animation': 'gentle_wave'
                    },
                    {
                        'name': 'Sunny', 
                        'file_path': visual_assets.get('characters', {}).get('Sunny', {}).get('file_path', ''),
                        'position': 'center_right',
                        'animation': 'excited_bounce'
                    }
                ],
                educational_objects=[
                    obj['file_path'] for obj in visual_assets.get('educational_objects', [])
                ],
                text_overlays=[
                    {
                        'text': scene_desc.get('content', f'Learning about {topic}'),
                        'position': 'bottom_center',
                        'style': 'child_friendly',
                        'duration': scene_desc.get('duration_seconds', 45)
                    }
                ],
                audio_narration=audio_assets.get('voice_narration', {}).get('file_path', ''),
                scene_description=scene_desc.get('description', f'Scene {i+1}')
            )
            
            scenes.append(scene)
        
        return scenes
    
    def _assemble_video_file(self, video_project: VideoProject, 
                           visual_assets: Dict[str, Any], 
                           audio_assets: Dict[str, Any]) -> bool:
        """Assemble final video file using ffmpeg"""
        
        try:
            # Create a simple video assembly using available assets
            # This is a basic implementation - production would be more sophisticated
            
            # Get the first background image as base
            background_image = ""
            if visual_assets.get('backgrounds'):
                background_image = visual_assets['backgrounds'][0]['file_path']
            
            # Get background music
            background_music = audio_assets.get('background_music', {}).get('file_path', '')
            
            # Get voice narration
            voice_narration = audio_assets.get('voice_narration', {}).get('file_path', '')
            
            # Create video using ffmpeg
            duration = video_project.total_duration
            
            # Basic ffmpeg command to create video from image and audio
            cmd = [
                'ffmpeg', '-y',  # Overwrite output
                '-loop', '1',    # Loop the image
                '-i', background_image if background_image and os.path.exists(background_image) else '/dev/null',
                '-f', 'lavfi', '-i', f'color=c=lightblue:size=1920x1080:d={duration}',  # Fallback background
                '-t', str(duration),
                '-c:v', 'libx264',
                '-r', '30',      # 30 fps
                '-pix_fmt', 'yuv420p',
                video_project.output_path
            ]
            
            # Add audio if available
            if background_music and os.path.exists(background_music):
                cmd.extend(['-i', background_music, '-c:a', 'aac', '-shortest'])
            
            # Run ffmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Video assembled successfully: {video_project.output_path}")
                return True
            else:
                print(f"FFmpeg error: {result.stderr}")
                
                # Fallback: create a simple placeholder video
                return self._create_placeholder_video(video_project)
                
        except Exception as e:
            print(f"Video assembly failed: {e}")
            return self._create_placeholder_video(video_project)
    
    def _create_placeholder_video(self, video_project: VideoProject) -> bool:
        """Create a placeholder video when full assembly fails"""
        
        try:
            duration = min(video_project.total_duration, 180)  # Max 3 minutes for placeholder
            
            # Create simple colored video with text
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', f'color=c=lightblue:size=1920x1080:d={duration}',
                '-vf', f'drawtext=text=\'{video_project.title}\':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264',
                '-t', str(duration),
                '-r', '30',
                video_project.output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Placeholder video created: {video_project.output_path}")
                return True
            else:
                print(f"Placeholder creation failed: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"Placeholder video creation failed: {e}")
            return False
    
    def get_video_info(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a generated video"""
        
        video_path = f"{self.video_output_dir}/{project_id}.mp4"
        
        if os.path.exists(video_path):
            file_size = os.path.getsize(video_path)
            return {
                "project_id": project_id,
                "file_path": video_path,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "exists": True,
                "created_at": datetime.fromtimestamp(os.path.getctime(video_path)).isoformat()
            }
        else:
            return None
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        
        try:
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("Temporary files cleaned up")
        except Exception as e:
            print(f"Cleanup failed: {e}")

# Example usage and testing
if __name__ == "__main__":
    # Test video generation
    video_service = VideoGenerationService()
    
    # Sample content data
    test_content = {
        "topic": "Letter A",
        "content_type": "alphabet",
        "age_group": "preschool",
        "title": "Learning the Letter A",
        "duration_minutes": 2,
        "script_text": "Hello! Today we're learning about the letter A. A is for Apple and Ant. Can you say A with me? A! A! A! Great job!",
        "scene_descriptions": [
            {
                "description": "Colorful classroom with alphabet chart",
                "duration_seconds": 60,
                "content": "Welcome to our learning adventure! Today we're exploring the letter A!"
            },
            {
                "description": "Fun learning environment with educational objects",
                "duration_seconds": 60,
                "content": "A is for Apple and Ant! Let's practice saying A together!"
            }
        ]
    }
    
    # Generate video
    video_project = video_service.create_educational_video(test_content)
    print(f"Test video project created: {video_project.project_id}")

