"""
Media Generation API Routes
Handles AI-powered generation of visual and audio assets
"""

from flask import Blueprint, request, jsonify, send_file
from src.services.media_generation_service import MediaGenerationService
from src.models.media_generator import VisualStyle, AudioStyle
from datetime import datetime
import os

media_bp = Blueprint('media', __name__)

# Initialize media generation service
media_service = MediaGenerationService()

@media_bp.route('/generate/character', methods=['POST'])
def generate_character():
    """Generate character image using AI"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        character_name = data.get('character_name')
        style_str = data.get('style', 'bright_colorful')
        age_group = data.get('age_group', 'preschool')
        expression = data.get('expression', 'happy')
        
        if not character_name:
            return jsonify({
                'error': 'character_name is required',
                'status': 'error'
            }), 400
        
        # Convert style string to enum
        try:
            style = VisualStyle(style_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid style: {style_str}',
                'valid_styles': [s.value for s in VisualStyle],
                'status': 'error'
            }), 400
        
        # Generate character image
        asset = media_service.generate_character_image(
            character_name=character_name,
            style=style,
            age_group=age_group,
            expression=expression
        )
        
        # Convert to JSON-serializable format
        result = {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'description': asset.description,
            'style': asset.style.value,
            'file_path': asset.file_path,
            'metadata': asset.metadata,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Character generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/generate/background', methods=['POST'])
def generate_background():
    """Generate background image using AI"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        scene_description = data.get('scene_description')
        style_str = data.get('style', 'educational_clean')
        content_type = data.get('content_type', 'educational')
        
        if not scene_description:
            return jsonify({
                'error': 'scene_description is required',
                'status': 'error'
            }), 400
        
        # Convert style string to enum
        try:
            style = VisualStyle(style_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid style: {style_str}',
                'valid_styles': [s.value for s in VisualStyle],
                'status': 'error'
            }), 400
        
        # Generate background image
        asset = media_service.generate_background_image(
            scene_description=scene_description,
            style=style,
            content_type=content_type
        )
        
        result = {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'description': asset.description,
            'style': asset.style.value,
            'file_path': asset.file_path,
            'metadata': asset.metadata,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Background generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/generate/object', methods=['POST'])
def generate_educational_object():
    """Generate educational object image using AI"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        object_type = data.get('object_type')
        topic = data.get('topic')
        style_str = data.get('style', 'bright_colorful')
        
        if not all([object_type, topic]):
            return jsonify({
                'error': 'object_type and topic are required',
                'status': 'error'
            }), 400
        
        # Convert style string to enum
        try:
            style = VisualStyle(style_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid style: {style_str}',
                'valid_styles': [s.value for s in VisualStyle],
                'status': 'error'
            }), 400
        
        # Generate educational object
        asset = media_service.generate_educational_object(
            object_type=object_type,
            topic=topic,
            style=style
        )
        
        result = {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'description': asset.description,
            'style': asset.style.value,
            'file_path': asset.file_path,
            'metadata': asset.metadata,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Educational object generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/generate/music', methods=['POST'])
def generate_background_music():
    """Generate background music using AI"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        content_type = data.get('content_type')
        age_group = data.get('age_group', 'preschool')
        duration_minutes = data.get('duration_minutes', 5.0)
        style_str = data.get('style', 'upbeat_cheerful')
        
        if not content_type:
            return jsonify({
                'error': 'content_type is required',
                'status': 'error'
            }), 400
        
        # Convert style string to enum
        try:
            style = AudioStyle(style_str)
        except ValueError:
            return jsonify({
                'error': f'Invalid style: {style_str}',
                'valid_styles': [s.value for s in AudioStyle],
                'status': 'error'
            }), 400
        
        # Generate background music
        asset = media_service.generate_background_music(
            content_type=content_type,
            age_group=age_group,
            duration_minutes=float(duration_minutes),
            style=style
        )
        
        result = {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'description': asset.description,
            'style': asset.style.value,
            'file_path': asset.file_path,
            'duration_seconds': asset.duration_seconds,
            'metadata': asset.metadata,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Music generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/generate/voice', methods=['POST'])
def generate_voice_narration():
    """Generate voice narration using AI"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        script_text = data.get('script_text')
        character_name = data.get('character_name', 'Teacher Emma')
        age_group = data.get('age_group', 'preschool')
        
        if not script_text:
            return jsonify({
                'error': 'script_text is required',
                'status': 'error'
            }), 400
        
        # Generate voice narration
        asset = media_service.generate_voice_narration(
            script_text=script_text,
            character_name=character_name,
            age_group=age_group
        )
        
        result = {
            'asset_id': asset.asset_id,
            'asset_type': asset.asset_type,
            'description': asset.description,
            'style': asset.style.value,
            'file_path': asset.file_path,
            'duration_seconds': asset.duration_seconds,
            'metadata': asset.metadata,
            'generation_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Voice generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/generate/complete_assets', methods=['POST'])
def generate_complete_assets():
    """Generate all assets needed for a video"""
    
    try:
        data = request.get_json()
        
        # Required parameters
        content_data = data.get('content_data')
        visual_style_str = data.get('visual_style', 'bright_colorful')
        audio_style_str = data.get('audio_style', 'upbeat_cheerful')
        
        if not content_data:
            return jsonify({
                'error': 'content_data is required',
                'status': 'error'
            }), 400
        
        # Convert styles
        try:
            visual_style = VisualStyle(visual_style_str)
            audio_style = AudioStyle(audio_style_str)
        except ValueError as e:
            return jsonify({
                'error': f'Invalid style: {str(e)}',
                'status': 'error'
            }), 400
        
        # Extract content information
        topic = content_data.get('topic', 'learning')
        content_type = content_data.get('content_type', 'educational')
        age_group = content_data.get('age_group', 'preschool')
        character_list = content_data.get('character_list', ['Teacher Emma'])
        script_text = content_data.get('script_text', '')
        scene_descriptions = content_data.get('scene_descriptions', [])
        duration_minutes = content_data.get('duration_minutes', 5)
        
        generated_assets = {
            'visual_assets': {},
            'audio_assets': {},
            'generation_summary': {
                'total_assets': 0,
                'generation_time': datetime.now().isoformat(),
                'content_info': {
                    'topic': topic,
                    'content_type': content_type,
                    'age_group': age_group
                }
            }
        }
        
        # Generate character assets
        characters = []
        for character_name in character_list:
            try:
                character_asset = media_service.generate_character_image(
                    character_name=character_name,
                    style=visual_style,
                    age_group=age_group,
                    expression='happy'
                )
                characters.append({
                    'asset_id': character_asset.asset_id,
                    'character_name': character_name,
                    'file_path': character_asset.file_path,
                    'description': character_asset.description
                })
            except Exception as e:
                print(f"Failed to generate character {character_name}: {e}")
        
        generated_assets['visual_assets']['characters'] = characters
        
        # Generate background assets
        backgrounds = []
        for i, scene in enumerate(scene_descriptions):
            try:
                scene_desc = scene.get('description', f'Educational scene {i+1}')
                background_asset = media_service.generate_background_image(
                    scene_description=scene_desc,
                    style=visual_style,
                    content_type=content_type
                )
                backgrounds.append({
                    'asset_id': background_asset.asset_id,
                    'scene_number': i + 1,
                    'file_path': background_asset.file_path,
                    'description': background_asset.description
                })
            except Exception as e:
                print(f"Failed to generate background for scene {i+1}: {e}")
        
        generated_assets['visual_assets']['backgrounds'] = backgrounds
        
        # Generate educational object
        try:
            object_asset = media_service.generate_educational_object(
                object_type='educational_element',
                topic=topic,
                style=visual_style
            )
            generated_assets['visual_assets']['educational_objects'] = [{
                'asset_id': object_asset.asset_id,
                'topic': topic,
                'file_path': object_asset.file_path,
                'description': object_asset.description
            }]
        except Exception as e:
            print(f"Failed to generate educational object: {e}")
            generated_assets['visual_assets']['educational_objects'] = []
        
        # Generate background music
        try:
            music_asset = media_service.generate_background_music(
                content_type=content_type,
                age_group=age_group,
                duration_minutes=duration_minutes,
                style=audio_style
            )
            generated_assets['audio_assets']['background_music'] = {
                'asset_id': music_asset.asset_id,
                'file_path': music_asset.file_path,
                'duration_seconds': music_asset.duration_seconds,
                'description': music_asset.description
            }
        except Exception as e:
            print(f"Failed to generate background music: {e}")
            generated_assets['audio_assets']['background_music'] = None
        
        # Generate voice narration
        if script_text and character_list:
            try:
                voice_asset = media_service.generate_voice_narration(
                    script_text=script_text,
                    character_name=character_list[0],
                    age_group=age_group
                )
                generated_assets['audio_assets']['voice_narration'] = {
                    'asset_id': voice_asset.asset_id,
                    'character_name': character_list[0],
                    'file_path': voice_asset.file_path,
                    'duration_seconds': voice_asset.duration_seconds,
                    'description': voice_asset.description
                }
            except Exception as e:
                print(f"Failed to generate voice narration: {e}")
                generated_assets['audio_assets']['voice_narration'] = None
        
        # Calculate total assets generated
        total_assets = (
            len(generated_assets['visual_assets'].get('characters', [])) +
            len(generated_assets['visual_assets'].get('backgrounds', [])) +
            len(generated_assets['visual_assets'].get('educational_objects', [])) +
            (1 if generated_assets['audio_assets'].get('background_music') else 0) +
            (1 if generated_assets['audio_assets'].get('voice_narration') else 0)
        )
        
        generated_assets['generation_summary']['total_assets'] = total_assets
        generated_assets['status'] = 'success'
        
        return jsonify(generated_assets), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Complete asset generation failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/asset/<asset_id>', methods=['GET'])
def get_asset_info(asset_id):
    """Get information about a generated asset"""
    
    try:
        asset_info = media_service.get_asset_info(asset_id)
        
        if not asset_info:
            return jsonify({
                'error': f'Asset not found: {asset_id}',
                'status': 'error'
            }), 404
        
        return jsonify(asset_info), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Asset info retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/asset/<asset_id>/download', methods=['GET'])
def download_asset(asset_id):
    """Download a generated asset file"""
    
    try:
        asset_info = media_service.get_asset_info(asset_id)
        
        if not asset_info:
            return jsonify({
                'error': f'Asset not found: {asset_id}',
                'status': 'error'
            }), 404
        
        file_path = asset_info.get('file_path')
        if not file_path or not os.path.exists(file_path):
            return jsonify({
                'error': f'Asset file not found: {asset_id}',
                'status': 'error'
            }), 404
        
        return send_file(file_path, as_attachment=True)
        
    except Exception as e:
        return jsonify({
            'error': f'Asset download failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/styles', methods=['GET'])
def get_available_styles():
    """Get available visual and audio styles"""
    
    try:
        styles = {
            'visual_styles': [style.value for style in VisualStyle],
            'audio_styles': [style.value for style in AudioStyle],
            'style_descriptions': {
                'visual': {
                    style.value: {
                        'name': style.value,
                        'description': f'Visual style: {style.value.replace("_", " ").title()}'
                    } for style in VisualStyle
                },
                'audio': {
                    style.value: {
                        'name': style.value,
                        'description': f'Audio style: {style.value.replace("_", " ").title()}'
                    } for style in AudioStyle
                }
            },
            'status': 'success'
        }
        
        return jsonify(styles), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Style retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@media_bp.route('/cleanup', methods=['POST'])
def cleanup_old_assets():
    """Clean up old generated assets"""
    
    try:
        data = request.get_json() or {}
        days_old = data.get('days_old', 30)
        
        media_service.cleanup_old_assets(days_old)
        
        return jsonify({
            'message': f'Cleaned up assets older than {days_old} days',
            'cleanup_timestamp': datetime.now().isoformat(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Asset cleanup failed: {str(e)}',
            'status': 'error'
        }), 500

