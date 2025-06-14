"""
Topic Selection Engine
Implements the autonomous topic selection algorithm
"""

import json
import random
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

from src.models.content_generator import ContentType, AgeGroup

@dataclass
class TopicPerformance:
    topic: str
    content_type: ContentType
    age_group: AgeGroup
    views: int
    watch_time_minutes: float
    engagement_rate: float
    retention_rate: float
    last_used: datetime
    success_score: float

@dataclass
class TopicSelection:
    topic: str
    content_type: ContentType
    age_group: AgeGroup
    priority_score: float
    selection_reason: str
    estimated_performance: Dict[str, float]

class TopicSelector:
    """Autonomous topic selection engine based on performance data and strategy"""
    
    def __init__(self):
        self.performance_database = self._initialize_performance_database()
        self.topic_categories = self._load_topic_categories()
        self.selection_weights = self._load_selection_weights()
        self.diversity_tracker = self._initialize_diversity_tracker()
    
    def select_next_topic(self, target_age_group: Optional[AgeGroup] = None) -> TopicSelection:
        """Select the next topic for content generation"""
        
        # Get candidate topics
        candidates = self._get_candidate_topics(target_age_group)
        
        # Calculate scores for each candidate
        scored_candidates = []
        for candidate in candidates:
            score = self._calculate_topic_score(candidate)
            scored_candidates.append((candidate, score))
        
        # Sort by score and apply diversity filters
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Select top candidate with diversity consideration
        selected_topic = self._apply_diversity_selection(scored_candidates)
        
        # Update diversity tracker
        self._update_diversity_tracker(selected_topic)
        
        return selected_topic
    
    def update_performance_data(self, topic: str, content_type: ContentType, 
                               age_group: AgeGroup, performance_metrics: Dict[str, float]):
        """Update performance data for a topic"""
        
        key = f"{topic}_{content_type.value}_{age_group.value}"
        
        if key in self.performance_database:
            # Update existing performance data
            perf = self.performance_database[key]
            perf.views += performance_metrics.get('views', 0)
            perf.watch_time_minutes += performance_metrics.get('watch_time', 0)
            perf.engagement_rate = (perf.engagement_rate + performance_metrics.get('engagement_rate', 0)) / 2
            perf.retention_rate = (perf.retention_rate + performance_metrics.get('retention_rate', 0)) / 2
            perf.success_score = self._calculate_success_score(perf)
        else:
            # Create new performance entry
            self.performance_database[key] = TopicPerformance(
                topic=topic,
                content_type=content_type,
                age_group=age_group,
                views=performance_metrics.get('views', 0),
                watch_time_minutes=performance_metrics.get('watch_time', 0),
                engagement_rate=performance_metrics.get('engagement_rate', 0),
                retention_rate=performance_metrics.get('retention_rate', 0),
                last_used=datetime.now(),
                success_score=0
            )
            self.performance_database[key].success_score = self._calculate_success_score(
                self.performance_database[key]
            )
    
    def get_performance_analytics(self) -> Dict[str, Any]:
        """Get comprehensive performance analytics"""
        
        analytics = {
            "total_topics": len(self.performance_database),
            "top_performing_topics": self._get_top_performers(10),
            "content_type_performance": self._analyze_content_type_performance(),
            "age_group_performance": self._analyze_age_group_performance(),
            "recent_trends": self._analyze_recent_trends(),
            "diversity_metrics": self._calculate_diversity_metrics()
        }
        
        return analytics
    
    def _initialize_performance_database(self) -> Dict[str, TopicPerformance]:
        """Initialize performance database with baseline data"""
        
        # Simulate historical performance data based on research
        baseline_topics = [
            # Alphabet topics
            ("A", ContentType.ALPHABET, AgeGroup.TODDLER, 1500000, 4.2, 0.85, 0.78),
            ("B", ContentType.ALPHABET, AgeGroup.TODDLER, 1200000, 3.8, 0.82, 0.75),
            ("C", ContentType.ALPHABET, AgeGroup.PRESCHOOL, 1800000, 5.1, 0.88, 0.82),
            
            # Number topics
            ("1", ContentType.NUMBERS, AgeGroup.TODDLER, 2100000, 4.5, 0.89, 0.84),
            ("2", ContentType.NUMBERS, AgeGroup.TODDLER, 1900000, 4.3, 0.87, 0.81),
            ("3", ContentType.NUMBERS, AgeGroup.PRESCHOOL, 1700000, 5.2, 0.86, 0.79),
            
            # Color topics
            ("red", ContentType.COLORS, AgeGroup.TODDLER, 2500000, 4.8, 0.91, 0.87),
            ("blue", ContentType.COLORS, AgeGroup.TODDLER, 2200000, 4.6, 0.89, 0.85),
            ("yellow", ContentType.COLORS, AgeGroup.PRESCHOOL, 1600000, 5.0, 0.84, 0.80),
            
            # Behavioral topics
            ("sharing", ContentType.BEHAVIOR, AgeGroup.PRESCHOOL, 2800000, 6.2, 0.93, 0.89),
            ("bedtime", ContentType.BEHAVIOR, AgeGroup.TODDLER, 3200000, 5.8, 0.95, 0.92),
            ("eating vegetables", ContentType.BEHAVIOR, AgeGroup.PRESCHOOL, 2600000, 5.9, 0.91, 0.88),
        ]
        
        database = {}
        for topic, content_type, age_group, views, watch_time, engagement, retention in baseline_topics:
            key = f"{topic}_{content_type.value}_{age_group.value}"
            perf = TopicPerformance(
                topic=topic,
                content_type=content_type,
                age_group=age_group,
                views=views,
                watch_time_minutes=watch_time,
                engagement_rate=engagement,
                retention_rate=retention,
                last_used=datetime.now() - timedelta(days=random.randint(1, 30)),
                success_score=0
            )
            perf.success_score = self._calculate_success_score(perf)
            database[key] = perf
        
        return database
    
    def _load_topic_categories(self) -> Dict[ContentType, List[str]]:
        """Load available topics for each content category"""
        
        return {
            ContentType.ALPHABET: [chr(i) for i in range(ord('A'), ord('Z') + 1)],
            ContentType.NUMBERS: [str(i) for i in range(1, 21)],
            ContentType.COLORS: ["red", "blue", "yellow", "green", "orange", "purple", "pink", "brown", "black", "white"],
            ContentType.SHAPES: ["circle", "square", "triangle", "rectangle", "oval", "diamond", "star", "heart"],
            ContentType.BEHAVIOR: [
                "sharing", "bedtime", "eating vegetables", "brushing teeth", "cleaning up",
                "saying please", "saying thank you", "helping others", "being kind", "listening"
            ],
            ContentType.SOCIAL: [
                "making friends", "playing together", "taking turns", "being patient",
                "expressing feelings", "solving problems", "being brave", "trying new things"
            ],
            ContentType.NURSERY_RHYME: [
                "twinkle twinkle little star", "wheels on the bus", "old macdonald",
                "if you're happy and you know it", "head shoulders knees and toes"
            ]
        }
    
    def _load_selection_weights(self) -> Dict[str, float]:
        """Load weighting factors for topic selection algorithm"""
        
        return {
            "performance_weight": 0.4,  # Historical performance importance
            "freshness_weight": 0.2,    # Time since last use
            "diversity_weight": 0.2,    # Content diversity maintenance
            "educational_weight": 0.1,  # Educational value priority
            "seasonal_weight": 0.1      # Seasonal relevance
        }
    
    def _initialize_diversity_tracker(self) -> Dict[str, Any]:
        """Initialize diversity tracking for balanced content selection"""
        
        return {
            "recent_content_types": [],
            "recent_age_groups": [],
            "recent_topics": [],
            "content_type_counts": {ct.value: 0 for ct in ContentType},
            "age_group_counts": {ag.value: 0 for ag in AgeGroup}
        }
    
    def _get_candidate_topics(self, target_age_group: Optional[AgeGroup] = None) -> List[Dict[str, Any]]:
        """Get list of candidate topics for selection"""
        
        candidates = []
        
        for content_type, topics in self.topic_categories.items():
            for topic in topics:
                age_groups = [target_age_group] if target_age_group else list(AgeGroup)
                
                for age_group in age_groups:
                    candidates.append({
                        "topic": topic,
                        "content_type": content_type,
                        "age_group": age_group
                    })
        
        return candidates
    
    def _calculate_topic_score(self, candidate: Dict[str, Any]) -> float:
        """Calculate priority score for a topic candidate"""
        
        topic = candidate["topic"]
        content_type = candidate["content_type"]
        age_group = candidate["age_group"]
        
        # Get performance data
        key = f"{topic}_{content_type.value}_{age_group.value}"
        performance = self.performance_database.get(key)
        
        # Calculate component scores
        performance_score = self._calculate_performance_score(performance)
        freshness_score = self._calculate_freshness_score(performance)
        diversity_score = self._calculate_diversity_score(content_type, age_group)
        educational_score = self._calculate_educational_score(content_type, topic)
        seasonal_score = self._calculate_seasonal_score(topic, content_type)
        
        # Weighted total score
        total_score = (
            performance_score * self.selection_weights["performance_weight"] +
            freshness_score * self.selection_weights["freshness_weight"] +
            diversity_score * self.selection_weights["diversity_weight"] +
            educational_score * self.selection_weights["educational_weight"] +
            seasonal_score * self.selection_weights["seasonal_weight"]
        )
        
        return total_score
    
    def _calculate_performance_score(self, performance: Optional[TopicPerformance]) -> float:
        """Calculate performance-based score"""
        
        if not performance:
            return 0.5  # Neutral score for new topics
        
        # Normalize metrics to 0-1 scale
        view_score = min(performance.views / 5000000, 1.0)  # Max 5M views = 1.0
        engagement_score = performance.engagement_rate
        retention_score = performance.retention_rate
        
        return (view_score + engagement_score + retention_score) / 3
    
    def _calculate_freshness_score(self, performance: Optional[TopicPerformance]) -> float:
        """Calculate freshness score based on time since last use"""
        
        if not performance:
            return 1.0  # New topics get max freshness
        
        days_since_use = (datetime.now() - performance.last_used).days
        
        # Score increases with time since last use
        if days_since_use >= 30:
            return 1.0
        elif days_since_use >= 14:
            return 0.8
        elif days_since_use >= 7:
            return 0.6
        elif days_since_use >= 3:
            return 0.4
        else:
            return 0.2
    
    def _calculate_diversity_score(self, content_type: ContentType, age_group: AgeGroup) -> float:
        """Calculate diversity score to maintain content balance"""
        
        # Check recent content type usage
        recent_content_types = self.diversity_tracker["recent_content_types"][-10:]
        content_type_frequency = recent_content_types.count(content_type.value)
        
        # Check recent age group usage
        recent_age_groups = self.diversity_tracker["recent_age_groups"][-10:]
        age_group_frequency = recent_age_groups.count(age_group.value)
        
        # Lower frequency = higher diversity score
        content_diversity = max(0, 1.0 - (content_type_frequency / 10))
        age_diversity = max(0, 1.0 - (age_group_frequency / 10))
        
        return (content_diversity + age_diversity) / 2
    
    def _calculate_educational_score(self, content_type: ContentType, topic: str) -> float:
        """Calculate educational value score"""
        
        # Priority scores for different content types
        educational_priorities = {
            ContentType.ALPHABET: 0.9,
            ContentType.NUMBERS: 0.9,
            ContentType.BEHAVIOR: 0.95,
            ContentType.COLORS: 0.8,
            ContentType.SHAPES: 0.8,
            ContentType.SOCIAL: 0.85,
            ContentType.NURSERY_RHYME: 0.7
        }
        
        return educational_priorities.get(content_type, 0.7)
    
    def _calculate_seasonal_score(self, topic: str, content_type: ContentType) -> float:
        """Calculate seasonal relevance score"""
        
        current_month = datetime.now().month
        
        # Seasonal topic boosts
        seasonal_boosts = {
            # Back to school (August-September)
            (8, 9): {"alphabet", "numbers", "colors", "shapes"},
            # Holiday season (November-December)
            (11, 12): {"sharing", "being kind", "helping others"},
            # Spring (March-May)
            (3, 4, 5): {"colors", "flowers", "animals"},
            # Summer (June-August)
            (6, 7, 8): {"playing together", "outdoor activities"}
        }
        
        for months, boosted_topics in seasonal_boosts.items():
            if current_month in months and topic.lower() in boosted_topics:
                return 1.0
        
        return 0.5  # Neutral seasonal score
    
    def _apply_diversity_selection(self, scored_candidates: List[tuple]) -> TopicSelection:
        """Apply diversity filters to candidate selection"""
        
        # Take top 5 candidates and apply diversity selection
        top_candidates = scored_candidates[:5]
        
        # Prefer candidates that improve diversity
        for candidate, score in top_candidates:
            content_type = candidate["content_type"]
            age_group = candidate["age_group"]
            
            # Check if this improves diversity
            if self._improves_diversity(content_type, age_group):
                return TopicSelection(
                    topic=candidate["topic"],
                    content_type=content_type,
                    age_group=age_group,
                    priority_score=score,
                    selection_reason="High performance with diversity benefit",
                    estimated_performance=self._estimate_performance(candidate)
                )
        
        # If no diversity benefit, select top performer
        best_candidate, best_score = top_candidates[0]
        return TopicSelection(
            topic=best_candidate["topic"],
            content_type=best_candidate["content_type"],
            age_group=best_candidate["age_group"],
            priority_score=best_score,
            selection_reason="Top performance score",
            estimated_performance=self._estimate_performance(best_candidate)
        )
    
    def _improves_diversity(self, content_type: ContentType, age_group: AgeGroup) -> bool:
        """Check if selection improves content diversity"""
        
        recent_content_types = self.diversity_tracker["recent_content_types"][-5:]
        recent_age_groups = self.diversity_tracker["recent_age_groups"][-5:]
        
        # Improves diversity if not recently used
        return (content_type.value not in recent_content_types or 
                age_group.value not in recent_age_groups)
    
    def _update_diversity_tracker(self, selection: TopicSelection):
        """Update diversity tracking with new selection"""
        
        self.diversity_tracker["recent_content_types"].append(selection.content_type.value)
        self.diversity_tracker["recent_age_groups"].append(selection.age_group.value)
        self.diversity_tracker["recent_topics"].append(selection.topic)
        
        # Keep only recent history
        for key in ["recent_content_types", "recent_age_groups", "recent_topics"]:
            if len(self.diversity_tracker[key]) > 20:
                self.diversity_tracker[key] = self.diversity_tracker[key][-20:]
        
        # Update counts
        self.diversity_tracker["content_type_counts"][selection.content_type.value] += 1
        self.diversity_tracker["age_group_counts"][selection.age_group.value] += 1
    
    def _estimate_performance(self, candidate: Dict[str, Any]) -> Dict[str, float]:
        """Estimate performance metrics for a candidate"""
        
        key = f"{candidate['topic']}_{candidate['content_type'].value}_{candidate['age_group'].value}"
        performance = self.performance_database.get(key)
        
        if performance:
            return {
                "estimated_views": performance.views * 1.1,  # Slight growth expectation
                "estimated_watch_time": performance.watch_time_minutes,
                "estimated_engagement": performance.engagement_rate,
                "estimated_retention": performance.retention_rate
            }
        else:
            # Estimates for new topics based on content type averages
            return {
                "estimated_views": 1000000,
                "estimated_watch_time": 4.0,
                "estimated_engagement": 0.8,
                "estimated_retention": 0.75
            }
    
    def _calculate_success_score(self, performance: TopicPerformance) -> float:
        """Calculate overall success score for a topic"""
        
        # Weighted combination of metrics
        view_weight = 0.3
        engagement_weight = 0.3
        retention_weight = 0.4
        
        # Normalize views (max 5M = 1.0)
        view_score = min(performance.views / 5000000, 1.0)
        
        success_score = (
            view_score * view_weight +
            performance.engagement_rate * engagement_weight +
            performance.retention_rate * retention_weight
        )
        
        return success_score
    
    def _get_top_performers(self, limit: int) -> List[Dict[str, Any]]:
        """Get top performing topics"""
        
        sorted_topics = sorted(
            self.performance_database.values(),
            key=lambda x: x.success_score,
            reverse=True
        )
        
        return [
            {
                "topic": topic.topic,
                "content_type": topic.content_type.value,
                "age_group": topic.age_group.value,
                "success_score": topic.success_score,
                "views": topic.views,
                "engagement_rate": topic.engagement_rate
            }
            for topic in sorted_topics[:limit]
        ]
    
    def _analyze_content_type_performance(self) -> Dict[str, float]:
        """Analyze performance by content type"""
        
        type_performance = {}
        
        for content_type in ContentType:
            topics = [p for p in self.performance_database.values() 
                     if p.content_type == content_type]
            
            if topics:
                avg_score = sum(t.success_score for t in topics) / len(topics)
                type_performance[content_type.value] = avg_score
            else:
                type_performance[content_type.value] = 0.0
        
        return type_performance
    
    def _analyze_age_group_performance(self) -> Dict[str, float]:
        """Analyze performance by age group"""
        
        age_performance = {}
        
        for age_group in AgeGroup:
            topics = [p for p in self.performance_database.values() 
                     if p.age_group == age_group]
            
            if topics:
                avg_score = sum(t.success_score for t in topics) / len(topics)
                age_performance[age_group.value] = avg_score
            else:
                age_performance[age_group.value] = 0.0
        
        return age_performance
    
    def _analyze_recent_trends(self) -> Dict[str, Any]:
        """Analyze recent performance trends"""
        
        recent_cutoff = datetime.now() - timedelta(days=30)
        recent_topics = [p for p in self.performance_database.values() 
                        if p.last_used >= recent_cutoff]
        
        if not recent_topics:
            return {"trend": "insufficient_data"}
        
        avg_recent_score = sum(t.success_score for t in recent_topics) / len(recent_topics)
        all_avg_score = sum(t.success_score for t in self.performance_database.values()) / len(self.performance_database)
        
        trend_direction = "improving" if avg_recent_score > all_avg_score else "declining"
        
        return {
            "trend": trend_direction,
            "recent_average_score": avg_recent_score,
            "overall_average_score": all_avg_score,
            "recent_topic_count": len(recent_topics)
        }
    
    def _calculate_diversity_metrics(self) -> Dict[str, Any]:
        """Calculate content diversity metrics"""
        
        return {
            "content_type_distribution": self.diversity_tracker["content_type_counts"],
            "age_group_distribution": self.diversity_tracker["age_group_counts"],
            "recent_diversity_score": len(set(self.diversity_tracker["recent_content_types"][-10:])) / min(10, len(ContentType))
        }

