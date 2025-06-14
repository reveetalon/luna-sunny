"""
Topic Selection API Routes
Handles autonomous topic selection and performance tracking
"""

from flask import Blueprint, request, jsonify
from src.models.topic_selector import TopicSelector, ContentType, AgeGroup
from datetime import datetime
import json

topic_bp = Blueprint('topics', __name__)

# Initialize topic selector
topic_selector = TopicSelector()

@topic_bp.route('/select', methods=['POST'])
def select_topic():
    """Select next topic for content generation"""
    
    try:
        data = request.get_json() or {}
        
        # Optional target age group
        target_age_group_str = data.get('target_age_group')
        target_age_group = None
        
        if target_age_group_str:
            try:
                target_age_group = AgeGroup(target_age_group_str)
            except ValueError:
                return jsonify({
                    'error': f'Invalid target_age_group: {target_age_group_str}',
                    'valid_age_groups': [ag.value for ag in AgeGroup]
                }), 400
        
        # Select topic
        selection = topic_selector.select_next_topic(target_age_group)
        
        # Convert to JSON-serializable format
        result = {
            'selected_topic': selection.topic,
            'content_type': selection.content_type.value,
            'age_group': selection.age_group.value,
            'priority_score': selection.priority_score,
            'selection_reason': selection.selection_reason,
            'estimated_performance': selection.estimated_performance,
            'selection_timestamp': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Topic selection failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/performance/update', methods=['POST'])
def update_performance():
    """Update performance data for a topic"""
    
    try:
        data = request.get_json()
        
        # Required fields
        topic = data.get('topic')
        content_type_str = data.get('content_type')
        age_group_str = data.get('age_group')
        performance_metrics = data.get('performance_metrics', {})
        
        if not all([topic, content_type_str, age_group_str]):
            return jsonify({
                'error': 'Missing required fields: topic, content_type, age_group',
                'status': 'error'
            }), 400
        
        # Convert string enums
        try:
            content_type = ContentType(content_type_str)
            age_group = AgeGroup(age_group_str)
        except ValueError as e:
            return jsonify({
                'error': f'Invalid content_type or age_group: {str(e)}',
                'valid_content_types': [ct.value for ct in ContentType],
                'valid_age_groups': [ag.value for ag in AgeGroup]
            }), 400
        
        # Validate performance metrics
        required_metrics = ['views', 'watch_time', 'engagement_rate', 'retention_rate']
        for metric in required_metrics:
            if metric not in performance_metrics:
                return jsonify({
                    'error': f'Missing performance metric: {metric}',
                    'required_metrics': required_metrics,
                    'status': 'error'
                }), 400
        
        # Update performance data
        topic_selector.update_performance_data(
            topic=topic,
            content_type=content_type,
            age_group=age_group,
            performance_metrics=performance_metrics
        )
        
        return jsonify({
            'message': 'Performance data updated successfully',
            'topic': topic,
            'content_type': content_type_str,
            'age_group': age_group_str,
            'update_timestamp': str(datetime.now()),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Performance update failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/analytics', methods=['GET'])
def get_analytics():
    """Get comprehensive performance analytics"""
    
    try:
        analytics = topic_selector.get_performance_analytics()
        
        # Add timestamp
        analytics['generated_at'] = str(datetime.now())
        analytics['status'] = 'success'
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Analytics retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/categories', methods=['GET'])
def get_topic_categories():
    """Get available topic categories and topics"""
    
    try:
        categories = {
            'content_types': [ct.value for ct in ContentType],
            'age_groups': [ag.value for ag in AgeGroup],
            'topic_categories': {
                ct.value: topics for ct, topics in topic_selector.topic_categories.items()
            },
            'selection_weights': topic_selector.selection_weights,
            'status': 'success'
        }
        
        return jsonify(categories), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Categories retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/performance/history', methods=['GET'])
def get_performance_history():
    """Get performance history for all topics"""
    
    try:
        # Get query parameters
        content_type_filter = request.args.get('content_type')
        age_group_filter = request.args.get('age_group')
        limit = int(request.args.get('limit', 50))
        
        # Filter performance data
        performance_data = []
        
        for key, perf in topic_selector.performance_database.items():
            # Apply filters
            if content_type_filter and perf.content_type.value != content_type_filter:
                continue
            if age_group_filter and perf.age_group.value != age_group_filter:
                continue
            
            performance_data.append({
                'topic': perf.topic,
                'content_type': perf.content_type.value,
                'age_group': perf.age_group.value,
                'views': perf.views,
                'watch_time_minutes': perf.watch_time_minutes,
                'engagement_rate': perf.engagement_rate,
                'retention_rate': perf.retention_rate,
                'success_score': perf.success_score,
                'last_used': str(perf.last_used)
            })
        
        # Sort by success score and limit results
        performance_data.sort(key=lambda x: x['success_score'], reverse=True)
        performance_data = performance_data[:limit]
        
        result = {
            'performance_history': performance_data,
            'total_topics': len(topic_selector.performance_database),
            'filtered_count': len(performance_data),
            'filters_applied': {
                'content_type': content_type_filter,
                'age_group': age_group_filter,
                'limit': limit
            },
            'generated_at': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Performance history retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/diversity/status', methods=['GET'])
def get_diversity_status():
    """Get current diversity status and recommendations"""
    
    try:
        diversity_data = topic_selector.diversity_tracker
        
        # Calculate diversity recommendations
        recommendations = []
        
        # Check content type balance
        content_counts = diversity_data['content_type_counts']
        total_content = sum(content_counts.values())
        
        if total_content > 0:
            for content_type, count in content_counts.items():
                percentage = (count / total_content) * 100
                if percentage > 40:
                    recommendations.append(f"Consider reducing {content_type} content (currently {percentage:.1f}%)")
                elif percentage < 10:
                    recommendations.append(f"Consider increasing {content_type} content (currently {percentage:.1f}%)")
        
        # Check recent diversity
        recent_types = set(diversity_data['recent_content_types'][-10:])
        if len(recent_types) < 3:
            recommendations.append("Recent content lacks diversity - consider varying content types")
        
        result = {
            'diversity_tracker': diversity_data,
            'diversity_score': len(recent_types) / min(10, len(ContentType)),
            'recommendations': recommendations,
            'content_type_percentages': {
                ct: (count / max(1, total_content)) * 100 
                for ct, count in content_counts.items()
            },
            'generated_at': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Diversity status retrieval failed: {str(e)}',
            'status': 'error'
        }), 500

@topic_bp.route('/simulate/selection', methods=['POST'])
def simulate_topic_selection():
    """Simulate topic selection for testing and optimization"""
    
    try:
        data = request.get_json() or {}
        
        # Number of selections to simulate
        num_selections = data.get('num_selections', 10)
        target_age_group_str = data.get('target_age_group')
        
        target_age_group = None
        if target_age_group_str:
            try:
                target_age_group = AgeGroup(target_age_group_str)
            except ValueError:
                return jsonify({
                    'error': f'Invalid target_age_group: {target_age_group_str}',
                    'valid_age_groups': [ag.value for ag in AgeGroup]
                }), 400
        
        # Simulate selections
        simulated_selections = []
        
        for i in range(num_selections):
            selection = topic_selector.select_next_topic(target_age_group)
            
            simulated_selections.append({
                'selection_number': i + 1,
                'topic': selection.topic,
                'content_type': selection.content_type.value,
                'age_group': selection.age_group.value,
                'priority_score': selection.priority_score,
                'selection_reason': selection.selection_reason
            })
        
        # Analyze simulation results
        content_type_distribution = {}
        age_group_distribution = {}
        
        for selection in simulated_selections:
            ct = selection['content_type']
            ag = selection['age_group']
            
            content_type_distribution[ct] = content_type_distribution.get(ct, 0) + 1
            age_group_distribution[ag] = age_group_distribution.get(ag, 0) + 1
        
        result = {
            'simulated_selections': simulated_selections,
            'simulation_analysis': {
                'content_type_distribution': content_type_distribution,
                'age_group_distribution': age_group_distribution,
                'diversity_score': len(set(s['content_type'] for s in simulated_selections)) / len(ContentType),
                'average_priority_score': sum(s['priority_score'] for s in simulated_selections) / len(simulated_selections)
            },
            'simulation_parameters': {
                'num_selections': num_selections,
                'target_age_group': target_age_group_str
            },
            'generated_at': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Topic selection simulation failed: {str(e)}',
            'status': 'error'
        }), 500

