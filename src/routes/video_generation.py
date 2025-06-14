"""
Video Generation API Routes
Handles complete video creation and assembly
"""

from flask import Blueprint, request, jsonify, send_file
from src.services.video_generation_service import VideoGenerationService
from datetime import datetime
import os

video_bp = Blueprint('video', __name__)

# Initialize video generation service
video_service = VideoGenerationService()

@video_bp.route('/generate', methods=['POST'])
def generate_video():
    """Generate complete educational video"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        content_data = data.get('content_data')
        
        if not content_data:
            return jsonify({
                'error': 'content_data is required',
                'status': 'error'
            }), 400
        
        # Validate content data
        required_fields = ['topic', 'content_type', 'age_group']
        missing_fields = [field for field in required_fields if not content_data.get(field)]
        
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {", ".join(missing_fields)}',
                'status': 'error'
            }), 400
        
        # Generate video
        video_project = video_service.create_educational_video(content_data)
        
        # Check if video was created successfully
        video_info = video_service.get_video_info(video_project.project_id)
        
        if video_info and video_info.get('exists'):
            result = {
                'project_id': video_project.project_id,
                'title': video_project.title,
                'content_type': video_project.content_type,
                'age_group': video_project.age_group,
                'duration_seconds': video_project.total_duration,
                'output_path': video_project.output_path,
                'file_info': video_info,
                'metadata': video_project.metadata,
                'scenes_count': len(video_project.scenes),
                'characters_used': video_project.metadata.get('characters_used', []),
                'visual_style': video_project.metadata.get('visual_style', 'bright_colorful'),
                'audio_style': video_project.metadata.get('audio_style', 'upbeat_cheerful'),
                'generation_timestamp': datetime.now().isoformat(),
                'status': 'success'
            }
        else:
            result = {
                'project_id': video_project.project_id,
                'title': video_project.title,
                'error': 'Video file was not created successfully',
                'status': 'partial_success'
            }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Video generation failed: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/generate/autonomous', methods=['POST'])
def generate_autonomous_video():
    """Generate video using autonomous content selection"""
    
    try:
        data = request.get_json() or {}
        
        # Use autonomous topic selection if no specific content provided
        age_group = data.get('age_group', 'preschool')
        content_type = data.get('content_type', 'alphabet')
        
        # Import topic selector for autonomous selection
        from src.models.topic_selector import TopicSelector
        topic_selector = TopicSelector()
        
        # Select optimal topic
        selected_topic = topic_selector.select_optimal_topic(
            age_group=age_group,
            content_type=content_type
        )
        
        # Generate content using the selected topic
        from src.models.content_generator import ContentGenerator
        content_generator = ContentGenerator()
        
        generated_content = content_generator.generate_educational_content(
            topic=selected_topic['topic'],
            content_type=content_type,
            age_group=age_group,
            duration_minutes=data.get('duration_minutes', 3)
        )
        
        # Create video from generated content
        video_project = video_service.create_educational_video(generated_content)
        
        # Get video info
        video_info = video_service.get_video_info(video_project.project_id)
        
        result = {
            'project_id': video_project.project_id,
            'title': video_project.title,
            'selected_topic': selected_topic,
            'generated_content': {
                'topic': generated_content.get('topic'),
                'content_type': generated_content.get('content_type'),
                'script_length': len(generated_content.get('script_text', '')),
                'scenes_count': len(generated_content.get('scene_descriptions', []))
            },
            'video_info': video_info,
            'autonomous_selection': True,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success' if video_info and video_info.get('exists') else 'partial_success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Autonomous video generation failed: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/project/<project_id>', methods=['GET'])
def get_video_project(project_id):
    """Get information about a video project"""
    
    try:
        video_info = video_service.get_video_info(project_id)
        
        if not video_info:
            return jsonify({
                'error': f'Video project not found: {project_id}',
                'status': 'error'
            }), 404
        
        return jsonify(video_info), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get video project info: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/project/<project_id>/download', methods=['GET'])
def download_video(project_id):
    """Download a generated video file"""
    
    try:
        video_info = video_service.get_video_info(project_id)
        
        if not video_info or not video_info.get('exists'):
            return jsonify({
                'error': f'Video file not found: {project_id}',
                'status': 'error'
            }), 404
        
        file_path = video_info['file_path']
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{project_id}.mp4",
            mimetype='video/mp4'
        )
        
    except Exception as e:
        return jsonify({
            'error': f'Video download failed: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/styles', methods=['GET'])
def get_video_styles():
    """Get available video styles and character information"""
    
    try:
        styles_info = {
            'visual_style': {
                'name': 'Colorful 2D Cartoon',
                'description': 'Bright, colorful cartoon style with friendly characters',
                'characteristics': [
                    'High contrast colors',
                    'Child-friendly designs',
                    'Educational focus',
                    'Engaging animations'
                ]
            },
            'audio_style': {
                'name': 'Nursery Style Music',
                'description': 'Original royalty-free nursery style music',
                'characteristics': [
                    'Upbeat and cheerful',
                    'Age-appropriate tempo',
                    'Educational support',
                    'Copyright-free'
                ]
            },
            'voice_style': {
                'name': 'Friendly Female Child Voice',
                'description': 'Warm, encouraging child-like female voice in English',
                'characteristics': [
                    'Clear pronunciation',
                    'Engaging delivery',
                    'Age-appropriate pacing',
                    'Encouraging tone'
                ]
            },
            'main_characters': video_service.main_characters,
            'status': 'success'
        }
        
        return jsonify(styles_info), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get style information: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/characters', methods=['GET'])
def get_characters():
    """Get information about available characters"""
    
    try:
        characters_info = {
            'main_characters': video_service.main_characters,
            'character_count': len(video_service.main_characters),
            'consistency_features': [
                'Unique fictional characters',
                'Consistent across all videos',
                'Child-friendly personalities',
                'Educational roles'
            ],
            'status': 'success'
        }
        
        return jsonify(characters_info), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to get character information: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/test', methods=['POST'])
def test_video_generation():
    """Test video generation with sample content"""
    
    try:
        # Sample test content
        test_content = {
            "topic": "Letter A",
            "content_type": "alphabet",
            "age_group": "preschool",
            "title": "Learning the Letter A with Luna and Sunny",
            "duration_minutes": 2,
            "script_text": "Hello friends! I'm Luna and this is Sunny! Today we're learning about the letter A. A is for Apple and Ant. Can you say A with us? A! A! A! Great job learning with us!",
            "scene_descriptions": [
                {
                    "description": "Colorful classroom with alphabet chart and friendly atmosphere",
                    "duration_seconds": 60,
                    "content": "Welcome to our learning adventure! Today Luna and Sunny are exploring the letter A!"
                },
                {
                    "description": "Fun learning environment with educational objects and bright colors",
                    "duration_seconds": 60,
                    "content": "A is for Apple and Ant! Let's practice saying A together with our friends!"
                }
            ]
        }
        
        # Generate test video
        video_project = video_service.create_educational_video(test_content)
        
        # Get video info
        video_info = video_service.get_video_info(video_project.project_id)
        
        result = {
            'test_status': 'completed',
            'project_id': video_project.project_id,
            'video_created': video_info is not None and video_info.get('exists', False),
            'video_info': video_info,
            'test_content': test_content,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Video generation test failed: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/cleanup', methods=['POST'])
def cleanup_temp_files():
    """Clean up temporary video files"""
    
    try:
        video_service.cleanup_temp_files()
        
        return jsonify({
            'message': 'Temporary files cleaned up successfully',
            'cleanup_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Cleanup failed: {str(e)}',
            'status': 'error'
        }), 500

@video_bp.route('/health', methods=['GET'])
def video_service_health():
    """Check video generation service health"""
    
    try:
        # Check if required directories exist
        directories_exist = all([
            os.path.exists(video_service.video_output_dir),
            os.path.exists(video_service.temp_dir),
            os.path.exists(video_service.assets_dir)
        ])
        
        # Check if ffmpeg is available
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            ffmpeg_available = True
        except:
            ffmpeg_available = False
        
        health_status = {
            'service': 'video_generation',
            'directories_exist': directories_exist,
            'ffmpeg_available': ffmpeg_available,
            'characters_loaded': len(video_service.main_characters),
            'visual_style': video_service.visual_style.value,
            'audio_style': video_service.audio_style.value,
            'healthy': directories_exist and ffmpeg_available,
            'timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            'service': 'video_generation',
            'healthy': False,
            'error': str(e),
            'status': 'error'
        }), 500

