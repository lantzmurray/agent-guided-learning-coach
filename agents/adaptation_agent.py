"""
Adaptation Agent - Personalize difficulty based on performance.

ROLE:
Analyze quiz results and learning progress to automatically 
adjust difficulty levels and recommend focus areas.

ADAPTATION STRATEGIES:
- If struggling (avg < 60%): Reduce difficulty, suggest review
- If succeeding (avg > 85%): Increase difficulty, skip basics
- If inconsistent: Focus on weak areas
"""

from agents.base import call_llm
from typing import Dict

def suggest_difficulty_adjustment(progress: Dict) -> Dict:
    """
    Analyze progress and suggest difficulty changes.
    
    Args:
        progress: Dict from ProgressTracker.get_topic_progress()
        
    Returns:
        Dict with: current_level, suggested_level, reasoning
    """
    score = progress.get("average_quiz_score", 70)
    
    if score < 60:
        return {
            "current_difficulty": "current assumption",
            "suggested_difficulty": "beginner",
            "reasoning": f"Score of {score:.0f}% suggests need for easier content",
            "action": "Review fundamentals before advancing"
        }
    elif score < 75:
        return {
            "current_difficulty": "current assumption",
            "suggested_difficulty": "intermediate",
            "reasoning": f"Score of {score:.0f}% indicates solid intermediate understanding",
            "action": "Continue with current pace, focus on weak areas"
        }
    elif score < 90:
        return {
            "current_difficulty": "current assumption",
            "suggested_difficulty": "intermediate",
            "reasoning": f"Score of {score:.0f}% shows strong intermediate mastery",
            "action": "Ready for advanced topics"
        }
    else:
        return {
            "current_difficulty": "current assumption",
            "suggested_difficulty": "advanced",
            "reasoning": f"Score of {score:.0f}% demonstrates mastery",
            "action": "Challenge with advanced projects"
        }

def generate_personalized_review(progress: Dict, weak_areas: list) -> str:
    """
    Generate a personalized review plan based on performance.
    
    Args:
        progress: Overall progress summary
        weak_areas: Areas needing work from ProgressTracker
        
    Returns:
        Review plan as text
    """
    weak_str = "\n".join([f"- {w['topic']} (avg: {w['average_score']:.0f}%)" 
                          for w in weak_areas])
                          
    prompt = f"""Create a personalized review plan based on this learning progress:

Overall Progress:
- Average Score: {progress.get('average_quiz_score', 0):.0f}%
- Quizzes Taken: {progress.get('quizzes_taken', 0)}
- Time Spent: {progress.get('total_time_minutes', 0)} minutes

Areas Needing Review:
{weak_str}

Provide a structured review plan that:
1. Prioritizes the weakest areas
2. Suggests specific topics to revisit
3. Estimates time needed
4. Recommends practice exercises
"""

    return call_llm(prompt)