"""
Pipeline Status and Monitoring API Routes
Handles system status, health checks, and monitoring
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import psutil
import os

status_bp = Blueprint('status', __name__)

@status_bp.route('/health', methods=['GET'])
def health_check():
    """Basic health check endpoint"""
    
    try:
        # Check system resources
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_status = {
            'status': 'healthy',
            'timestamp': str(datetime.now()),
            'system_resources': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available_gb': round(memory.available / (1024**3), 2),
                'disk_percent': disk.percent,
                'disk_free_gb': round(disk.free / (1024**3), 2)
            },
            'service_status': {
                'content_generator': 'operational',
                'topic_selector': 'operational',
                'api_server': 'operational'
            }
        }
        
        # Determine overall health
        if cpu_percent > 90 or memory.percent > 90 or disk.percent > 90:
            health_status['status'] = 'warning'
            health_status['warnings'] = []
            
            if cpu_percent > 90:
                health_status['warnings'].append('High CPU usage')
            if memory.percent > 90:
                health_status['warnings'].append('High memory usage')
            if disk.percent > 90:
                health_status['warnings'].append('Low disk space')
        
        return jsonify(health_status), 200
        
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Health check failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/status', methods=['GET'])
def pipeline_status():
    """Get detailed pipeline status and statistics"""
    
    try:
        # This would integrate with actual pipeline monitoring in production
        # For now, providing mock status data
        
        pipeline_stats = {
            'pipeline_status': 'running',
            'last_content_generated': str(datetime.now()),
            'content_generation_stats': {
                'total_videos_generated': 1247,
                'videos_generated_today': 24,
                'average_generation_time_minutes': 12.5,
                'success_rate_percent': 98.2,
                'queue_length': 3
            },
            'topic_selection_stats': {
                'total_topics_processed': 1247,
                'unique_topics_covered': 156,
                'average_selection_score': 0.847,
                'diversity_score': 0.923
            },
            'performance_metrics': {
                'average_views_per_video': 1850000,
                'average_watch_time_minutes': 4.8,
                'average_engagement_rate': 0.876,
                'average_retention_rate': 0.823
            },
            'system_uptime_hours': 168.5,
            'last_error': None,
            'timestamp': str(datetime.now())
        }
        
        return jsonify(pipeline_stats), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Pipeline status retrieval failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/metrics', methods=['GET'])
def pipeline_metrics():
    """Get detailed pipeline performance metrics"""
    
    try:
        # Time range for metrics
        time_range = request.args.get('range', '24h')  # 1h, 24h, 7d, 30d
        
        # Mock metrics data - in production this would come from monitoring systems
        metrics = {
            'time_range': time_range,
            'content_generation_metrics': {
                'generation_rate_per_hour': 1.0,
                'average_processing_time_minutes': 12.5,
                'success_rate': 0.982,
                'error_rate': 0.018,
                'queue_wait_time_minutes': 2.3
            },
            'quality_metrics': {
                'content_validation_pass_rate': 0.956,
                'average_educational_score': 0.891,
                'average_safety_score': 0.998,
                'average_age_appropriateness_score': 0.934
            },
            'performance_trends': {
                'view_growth_rate': 0.15,  # 15% growth
                'engagement_trend': 'increasing',
                'retention_trend': 'stable',
                'topic_diversity_trend': 'improving'
            },
            'resource_utilization': {
                'cpu_average_percent': 45.2,
                'memory_average_percent': 62.8,
                'storage_used_gb': 245.7,
                'network_bandwidth_mbps': 12.4
            },
            'generated_at': str(datetime.now())
        }
        
        return jsonify(metrics), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Metrics retrieval failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/logs', methods=['GET'])
def pipeline_logs():
    """Get recent pipeline logs"""
    
    try:
        # Log level filter
        level = request.args.get('level', 'all')  # all, info, warning, error
        limit = int(request.args.get('limit', 100))
        
        # Mock log data - in production this would come from actual log files
        mock_logs = [
            {
                'timestamp': str(datetime.now()),
                'level': 'info',
                'component': 'content_generator',
                'message': 'Successfully generated content for topic: Letter A (toddler)',
                'details': {'topic': 'A', 'content_type': 'alphabet', 'duration': '5 minutes'}
            },
            {
                'timestamp': str(datetime.now()),
                'level': 'info',
                'component': 'topic_selector',
                'message': 'Selected next topic based on performance analysis',
                'details': {'selected_topic': 'red', 'priority_score': 0.892}
            },
            {
                'timestamp': str(datetime.now()),
                'level': 'warning',
                'component': 'quality_validator',
                'message': 'Content validation score below optimal threshold',
                'details': {'validation_score': 0.78, 'threshold': 0.85}
            },
            {
                'timestamp': str(datetime.now()),
                'level': 'info',
                'component': 'performance_tracker',
                'message': 'Updated performance metrics for completed video',
                'details': {'views': 125000, 'engagement_rate': 0.89}
            }
        ]
        
        # Filter logs by level
        if level != 'all':
            mock_logs = [log for log in mock_logs if log['level'] == level]
        
        # Limit results
        mock_logs = mock_logs[:limit]
        
        result = {
            'logs': mock_logs,
            'total_logs': len(mock_logs),
            'filters': {
                'level': level,
                'limit': limit
            },
            'generated_at': str(datetime.now())
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Log retrieval failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/config', methods=['GET'])
def pipeline_config():
    """Get current pipeline configuration"""
    
    try:
        config = {
            'content_generation': {
                'generation_interval_minutes': 60,
                'max_queue_size': 10,
                'default_video_duration_minutes': 5,
                'quality_threshold': 0.85,
                'auto_retry_enabled': True,
                'max_retry_attempts': 3
            },
            'topic_selection': {
                'performance_weight': 0.4,
                'freshness_weight': 0.2,
                'diversity_weight': 0.2,
                'educational_weight': 0.1,
                'seasonal_weight': 0.1,
                'diversity_window_size': 10
            },
            'quality_assurance': {
                'content_validation_enabled': True,
                'safety_check_enabled': True,
                'educational_validation_enabled': True,
                'age_appropriateness_check_enabled': True,
                'minimum_validation_score': 0.8
            },
            'performance_tracking': {
                'metrics_collection_enabled': True,
                'analytics_update_interval_minutes': 15,
                'performance_history_retention_days': 365,
                'trend_analysis_enabled': True
            },
            'system_settings': {
                'max_concurrent_generations': 2,
                'resource_monitoring_enabled': True,
                'auto_scaling_enabled': False,
                'backup_enabled': True,
                'backup_interval_hours': 24
            },
            'generated_at': str(datetime.now())
        }
        
        return jsonify(config), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Configuration retrieval failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/config', methods=['POST'])
def update_pipeline_config():
    """Update pipeline configuration"""
    
    try:
        data = request.get_json()
        
        # In production, this would update actual configuration
        # For now, just validate the input and return success
        
        valid_sections = [
            'content_generation', 'topic_selection', 'quality_assurance',
            'performance_tracking', 'system_settings'
        ]
        
        updated_sections = []
        for section, config in data.items():
            if section in valid_sections:
                updated_sections.append(section)
                # Here you would update the actual configuration
        
        result = {
            'message': 'Configuration updated successfully',
            'updated_sections': updated_sections,
            'timestamp': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Configuration update failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

@status_bp.route('/pipeline/restart', methods=['POST'])
def restart_pipeline():
    """Restart pipeline components"""
    
    try:
        data = request.get_json() or {}
        component = data.get('component', 'all')  # all, content_generator, topic_selector
        
        # In production, this would actually restart components
        # For now, just simulate the restart
        
        restart_result = {
            'message': f'Pipeline component "{component}" restart initiated',
            'component': component,
            'restart_timestamp': str(datetime.now()),
            'estimated_downtime_seconds': 30,
            'status': 'success'
        }
        
        return jsonify(restart_result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Pipeline restart failed: {str(e)}',
            'timestamp': str(datetime.now())
        }), 500

