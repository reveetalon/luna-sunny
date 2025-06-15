
"""Publishing and Upload API Routes
Handles automated video uploading and publishing"""

from flask import Blueprint, request, jsonify, send_file
from src.services.automated_publishing_service import AutomatedPublishingService
from datetime import datetime
import os

publishing_bp = Blueprint('publishing', __name__)
publishing_service = AutomatedPublishingService()

@publishing_bp.route('/thumbnail/<path:thumbnail_path>')
def download_thumbnail(thumbnail_path):
    try:
        # SAFELY construct the full path using project-relative directory
        full_path = os.path.join(os.getcwd(), "generated_assets", "thumbnails", thumbnail_path)

        if not os.path.exists(full_path):
            return jsonify({'error': f'Thumbnail not found: {thumbnail_path}', 'status': 'error'}), 404

        return send_file(full_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'Thumbnail download failed: {str(e)}', 'status': 'error'}), 500

@publishing_bp.route('/test', methods=['POST'])
def test_publishing():
    try:
        # Use a relative path instead of /home/ubuntu
        test_video_dir = os.path.join(os.getcwd(), "generated_assets", "videos")
        os.makedirs(test_video_dir, exist_ok=True)
        test_video_path = os.path.join(test_video_dir, "test_publishing.mp4")

        if not os.path.exists(test_video_path):
            import subprocess
            cmd = [
                'ffmpeg', '-y',
                '-f', 'lavfi',
                '-i', 'color=c=lightgreen:size=1280x720:d=10',
                '-vf', 'drawtext=text='Publishing Test Video':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264',
                '-t', '10',
                test_video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return jsonify({'error': f'Failed to create test video: {result.stderr}', 'status': 'error'}), 500

        test_metadata = {
            "topic": "Publishing Test",
            "title": "Test Video for Publishing System",
            "content_type": "test",
            "age_group": "preschool",
            "characters": ["Luna", "Sunny"],
            "test_upload": True
        }

        upload_results = publishing_service.upload_video_to_all_platforms(test_video_path, test_metadata)
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
        return jsonify({'error': f'Publishing test failed: {str(e)}', 'status': 'error'}), 500
