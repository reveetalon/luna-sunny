"""
Content Generation API Routes
Handles requests for generating educational video content
"""

from flask import Blueprint, request, jsonify
from src.models.content_generator import ScriptGenerator, ContentRequest, ContentType, AgeGroup
from src.models.topic_selector import TopicSelector
import json

content_bp = Blueprint('content', __name__)

# Initialize generators
script_generator = ScriptGenerator()
topic_selector = TopicSelector()

@content_bp.route('/generate', methods=['POST'])
def generate_content():
    """Generate educational content based on request parameters"""
    
    try:
        data = request.get_json()
        
        # Parse request parameters
        topic = data.get('topic')
        content_type_str = data.get('content_type', 'alphabet')
        age_group_str = data.get('age_group', 'toddler')
        duration_minutes = data.get('duration_minutes', 5)
        learning_objectives = data.get('learning_objectives', [])
        style_preferences = data.get('style_preferences', {})
        
        # Convert string enums to enum objects
        try:
            content_type = ContentType(content_type_str)
            age_group = AgeGroup(age_group_str)
        except ValueError as e:
            return jsonify({
                'error': f'Invalid content_type or age_group: {str(e)}',
                'valid_content_types': [ct.value for ct in ContentType],
                'valid_age_groups': [ag.value for ag in AgeGroup]
            }), 400
        
        # Create content request
        content_request = ContentRequest(
            topic=topic,
            content_type=content_type,
            age_group=age_group,
            duration_minutes=duration_minutes,
            learning_objectives=learning_objectives,
            style_preferences=style_preferences
        )
        
        # Generate script
        generated_script = script_generator.generate_script(content_request)
        
        # Convert to JSON-serializable format
        result = {
            'title': generated_script.title,
            'content_type': generated_script.content_type.value,
            'age_group': generated_script.age_group.value,
            'duration_minutes': generated_script.duration_minutes,
            'script_text': generated_script.script_text,
            'scene_descriptions': generated_script.scene_descriptions,
            'audio_cues': generated_script.audio_cues,
            'learning_objectives': generated_script.learning_objectives,
            'character_list': generated_script.character_list,
            'generation_timestamp': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Content generation failed: {str(e)}',
            'status': 'error'
        }), 500

@content_bp.route('/generate/auto', methods=['POST'])
def generate_auto_content():
    """Generate content using autonomous topic selection"""
    
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
        
        # Select topic autonomously
        topic_selection = topic_selector.select_next_topic(target_age_group)
        
        # Determine duration based on age group and content type
        duration_map = {
            AgeGroup.TODDLER: 5,
            AgeGroup.PRESCHOOL: 8,
            AgeGroup.EARLY_ELEMENTARY: 12
        }
        duration_minutes = duration_map.get(topic_selection.age_group, 5)
        
        # Generate learning objectives based on content type
        learning_objectives = _generate_learning_objectives(
            topic_selection.content_type, 
            topic_selection.topic
        )
        
        # Create content request
        content_request = ContentRequest(
            topic=topic_selection.topic,
            content_type=topic_selection.content_type,
            age_group=topic_selection.age_group,
            duration_minutes=duration_minutes,
            learning_objectives=learning_objectives,
            style_preferences={}
        )
        
        # Generate script
        generated_script = script_generator.generate_script(content_request)
        
        # Convert to JSON-serializable format
        result = {
            'title': generated_script.title,
            'content_type': generated_script.content_type.value,
            'age_group': generated_script.age_group.value,
            'duration_minutes': generated_script.duration_minutes,
            'script_text': generated_script.script_text,
            'scene_descriptions': generated_script.scene_descriptions,
            'audio_cues': generated_script.audio_cues,
            'learning_objectives': generated_script.learning_objectives,
            'character_list': generated_script.character_list,
            'topic_selection_info': {
                'selected_topic': topic_selection.topic,
                'priority_score': topic_selection.priority_score,
                'selection_reason': topic_selection.selection_reason,
                'estimated_performance': topic_selection.estimated_performance
            },
            'generation_timestamp': str(datetime.now()),
            'status': 'success'
        }
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Auto content generation failed: {str(e)}',
            'status': 'error'
        }), 500

@content_bp.route('/templates', methods=['GET'])
def get_content_templates():
    """Get available content templates and categories"""
    
    try:
        templates = {
            'content_types': [ct.value for ct in ContentType],
            'age_groups': [ag.value for ag in AgeGroup],
            'template_structures': script_generator.templates,
            'character_database': script_generator.character_database
        }
        
        return jsonify(templates), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to retrieve templates: {str(e)}',
            'status': 'error'
        }), 500

