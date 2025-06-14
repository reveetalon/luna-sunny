"""
Automated Upload and Publishing Service
Handles uploading videos to multiple platforms automatically
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import subprocess

@dataclass
class UploadResult:
    platform: str
    video_id: str
    upload_url: str
    status: str
    upload_timestamp: str
    metadata: Dict[str, Any]

@dataclass
class PublishingConfig:
    platform: str
    enabled: bool
    api_credentials: Dict[str, str]
    default_settings: Dict[str, Any]
    upload_schedule: Optional[str] = None

class AutomatedPublishingService:
    """Service for automated video uploading and publishing"""
    
    def __init__(self, config_dir: str = "/home/ubuntu/publishing_config"):
        self.config_dir = config_dir
        self.upload_history_file = f"{config_dir}/upload_history.json"
        self.platforms_config_file = f"{config_dir}/platforms_config.json"
        
        # Create config directory
        os.makedirs(config_dir, exist_ok=True)
        
        # Initialize platform configurations
        self.platforms = self._load_platform_configs()
        
        # Upload history tracking
        self.upload_history = self._load_upload_history()
    
    def _load_platform_configs(self) -> Dict[str, PublishingConfig]:
        """Load platform configurations"""
        
        default_configs = {
            "youtube": PublishingConfig(
                platform="youtube",
                enabled=True,
                api_credentials={
                    "client_id": "YOUR_YOUTUBE_CLIENT_ID",
                    "client_secret": "YOUR_YOUTUBE_CLIENT_SECRET",
                    "refresh_token": "YOUR_YOUTUBE_REFRESH_TOKEN"
                },
                default_settings={
                    "privacy_status": "public",
                    "category_id": "27",  # Education category
                    "default_language": "en",
                    "tags": ["education", "children", "learning", "preschool", "alphabet", "numbers"],
                    "description_template": "Educational content for children featuring Luna and Sunny! Learn {topic} in a fun and engaging way.\n\n🌟 Subscribe for more educational videos!\n🎨 Colorful 2D cartoon style\n🎵 Original nursery music\n👧 Friendly characters\n\n#Education #Children #Learning #Preschool #{topic}",
                    "thumbnail_style": "bright_educational"
                }
            ),
            "vimeo": PublishingConfig(
                platform="vimeo",
                enabled=True,
                api_credentials={
                    "access_token": "YOUR_VIMEO_ACCESS_TOKEN"
                },
                default_settings={
                    "privacy": "anybody",
                    "embed_privacy": "public",
                    "description_template": "Educational content for children! Learn {topic} with Luna and Sunny in this colorful and engaging video.",
                    "tags": ["education", "children", "learning", "preschool"]
                }
            ),
            "facebook": PublishingConfig(
                platform="facebook",
                enabled=False,  # Disabled by default - requires page access
                api_credentials={
                    "page_access_token": "YOUR_FACEBOOK_PAGE_ACCESS_TOKEN",
                    "page_id": "YOUR_FACEBOOK_PAGE_ID"
                },
                default_settings={
                    "published": True,
                    "description_template": "🎓 New educational video! Learn {topic} with Luna and Sunny! 🌟\n\n👶 Perfect for preschoolers\n🎨 Colorful and engaging\n🎵 Original music\n\n#Education #Children #Learning #{topic}"
                }
            )
        }
        
        # Load from file if exists, otherwise use defaults
        if os.path.exists(self.platforms_config_file):
            try:
                with open(self.platforms_config_file, 'r') as f:
                    saved_configs = json.load(f)
                
                # Update default configs with saved values
                for platform, config_data in saved_configs.items():
                    if platform in default_configs:
                        # Update existing config
                        default_configs[platform].enabled = config_data.get('enabled', True)
                        default_configs[platform].api_credentials.update(config_data.get('api_credentials', {}))
                        default_configs[platform].default_settings.update(config_data.get('default_settings', {}))
                        
            except Exception as e:
                print(f"Error loading platform configs: {e}")
        
        # Save current configs
        self._save_platform_configs(default_configs)
        
        return default_configs
    
    def _save_platform_configs(self, configs: Dict[str, PublishingConfig]):
        """Save platform configurations to file"""
        
        try:
            config_data = {}
            for platform, config in configs.items():
                config_data[platform] = {
                    'enabled': config.enabled,
                    'api_credentials': config.api_credentials,
                    'default_settings': config.default_settings,
                    'upload_schedule': config.upload_schedule
                }
            
            with open(self.platforms_config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
                
        except Exception as e:
            print(f"Error saving platform configs: {e}")
    
    def _load_upload_history(self) -> List[Dict[str, Any]]:
        """Load upload history from file"""
        
        if os.path.exists(self.upload_history_file):
            try:
                with open(self.upload_history_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading upload history: {e}")
        
        return []
    
    def _save_upload_history(self):
        """Save upload history to file"""
        
        try:
            with open(self.upload_history_file, 'w') as f:
                json.dump(self.upload_history, f, indent=2)
        except Exception as e:
            print(f"Error saving upload history: {e}")
    
    def upload_video_to_all_platforms(self, video_path: str, video_metadata: Dict[str, Any]) -> List[UploadResult]:
        """Upload video to all enabled platforms"""
        
        results = []
        
        for platform_name, config in self.platforms.items():
            if config.enabled:
                try:
                    print(f"Uploading to {platform_name}...")
                    result = self._upload_to_platform(video_path, video_metadata, config)
                    results.append(result)
                    
                    # Add to upload history
                    self.upload_history.append({
                        'video_path': video_path,
                        'platform': platform_name,
                        'result': asdict(result),
                        'upload_timestamp': datetime.now().isoformat()
                    })
                    
                except Exception as e:
                    print(f"Upload to {platform_name} failed: {e}")
                    results.append(UploadResult(
                        platform=platform_name,
                        video_id="",
                        upload_url="",
                        status="failed",
                        upload_timestamp=datetime.now().isoformat(),
                        metadata={"error": str(e)}
                    ))
        
        # Save updated history
        self._save_upload_history()
        
        return results
    
    def _upload_to_platform(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
        """Upload video to specific platform"""
        
        if config.platform == "youtube":
            return self._upload_to_youtube(video_path, video_metadata, config)
        elif config.platform == "vimeo":
            return self._upload_to_vimeo(video_path, video_metadata, config)
        elif config.platform == "facebook":
            return self._upload_to_facebook(video_path, video_metadata, config)
        else:
            raise ValueError(f"Unsupported platform: {config.platform}")
    
    def _upload_to_youtube(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
        """Upload video to YouTube using API"""
        
        # This is a mock implementation - real implementation would use YouTube Data API v3
        # For production, you would need to:
        # 1. Set up OAuth 2.0 credentials
        # 2. Use google-api-python-client library
        # 3. Handle authentication and refresh tokens
        
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        
        # Generate description from template
        description = config.default_settings['description_template'].format(
            topic=topic.lower()
        )
        
        # Mock upload result
        mock_video_id = f"yt_{hashlib.md5(f'{video_path}_{datetime.now()}'.encode()).hexdigest()[:8]}"
        
        print(f"Mock YouTube upload:")
        print(f"  Title: {title}")
        print(f"  Description: {description[:100]}...")
        print(f"  Tags: {config.default_settings['tags']}")
        print(f"  Category: {config.default_settings['category_id']}")
        print(f"  Privacy: {config.default_settings['privacy_status']}")
        
        return UploadResult(
            platform="youtube",
            video_id=mock_video_id,
            upload_url=f"https://youtube.com/watch?v={mock_video_id}",
            status="success",
            upload_timestamp=datetime.now().isoformat(),
            metadata={
                "title": title,
                "description": description,
                "tags": config.default_settings['tags'],
                "category_id": config.default_settings['category_id'],
                "privacy_status": config.default_settings['privacy_status']
            }
        )
    
    def _upload_to_vimeo(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
        """Upload video to Vimeo using API"""
        
        # Mock implementation - real implementation would use Vimeo API
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        
        description = config.default_settings['description_template'].format(
            topic=topic.lower()
        )
        
        mock_video_id = f"vimeo_{hashlib.md5(f'{video_path}_{datetime.now()}'.encode()).hexdigest()[:8]}"
        
        print(f"Mock Vimeo upload:")
        print(f"  Title: {title}")
        print(f"  Description: {description}")
        print(f"  Privacy: {config.default_settings['privacy']}")
        
        return UploadResult(
            platform="vimeo",
            video_id=mock_video_id,
            upload_url=f"https://vimeo.com/{mock_video_id}",
            status="success",
            upload_timestamp=datetime.now().isoformat(),
            metadata={
                "title": title,
                "description": description,
                "privacy": config.default_settings['privacy']
            }
        )
    
    def _upload_to_facebook(self, video_path: str, video_metadata: Dict[str, Any], config: PublishingConfig) -> UploadResult:
        """Upload video to Facebook using Graph API"""
        
        # Mock implementation - real implementation would use Facebook Graph API
        topic = video_metadata.get('topic', 'learning')
        title = video_metadata.get('title', f'Learning {topic}')
        
        description = config.default_settings['description_template'].format(
            topic=topic.lower()
        )
        
        mock_video_id = f"fb_{hashlib.md5(f'{video_path}_{datetime.now()}'.encode()).hexdigest()[:8]}"
        
        print(f"Mock Facebook upload:")
        print(f"  Title: {title}")
        print(f"  Description: {description}")
        print(f"  Published: {config.default_settings['published']}")
        
        return UploadResult(
            platform="facebook",
            video_id=mock_video_id,
            upload_url=f"https://facebook.com/watch/?v={mock_video_id}",
            status="success",
            upload_timestamp=datetime.now().isoformat(),
            metadata={
                "title": title,
                "description": description,
                "published": config.default_settings['published']
            }
        )
    
    def generate_thumbnail(self, video_path: str, video_metadata: Dict[str, Any]) -> str:
        """Generate thumbnail for video"""
        
        try:
            # Extract frame from video for thumbnail
            thumbnail_dir = os.path.dirname(video_path).replace('/videos', '/thumbnails')
            os.makedirs(thumbnail_dir, exist_ok=True)
            
            video_name = os.path.splitext(os.path.basename(video_path))[0]
            thumbnail_path = f"{thumbnail_dir}/{video_name}_thumbnail.jpg"
            
            # Use ffmpeg to extract frame at 5 seconds
            cmd = [
                'ffmpeg', '-y',
                '-i', video_path,
                '-ss', '5',  # Extract frame at 5 seconds
                '-vframes', '1',
                '-q:v', '2',  # High quality
                '-vf', 'scale=1280:720',  # HD resolution
                thumbnail_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(thumbnail_path):
                print(f"Thumbnail generated: {thumbnail_path}")
                return thumbnail_path
            else:
                print(f"Thumbnail generation failed: {result.stderr}")
                return self._create_custom_thumbnail(video_metadata, thumbnail_path)
                
        except Exception as e:
            print(f"Thumbnail generation error: {e}")
            return ""
    
    def _create_custom_thumbnail(self, video_metadata: Dict[str, Any], output_path: str) -> str:
        """Create custom thumbnail with text overlay"""
        
        try:
            topic = video_metadata.get('topic', 'Learning')
            title = video_metadata.get('title', f'Learning {topic}')
            
            # Create thumbnail with ffmpeg and text overlay
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', 'color=c=lightblue:size=1280x720:d=1',
                '-vf', f'drawtext=text=\'{title}\':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=(h-text_h)/2:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
                '-frames:v', '1',
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"Custom thumbnail created: {output_path}")
                return output_path
            else:
                print(f"Custom thumbnail creation failed: {result.stderr}")
                return ""
                
        except Exception as e:
            print(f"Custom thumbnail creation error: {e}")
            return ""
    
    def schedule_upload(self, video_path: str, video_metadata: Dict[str, Any], 
                       upload_time: Optional[str] = None) -> Dict[str, Any]:
        """Schedule video upload for later"""
        
        # For now, just upload immediately
        # In production, this would integrate with a job scheduler
        
        print(f"Scheduling upload for: {upload_time or 'immediate'}")
        
        # Generate thumbnail
        thumbnail_path = self.generate_thumbnail(video_path, video_metadata)
        
        # Upload to all platforms
        upload_results = self.upload_video_to_all_platforms(video_path, video_metadata)
        
        return {
            "video_path": video_path,
            "thumbnail_path": thumbnail_path,
            "upload_results": [asdict(result) for result in upload_results],
            "scheduled_time": upload_time,
            "actual_upload_time": datetime.now().isoformat(),
            "status": "completed"
        }
    
    def get_upload_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent upload history"""
        
        return self.upload_history[-limit:] if limit else self.upload_history
    
    def get_platform_status(self) -> Dict[str, Any]:
        """Get status of all platforms"""
        
        status = {}
        
        for platform_name, config in self.platforms.items():
            status[platform_name] = {
                "enabled": config.enabled,
                "has_credentials": bool(config.api_credentials.get('client_id') or 
                                      config.api_credentials.get('access_token') or
                                      config.api_credentials.get('page_access_token')),
                "last_upload": None,
                "total_uploads": 0
            }
            
            # Count uploads for this platform
            platform_uploads = [h for h in self.upload_history if h.get('platform') == platform_name]
            status[platform_name]["total_uploads"] = len(platform_uploads)
            
            if platform_uploads:
                status[platform_name]["last_upload"] = platform_uploads[-1].get('upload_timestamp')
        
        return status
    
    def update_platform_config(self, platform: str, config_updates: Dict[str, Any]) -> bool:
        """Update platform configuration"""
        
        if platform not in self.platforms:
            return False
        
        try:
            # Update configuration
            if 'enabled' in config_updates:
                self.platforms[platform].enabled = config_updates['enabled']
            
            if 'api_credentials' in config_updates:
                self.platforms[platform].api_credentials.update(config_updates['api_credentials'])
            
            if 'default_settings' in config_updates:
                self.platforms[platform].default_settings.update(config_updates['default_settings'])
            
            # Save updated configs
            self._save_platform_configs(self.platforms)
            
            return True
            
        except Exception as e:
            print(f"Error updating platform config: {e}")
            return False

# Example usage and testing
if __name__ == "__main__":
    # Test publishing service
    publishing_service = AutomatedPublishingService()
    
    # Sample video metadata
    test_metadata = {
        "topic": "Letter A",
        "title": "Learning the Letter A with Luna and Sunny",
        "content_type": "alphabet",
        "age_group": "preschool",
        "duration_minutes": 2,
        "characters": ["Luna", "Sunny"],
        "educational_objectives": ["Letter recognition", "Phonics", "Vocabulary"]
    }
    
    # Test video path (would be actual video file)
    test_video_path = "/home/ubuntu/generated_assets/videos/test_video.mp4"
    
    # Test upload scheduling
    if os.path.exists(test_video_path):
        result = publishing_service.schedule_upload(test_video_path, test_metadata)
        print(f"Upload test completed: {result['status']}")
    else:
        print("Test video not found, skipping upload test")
    
    # Test platform status
    status = publishing_service.get_platform_status()
    print(f"Platform status: {json.dumps(status, indent=2)}")

