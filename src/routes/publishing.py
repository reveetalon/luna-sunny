"""
Publishing and Upload API Routes
Handles automated video uploading and publishing
"""

from flask import Blueprint, request, jsonify, send_file
from src.services.automated_publishing_service import AutomatedPublishingService
from datetime import datetime
import os

publishing_bp = Blueprint('publishing', __name__)

# Initialize publishing service
publishing_service = AutomatedPublishingService()

@publishing_bp.route('/upload', methods=['POST'])
def upload_video():
    """Upload video to all enabled platforms"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        video_path = data.get('video_path')
        video_metadata = data.get('video_metadata', {})
        
        if not video_path:
            return jsonify({
                'error': 'video_path is required',
                'status': 'error'
            }), 400
        
        if not os.path.exists(video_path):
            return jsonify({
                'error': f'Video file not found: {video_path}',
                'status': 'error'
            }), 404
        
        # Upload to all platforms
        upload_results = publishing_service.upload_video_to_all_platforms(video_path, video_metadata)
        
        # Generate thumbnail
        thumbnail_path = publishing_service.generate_thumbnail(video_path, video_metadata)
        
        result = {
            'video_path': video_path,
            'thumbnail_path': thumbnail_path,
            'upload_results': [
                {
                    'platform': r.platform,
                    'video_id': r.video_id,
                    'upload_url': r.upload_url,
                    'status': r.status,
                    'upload_timestamp': r.upload_timestamp
                } for r in upload_results
            ],
            'successful_uploads': len([r for r in upload_results if r.status == 'success']),
            'total_platforms': len(upload_results),
            'upload_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Upload failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/upload/schedule', methods=['POST'])
def schedule_upload():
    """Schedule video upload for later"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        video_path = data.get('video_path')
        video_metadata = data.get('video_metadata', {})
        upload_time = data.get('upload_time')  # Optional - immediate if not provided
        
        if not video_path:
            return jsonify({
                'error': 'video_path is required',
                'status': 'error'
            }), 400
        
        if not os.path.exists(video_path):
            return jsonify({
                'error': f'Video file not found: {video_path}',
                'status': 'error'
            }), 404
        
        # Schedule upload
        result = publishing_service.schedule_upload(video_path, video_metadata, upload_time)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Upload scheduling failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/upload/autonomous', methods=['POST'])