@content_bp.route('/validate', methods=['POST'])
def validate_content():
    """Validate generated content for quality and appropriateness"""
    
    try:
        data = request.get_json()
        
        script_text = data.get('script_text', '')
        content_type_str = data.get('content_type', '')
        age_group_str = data.get('age_group', '')
        
        # Perform validation checks
        validation_results = {
            'length_appropriate': _validate_length(script_text, age_group_str),
            'content_safe': _validate_content_safety(script_text),
            'educational_value': _validate_educational_value(script_text, content_type_str),
            'age_appropriate': _validate_age_appropriateness(script_text, age_group_str),
            'overall_score': 0.0,
            'recommendations': []
        }
        
        # Calculate overall score
        scores = [v for k, v in validation_results.items() 
                 if k.endswith('_appropriate') or k.endswith('_safe') or k.endswith('_value')]
        validation_results['overall_score'] = sum(scores) / len(scores) if scores else 0.0
        
        # Generate recommendations
        if validation_results['overall_score'] < 0.8:
            validation_results['recommendations'].append('Consider revising content for better quality')
        
        return jsonify(validation_results), 200
        
    except Exception as e:
        return jsonify({
            'error': f'Content validation failed: {str(e)}',
            'status': 'error'
        }), 500

def _generate_learning_objectives(content_type: ContentType, topic: str) -> list:
    """Generate appropriate learning objectives for content"""
    
    objectives_map = {
        ContentType.ALPHABET: [
            f"Recognize the letter {topic.upper()}",
            f"Identify the sound of letter {topic.upper()}",
            f"Name words that start with {topic.upper()}"
        ],
        ContentType.NUMBERS: [
            f"Recognize the number {topic}",
            f"Count to {topic}",
            f"Understand quantity represented by {topic}"
        ],
        ContentType.COLORS: [
            f"Identify the color {topic}",
            f"Name objects that are {topic}",
            f"Distinguish {topic} from other colors"
        ],
        ContentType.BEHAVIOR: [
            f"Understand the importance of {topic}",
            f"Practice {topic} in daily life",
            f"Recognize when to apply {topic}"
        ]
    }
    
    return objectives_map.get(content_type, [f"Learn about {topic}"])

def _validate_length(script_text: str, age_group_str: str) -> float:
    """Validate script length for age appropriateness"""
    
    word_count = len(script_text.split())
    
    # Expected word counts by age group (words per minute * typical duration)
    expected_ranges = {
        'toddler': (200, 400),      # 2-3 words per second * 5 minutes
        'preschool': (400, 800),    # 2-3 words per second * 8 minutes  
        'early_elementary': (600, 1200)  # 2-3 words per second * 12 minutes
    }
    
    min_words, max_words = expected_ranges.get(age_group_str, (200, 400))
    
    if min_words <= word_count <= max_words:
        return 1.0
    elif word_count < min_words:
        return max(0.5, word_count / min_words)
    else:
        return max(0.5, max_words / word_count)

def _validate_content_safety(script_text: str) -> float:
    """Validate content for child safety"""
    
    # Check for inappropriate content indicators
    unsafe_keywords = [
        'scary', 'frightening', 'dangerous', 'violent', 'angry', 
        'sad', 'crying', 'hurt', 'pain', 'fear'
    ]
    
    text_lower = script_text.lower()
    unsafe_count = sum(1 for keyword in unsafe_keywords if keyword in text_lower)
    
    # Penalize based on unsafe content
    safety_score = max(0.0, 1.0 - (unsafe_count * 0.2))
    
    return safety_score

def _validate_educational_value(script_text: str, content_type_str: str) -> float:
    """Validate educational value of content"""
    
    # Check for educational keywords based on content type
    educational_keywords = {
        'alphabet': ['letter', 'sound', 'phonics', 'word', 'spell'],
        'numbers': ['count', 'number', 'quantity', 'math', 'add'],
        'colors': ['color', 'identify', 'recognize', 'see', 'look'],
        'behavior': ['learn', 'practice', 'good', 'right', 'important']
    }
    
    keywords = educational_keywords.get(content_type_str, [])
    text_lower = script_text.lower()
    
    keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
    educational_score = min(1.0, keyword_count / max(1, len(keywords)))
    
    return educational_score

def _validate_age_appropriateness(script_text: str, age_group_str: str) -> float:
    """Validate age appropriateness of language and concepts"""
    
    # Check vocabulary complexity
    complex_words = [
        'sophisticated', 'complicated', 'difficult', 'advanced',
        'complex', 'intricate', 'elaborate'
    ]
    
    text_lower = script_text.lower()
    complex_count = sum(1 for word in complex_words if word in text_lower)
    
    # Age group complexity tolerance
    complexity_tolerance = {
        'toddler': 0,
        'preschool': 1,
        'early_elementary': 2
    }
    
    max_complexity = complexity_tolerance.get(age_group_str, 0)
    
    if complex_count <= max_complexity:
        return 1.0
    else:
        return max(0.5, max_complexity / complex_count)

# Import datetime at the top
from datetime import datetime

