"""
Learning Path Agent - Create structured learning curricula.

ROLE:
Takes a topic and creates an ordered sequence of lessons, 
each with objectives, resources, and exercises.

OUTPUT STRUCTURE:
- Modules (major sections)
- Lessons (within modules)
- Each lesson has: objective, content summary, exercises
"""

from agents.base import call_llm
from typing import List, Dict

def create_learning_path(topic: str, difficulty: str = "intermediate", 
                         time_commitment: str = "2 hours/week") -> Dict:
    """
    Create a personalized learning path.
    
    Args:
        topic: Subject to learn (e.g., "AWS Cloud Practitioner")
        difficulty: beginner, intermediate, or advanced
        time_commitment: Estimated weekly study time
        
    Returns:
        Dict with modules, lessons, objectives
    """
    prompt = f"""Create a comprehensive learning path for "{topic}" 
at the {difficulty} level assuming {time_commitment} of study time.

Structure the response as:
1. Overview (brief description of what will be learned)
2. Modules (3-5 major sections)
3. For each module, provide:
   - Module name
   - Lessons within (2-4 per module)
   - Learning objectives
   - Estimated time
   - Key concepts to master

Format as a structured outline that could be parsed into JSON.
"""

    response = call_llm(prompt)
    
    return {
        "topic": topic,
        "difficulty": difficulty,
        "time_commitment": time_commitment,
        "path_text": response
    }

def get_lesson_detail(lesson_name: str, topic: str) -> Dict:
    """
    Get detailed content for a specific lesson.
    
    Args:
        lesson_name: Name of the lesson
        topic: Overall topic
        
    Returns:
        Dict with lesson content, examples, exercises
    """
    prompt = f"""Provide detailed lesson content for: {lesson_name}
    
Part of: {topic}

Include:
1. Lesson overview
2. Key concepts (bullet points)
3. Real-world examples
4. Practice exercises (3-5)
5. Additional resources
"""

    content = call_llm(prompt)
    
    return {
        "lesson": lesson_name,
        "topic": topic,
        "content": content
    }
