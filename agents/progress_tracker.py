"""
Progress Tracker - Monitor learning journey.

ROLE:
Store quiz results, lesson completions, time spent.
Generate progress reports and identify weak areas.

STORAGE:
Uses TinyDB to persist progress data
"""

from tinydb import TinyDB
from datetime import datetime
from typing import Dict, List

class ProgressTracker:
    def __init__(self, db_path: str = "memory/progress_store.json"):
        self.db = TinyDB(db_path)
        self.progress = self.db.table("progress")
        
    def log_quiz_result(self, topic: str, score: float, total: int, 
                       quiz_questions: List[Dict]):
        """
        Log a completed quiz result.
        
        Args:
            topic: Subject of quiz
            score: Number correct
            total: Total questions
            quiz_questions: Full question list for review
        """
        self.progress.insert({
            "type": "quiz",
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": (score / total) * 100 if total > 0 else 0,
            "timestamp": datetime.now().isoformat(),
            "questions": quiz_questions
        })
        
    def log_lesson_complete(self, topic: str, lesson_name: str, 
                           time_spent_minutes: int):
        """Log lesson completion."""
        self.progress.insert({
            "type": "lesson_complete",
            "topic": topic,
            "lesson": lesson_name,
            "time_spent": time_spent_minutes,
            "timestamp": datetime.now().isoformat()
        })
        
    def get_topic_progress(self, topic: str) -> Dict:
        """
        Get progress summary for a topic.
        
        Returns:
            Dict with quiz scores, lessons completed, time spent
        """
        topic_progress = [p for p in self.progress.all() 
                         if p.get("topic") == topic]
                         
        quizzes = [p for p in topic_progress if p["type"] == "quiz"]
        lessons = [p for p in topic_progress if p["type"] == "lesson_complete"]
        
        avg_score = sum(q["percentage"] for q in quizzes) / len(quizzes) if quizzes else 0
        total_time = sum(l.get("time_spent", 0) for l in lessons)
        
        return {
            "topic": topic,
            "quizzes_taken": len(quizzes),
            "average_quiz_score": avg_score,
            "lessons_completed": len(lessons),
            "total_time_minutes": total_time
        }
        
    def get_weak_areas(self, topic: str = None) -> List[Dict]:
        """
        Identify topics/areas where user struggles.
        
        Returns:
            List of weak areas sorted by lowest scores
        """
        data = self.progress.all()
        
        if topic:
            data = [d for d in data if d.get("topic") == topic]
            
        quizzes = [d for d in data if d["type"] == "quiz"]
        
        # Group by topic and calculate averages
        topic_scores = {}
        for q in quizzes:
            t = q["topic"]
            if t not in topic_scores:
                topic_scores[t] = []
            topic_scores[t].append(q["percentage"])
            
        weak_areas = []
        for t, scores in topic_scores.items():
            avg = sum(scores) / len(scores)
            if avg < 70:  # Below 70% is struggling
                weak_areas.append({
                    "topic": t,
                    "average_score": avg,
                    "attempts": len(scores)
                })
                
        return sorted(weak_areas, key=lambda x: x["average_score"])

    def get_all_topics(self) -> List[str]:
        """Return a list of all unique topics in progress history."""
        data = self.progress.all()
        topics = set(d.get("topic") for d in data if "topic" in d)
        return list(topics)
