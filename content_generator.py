"""
Content Generation Pipeline Core Classes
Handles the AI-powered generation of educational video content
"""

import json
import random
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ContentType(Enum):
    ALPHABET = "alphabet"
    NUMBERS = "numbers"
    COLORS = "colors"
    SHAPES = "shapes"
    BEHAVIOR = "behavior"
    SOCIAL = "social"
    NURSERY_RHYME = "nursery_rhyme"

class AgeGroup(Enum):
    TODDLER = "toddler"  # 2-3 years
    PRESCHOOL = "preschool"  # 4-5 years
    EARLY_ELEMENTARY = "early_elementary"  # 6-8 years

@dataclass
class ContentRequest:
    topic: str
    content_type: ContentType
    age_group: AgeGroup
    duration_minutes: int
    learning_objectives: List[str]
    style_preferences: Dict[str, Any]

@dataclass
class GeneratedScript:
    title: str
    content_type: ContentType
    age_group: AgeGroup
    duration_minutes: int
    script_text: str
    scene_descriptions: List[Dict[str, Any]]
    audio_cues: List[Dict[str, Any]]
    learning_objectives: List[str]
    character_list: List[str]

class ScriptGenerator:
    """Generates educational scripts based on content templates and AI"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.character_database = self._load_characters()
    
    def generate_script(self, request: ContentRequest) -> GeneratedScript:
        """Generate a complete script based on the content request"""
        
        # Select appropriate template
        template = self._select_template(request.content_type, request.age_group)
        
        # Generate core content
        script_content = self._generate_content(request, template)
        
        # Create scene descriptions
        scenes = self._generate_scenes(script_content, request)
        
        # Generate audio cues
        audio_cues = self._generate_audio_cues(script_content, request)
        
        # Select characters
        characters = self._select_characters(request)
        
        return GeneratedScript(
            title=self._generate_title(request),
            content_type=request.content_type,
            age_group=request.age_group,
            duration_minutes=request.duration_minutes,
            script_text=script_content,
            scene_descriptions=scenes,
            audio_cues=audio_cues,
            learning_objectives=request.learning_objectives,
            character_list=characters
        )
    
    def _load_templates(self) -> Dict[str, Any]:
        """Load content templates for different educational topics"""
        return {
            ContentType.ALPHABET: {
                "structure": ["introduction", "letter_presentation", "phonics", "examples", "practice", "conclusion"],
                "duration_per_section": {"toddler": 1, "preschool": 1.5, "early_elementary": 2},
                "repetition_factor": {"toddler": 3, "preschool": 2, "early_elementary": 1}
            },
            ContentType.NUMBERS: {
                "structure": ["introduction", "number_presentation", "counting", "examples", "practice", "conclusion"],
                "duration_per_section": {"toddler": 1, "preschool": 1.5, "early_elementary": 2},
                "repetition_factor": {"toddler": 3, "preschool": 2, "early_elementary": 1}
            },
            ContentType.COLORS: {
                "structure": ["introduction", "color_presentation", "identification", "examples", "practice", "conclusion"],
                "duration_per_section": {"toddler": 1, "preschool": 1.5, "early_elementary": 2},
                "repetition_factor": {"toddler": 3, "preschool": 2, "early_elementary": 1}
            },
            ContentType.BEHAVIOR: {
                "structure": ["introduction", "problem_presentation", "solution_demonstration", "practice", "reinforcement", "conclusion"],
                "duration_per_section": {"toddler": 1.5, "preschool": 2, "early_elementary": 2.5},
                "repetition_factor": {"toddler": 2, "preschool": 2, "early_elementary": 1}
            }
        }
    
    def _load_characters(self) -> Dict[str, Any]:
        """Load character database for consistent character usage"""
        return {
            "main_characters": [
                {"name": "Sunny", "type": "child", "personality": "curious", "age": "preschool"},
                {"name": "Luna", "type": "child", "personality": "helpful", "age": "preschool"},
                {"name": "Max", "type": "child", "personality": "energetic", "age": "toddler"},
                {"name": "Zoe", "type": "child", "personality": "creative", "age": "early_elementary"}
            ],
            "supporting_characters": [
                {"name": "Teacher Emma", "type": "adult", "role": "educator"},
                {"name": "Buddy", "type": "animal", "species": "dog", "personality": "friendly"},
                {"name": "Wise Owl", "type": "animal", "species": "owl", "personality": "knowledgeable"}
            ]
        }
    
    def _select_template(self, content_type: ContentType, age_group: AgeGroup) -> Dict[str, Any]:
        """Select appropriate template based on content type and age group"""
        return self.templates.get(content_type, self.templates[ContentType.ALPHABET])
    
    def _generate_content(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate the main script content using AI and templates"""
        
        # This would integrate with actual AI models in production
        # For now, using template-based generation
        
        if request.content_type == ContentType.ALPHABET:
            return self._generate_alphabet_script(request, template)
        elif request.content_type == ContentType.NUMBERS:
            return self._generate_numbers_script(request, template)
        elif request.content_type == ContentType.COLORS:
            return self._generate_colors_script(request, template)
        elif request.content_type == ContentType.BEHAVIOR:
            return self._generate_behavior_script(request, template)
        else:
            return self._generate_generic_script(request, template)
    
    def _generate_alphabet_script(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate alphabet learning script"""
        letter = request.topic.upper()
        
        script = f"""
TITLE: Learning the Letter {letter}

INTRODUCTION:
Hello, friends! Today we're going to learn about the letter {letter}!
Can you say "{letter}"? Let's say it together: {letter}!

LETTER PRESENTATION:
This is the letter {letter}. 
Look at the big {letter} and the little {letter.lower()}.
{letter} says "{self._get_letter_sound(letter)}".
Let's practice: {letter} says "{self._get_letter_sound(letter)}".

PHONICS PRACTICE:
{letter} makes the sound "{self._get_letter_sound(letter)}".
Listen carefully: "{self._get_letter_sound(letter)}", "{self._get_letter_sound(letter)}", "{self._get_letter_sound(letter)}".
Now you try! Say "{self._get_letter_sound(letter)}" with me!

EXAMPLES:
{letter} is for {self._get_letter_words(letter)[0]}!
{letter} is for {self._get_letter_words(letter)[1]}!
{letter} is for {self._get_letter_words(letter)[2]}!

PRACTICE:
Can you find the letter {letter}? Point to the {letter}!
Great job! You found the letter {letter}!

CONCLUSION:
Wonderful! Today we learned about the letter {letter}.
{letter} says "{self._get_letter_sound(letter)}".
Keep practicing, and we'll see you next time!
"""
        return script.strip()
    
    def _generate_numbers_script(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate number learning script"""
        number = request.topic
        
        script = f"""
TITLE: Learning the Number {number}

INTRODUCTION:
Hello, little learners! Today we're going to learn about the number {number}!
Can you say "{number}"? Let's count together!

NUMBER PRESENTATION:
This is the number {number}.
The number {number} means we have {number} things.
Let's look at the number {number} together!

COUNTING PRACTICE:
Let's count to {number}!
{self._generate_counting_sequence(int(number))}
Great job counting to {number}!

EXAMPLES:
Here are {number} {self._get_counting_objects()[0]}!
Let's count them: {self._generate_counting_sequence(int(number))}
Here are {number} {self._get_counting_objects()[1]}!
Let's count them again: {self._generate_counting_sequence(int(number))}

PRACTICE:
Can you show me {number} fingers?
Count with me: {self._generate_counting_sequence(int(number))}
Excellent! You know the number {number}!

CONCLUSION:
Amazing work! Today we learned about the number {number}.
Remember, {number} means {number} things.
Keep practicing your numbers!
"""
        return script.strip()
    
    def _generate_colors_script(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate color learning script"""
        color = request.topic.lower()
        
        script = f"""
TITLE: Learning the Color {color.title()}

INTRODUCTION:
Hello, colorful friends! Today we're going to learn about the color {color}!
Can you say "{color}"? Let's say it together: {color}!

COLOR PRESENTATION:
This is the color {color}.
Look around - can you see anything {color}?
{color.title()} is a beautiful color!

IDENTIFICATION:
Let's find {color} things!
Here's a {color} {self._get_color_objects(color)[0]}!
Here's a {color} {self._get_color_objects(color)[1]}!
Here's a {color} {self._get_color_objects(color)[2]}!

EXAMPLES:
{self._get_color_examples(color)}

PRACTICE:
Point to something {color}!
Can you find the {color} object?
Great job finding {color} things!

CONCLUSION:
Wonderful! Today we learned about the color {color}.
{color.title()} is everywhere around us!
Keep looking for {color} things!
"""
        return script.strip()
    
    def _generate_behavior_script(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate behavioral learning script"""
        behavior = request.topic.lower()
        
        script = f"""
TITLE: Learning About {behavior.title()}

INTRODUCTION:
Hello, wonderful friends! Today we're going to learn about {behavior}.
This is something very important for all of us!

PROBLEM PRESENTATION:
Sometimes we need to learn how to {behavior}.
Let's see what happens when we don't {behavior}.
Our friend Sunny is learning about {behavior} too!

SOLUTION DEMONSTRATION:
Watch how Sunny learns to {behavior}!
First, Sunny tries this way...
Then, Sunny learns the right way to {behavior}!

PRACTICE:
Now let's practice {behavior} together!
Can you show me how to {behavior}?
Great job! You're learning to {behavior}!

REINFORCEMENT:
When we {behavior}, good things happen!
Everyone feels happy when we {behavior}!
You're doing such a good job with {behavior}!

CONCLUSION:
Excellent work! Today we learned about {behavior}.
Remember to always try to {behavior}.
You're becoming so good at {behavior}!
"""
        return script.strip()
    
    def _generate_generic_script(self, request: ContentRequest, template: Dict[str, Any]) -> str:
        """Generate generic educational script"""
        topic = request.topic
        
        script = f"""
TITLE: Learning About {topic.title()}

INTRODUCTION:
Hello, amazing learners! Today we're going to explore {topic}!
Are you ready to learn something new and exciting?

MAIN CONTENT:
Let's discover all about {topic}!
There are so many interesting things to learn about {topic}.
Watch and listen as we explore {topic} together!

PRACTICE:
Now let's practice what we learned about {topic}!
Can you remember what we discovered about {topic}?
You're doing such a great job learning about {topic}!

CONCLUSION:
Fantastic! Today we learned about {topic}.
You did wonderful work exploring {topic} with us!
Keep being curious and keep learning!
"""
        return script.strip()
    
    def _generate_scenes(self, script_content: str, request: ContentRequest) -> List[Dict[str, Any]]:
        """Generate scene descriptions for visual content"""
        scenes = []
        
        # Parse script sections and create corresponding scenes
        sections = script_content.split('\n\n')
        
        for i, section in enumerate(sections):
            if section.strip():
                scene = {
                    "scene_id": i + 1,
                    "title": section.split(':')[0] if ':' in section else f"Scene {i + 1}",
                    "description": self._generate_scene_description(section, request),
                    "duration_seconds": self._calculate_scene_duration(section, request),
                    "visual_elements": self._generate_visual_elements(section, request),
                    "character_actions": self._generate_character_actions(section, request)
                }
                scenes.append(scene)
        
        return scenes
    
    def _generate_audio_cues(self, script_content: str, request: ContentRequest) -> List[Dict[str, Any]]:
        """Generate audio cues for music and sound effects"""
        audio_cues = []
        
        # Add intro music
        audio_cues.append({
            "type": "music",
            "name": "intro_theme",
            "start_time": 0,
            "duration": 10,
            "volume": 0.7,
            "fade_in": True
        })
        
        # Add educational content music
        audio_cues.append({
            "type": "music",
            "name": "learning_background",
            "start_time": 10,
            "duration": request.duration_minutes * 60 - 20,
            "volume": 0.3,
            "loop": True
        })
        
        # Add conclusion music
        audio_cues.append({
            "type": "music",
            "name": "outro_theme",
            "start_time": request.duration_minutes * 60 - 10,
            "duration": 10,
            "volume": 0.7,
            "fade_out": True
        })
        
        return audio_cues
    
    def _select_characters(self, request: ContentRequest) -> List[str]:
        """Select appropriate characters for the content"""
        characters = []
        
        # Select main character based on age group
        main_chars = [char for char in self.character_database["main_characters"] 
                     if char["age"] == request.age_group.value]
        if main_chars:
            characters.append(main_chars[0]["name"])
        
        # Add supporting character if needed
        if request.content_type in [ContentType.BEHAVIOR, ContentType.SOCIAL]:
            characters.append(self.character_database["supporting_characters"][0]["name"])
        
        return characters
    
    def _generate_title(self, request: ContentRequest) -> str:
        """Generate an engaging title for the content"""
        topic = request.topic.title()
        
        title_templates = {
            ContentType.ALPHABET: f"Learning the Letter {topic}",
            ContentType.NUMBERS: f"Counting with Number {topic}",
            ContentType.COLORS: f"Exploring the Color {topic}",
            ContentType.SHAPES: f"Discovering {topic} Shapes",
            ContentType.BEHAVIOR: f"Learning About {topic}",
            ContentType.SOCIAL: f"Social Skills: {topic}",
            ContentType.NURSERY_RHYME: f"Nursery Rhyme: {topic}"
        }
        
        return title_templates.get(request.content_type, f"Learning About {topic}")
    
    # Helper methods for content generation
    def _get_letter_sound(self, letter: str) -> str:
        """Get phonetic sound for a letter"""
        sounds = {
            'A': 'ah', 'B': 'buh', 'C': 'kuh', 'D': 'duh', 'E': 'eh',
            'F': 'fuh', 'G': 'guh', 'H': 'huh', 'I': 'ih', 'J': 'juh',
            'K': 'kuh', 'L': 'luh', 'M': 'muh', 'N': 'nuh', 'O': 'oh',
            'P': 'puh', 'Q': 'kwuh', 'R': 'ruh', 'S': 'sss', 'T': 'tuh',
            'U': 'uh', 'V': 'vuh', 'W': 'wuh', 'X': 'ks', 'Y': 'yuh', 'Z': 'zzz'
        }
        return sounds.get(letter.upper(), 'uh')
    
    def _get_letter_words(self, letter: str) -> List[str]:
        """Get example words for a letter"""
        words = {
            'A': ['apple', 'ant', 'airplane'],
            'B': ['ball', 'bear', 'banana'],
            'C': ['cat', 'car', 'cookie'],
            'D': ['dog', 'duck', 'door'],
            'E': ['elephant', 'egg', 'eye']
        }
        return words.get(letter.upper(), ['word1', 'word2', 'word3'])
    
    def _generate_counting_sequence(self, number: int) -> str:
        """Generate counting sequence up to number"""
        return ', '.join([str(i) for i in range(1, number + 1)])
    
    def _get_counting_objects(self) -> List[str]:
        """Get objects for counting examples"""
        return ['apples', 'balloons', 'toys', 'flowers', 'stars']
    
    def _get_color_objects(self, color: str) -> List[str]:
        """Get objects of a specific color"""
        objects = {
            'red': ['apple', 'fire truck', 'strawberry'],
            'blue': ['sky', 'ocean', 'blueberry'],
            'yellow': ['sun', 'banana', 'school bus'],
            'green': ['grass', 'tree', 'frog'],
            'orange': ['orange', 'pumpkin', 'carrot']
        }
        return objects.get(color, ['object1', 'object2', 'object3'])
    
    def _get_color_examples(self, color: str) -> str:
        """Get color examples text"""
        examples = {
            'red': 'Red is the color of roses and fire trucks!',
            'blue': 'Blue is the color of the sky and ocean!',
            'yellow': 'Yellow is the color of the sun and bananas!',
            'green': 'Green is the color of grass and trees!',
            'orange': 'Orange is the color of oranges and pumpkins!'
        }
        return examples.get(color, f'{color.title()} is a wonderful color!')
    
    def _generate_scene_description(self, section: str, request: ContentRequest) -> str:
        """Generate visual scene description"""
        return f"Animated scene for {request.content_type.value} content featuring colorful, child-friendly visuals"
    
    def _calculate_scene_duration(self, section: str, request: ContentRequest) -> int:
        """Calculate duration for scene in seconds"""
        word_count = len(section.split())
        # Assume 2 words per second for child-appropriate pacing
        return max(10, word_count // 2)
    
    def _generate_visual_elements(self, section: str, request: ContentRequest) -> List[str]:
        """Generate list of visual elements for scene"""
        return ["background", "characters", "educational_objects", "text_overlay"]
    
    def _generate_character_actions(self, section: str, request: ContentRequest) -> List[str]:
        """Generate character actions for scene"""
        return ["speaking", "gesturing", "interacting_with_objects"]