def autonomous_upload():
    """Upload video generated autonomously"""
    
    try:
        data = request.get_json() or {}
        
        # Get the most recent video from video generation service
        from src.services.video_generation_service import VideoGenerationService
        video_service = VideoGenerationService()
        
        # Generate content autonomously if not provided
        if not data.get('video_project_id'):
            # Use autonomous content generation
            from src.models.topic_selector import TopicSelector
            from src.models.content_generator import ContentGenerator
            
            topic_selector = TopicSelector()
            content_generator = ContentGenerator()
            
            # Select optimal topic
            selected_topic = topic_selector.select_optimal_topic(
                age_group=data.get('age_group', 'preschool'),
                content_type=data.get('content_type', 'alphabet')
            )
            
            # Generate content
            generated_content = content_generator.generate_educational_content(
                topic=selected_topic['topic'],
                content_type=selected_topic['content_type'],
                age_group=data.get('age_group', 'preschool'),
                duration_minutes=data.get('duration_minutes', 3)
            )
            
            # Create video
            video_project = video_service.create_educational_video(generated_content)
            video_path = video_project.output_path
            video_metadata = {
                'topic': generated_content.get('topic'),
                'title': generated_content.get('title'),
                'content_type': generated_content.get('content_type'),
                'age_group': generated_content.get('age_group'),
                'characters': ['Luna', 'Sunny'],
                'autonomous_generation': True,
                'selected_topic_data': selected_topic
            }
        else:
            # Use provided video project
            video_project_id = data['video_project_id']
            video_info = video_service.get_video_info(video_project_id)
            
            if not video_info or not video_info.get('exists'):
                return jsonify({
                    'error': f'Video project not found: {video_project_id}',
                    'status': 'error'
                }), 404
            
            video_path = video_info['file_path']
            video_metadata = data.get('video_metadata', {})
        
        # Upload the video
        upload_results = publishing_service.upload_video_to_all_platforms(video_path, video_metadata)
        
        # Generate thumbnail
        thumbnail_path = publishing_service.generate_thumbnail(video_path, video_metadata)
        
        result = {
            'autonomous_upload': True,
            'video_path': video_path,
            'thumbnail_path': thumbnail_path,
            'video_metadata': video_metadata,
            'upload_results': [
                {
                    'platform': r.platform,
                    'video_id': r.video_id,
                    'upload_url': r.upload_url,
                    'status': r.status,
                    'upload_timestamp': r.upload_timestamp,
                    'metadata': r.metadata
                } for r in upload_results
            ],
            'successful_uploads': len([r for r in upload_results if r.status == 'success']),
            'total_platforms': len(upload_results),
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Autonomous upload failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/platforms', methods=['GET'])
def get_platforms():
    """Get platform configurations and status"""
    
    try:
        platform_status = publishing_service.get_platform_status()
        
        result = {
            'platforms': platform_status,
            'total_platforms': len(platform_status),
            'enabled_platforms': len([p for p in platform_status.values() if p['enabled']]),
            'configured_platforms': len([p for p in platform_status.values() if p['has_credentials']]),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get platform status: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/platforms/<platform>/config', methods=['PUT'])
def update_platform_config(platform):
    """Update platform configuration"""
    
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Configuration data is required',
                'status': 'error'
            }), 400
        
        success = publishing_service.update_platform_config(platform, data)
        
        if success:
            return jsonify({
                'platform': platform,
                'message': 'Configuration updated successfully',
                'status': 'success'
            }), 200
        else:
            return jsonify({
                'error': f'Failed to update configuration for platform: {platform}',
                'status': 'error'
            }), 400
        
    except Exception as e:
        return jsonify({
            'error': f'Configuration update failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/history', methods=['GET'])
def get_upload_history():
    """Get upload history"""
    
    try:
        limit = request.args.get('limit', 50, type=int)
        
        history = publishing_service.get_upload_history(limit)
        
        result = {
            'upload_history': history,
            'total_uploads': len(publishing_service.upload_history),
            'recent_uploads': len(history),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get upload history: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/thumbnail/generate', methods=['POST'])
def generate_thumbnail():
    """Generate thumbnail for video"""
    
    try:
        data = request.get_json()
        
        video_path = data.get('video_path')
        video_metadata = data.get('video_metadata', {})
        
        if not video_path:
            return jsonify({
                'error': 'video_path is required',
                'status': 'error'
            }), 400
        
        if not os.path.exists(video_path):
            return jsonify({
                'error': f'Video file not found: {video_path}',
                'status': 'error'
            }), 404
        
        thumbnail_path = publishing_service.generate_thumbnail(video_path, video_metadata)
        
        if thumbnail_path and os.path.exists(thumbnail_path):
            result = {
                'video_path': video_path,
                'thumbnail_path': thumbnail_path,
                'thumbnail_exists': True,
                'generation_timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
        else:
            result = {
                'video_path': video_path,
                'thumbnail_path': '',
                'thumbnail_exists': False,
                'error': 'Thumbnail generation failed',
                'status': 'partial_success'
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Thumbnail generation failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/thumbnail/<path:thumbnail_path>')
def download_thumbnail(thumbnail_path):
    """Download generated thumbnail"""
    
    try:
        # Construct full path
        full_path = f"/home/ubuntu/generated_assets/thumbnails/{thumbnail_path}"
        
        if not os.path.exists(full_path):
            return jsonify({
                'error': f'Thumbnail not found: {thumbnail_path}',
                'status': 'error'
            }), 404
        
        return send_file(full_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            'error': f'Thumbnail download failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/test', methods=['POST'])
def test_publishing():
    """Test publishing system with sample data"""
    
    try:
        # Create a test video if it doesn't exist
        test_video_dir = "/home/ubuntu/generated_assets/videos"
        test_video_path = f"{test_video_dir}/test_publishing.mp4"
        
        if not os.path.exists(test_video_path):
            # Create a simple test video
            import subprocess
            
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', 'color=c=lightgreen:size=1280x720:d=10',
                '-vf', 'drawtext=text=\'Publishing Test Video\':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264',
                '-t', '10',
                test_video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return jsonify({
                    'error': f'Failed to create test video: {result.stderr}',
                    'status': 'error'
                }), 500
        
        # Test metadata
        test_metadata = {
            "topic": "Publishing Test",
            "title": "Test Video for Publishing System",
            "content_type": "test",
            "age_group": "preschool",
            "characters": ["Luna", "Sunny"],
            "test_upload": True
        }
        
        # Test upload
        upload_results = publishing_service.upload_video_to_all_platforms(test_video_path, test_metadata)
        
        # Test thumbnail generation
        thumbnail_path = publishing_service.generate_thumbnail(test_video_path, test_metadata)
        
        result = {
            'test_status': 'completed',
            'test_video_path': test_video_path,
            'thumbnail_path': thumbnail_path,
            'upload_results': [
                {
                    'platform': r.platform,
                    'status': r.status,
                    'video_id': r.video_id,
                    'upload_url': r.upload_url
                } for r in upload_results
            ],
            'successful_uploads': len([r for r in upload_results if r.status == 'success']),
            'test_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Publishing test failed: {str(e)}',
            'status': 'error'
        }), 500

@publishing_bp.route('/health', methods=['GET'])
def publishing_health():
    """Check publishing service health"""
    
    try:
        platform_status = publishing_service.get_platform_status()
        
        health_status = {
            'service': 'automated_publishing',
            'platforms_configured': len([p for p in platform_status.values() if p['has_credentials']]),
            'platforms_enabled': len([p for p in platform_status.values() if p['enabled']]),
            'total_platforms': len(platform_status),
            'upload_history_count': len(publishing_service.upload_history),
            'config_files_exist': all([
                os.path.exists(publishing_service.platforms_config_file),
                os.path.exists(publishing_service.upload_history_file)
            ]),
            'healthy': True,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            'service': 'automated_publishing',
            'healthy': False,
            'error': str(e),
            'status': 'error'
        }), 500

