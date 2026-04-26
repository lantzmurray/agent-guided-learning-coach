"""
PROJECT 18: Agent-Guided Learning Coach

PURPOSE:
An AI tutor that creates personalized learning paths, quizzes you,
tracks progress, and adapts to your learning style. Great for certification exams!

CORE CONCEPT:
- Create learning paths for any subject (e.g. AWS Cloud Practitioner)
- Quiz yourself with AI-generated questions
- Track progress and identify weak areas
- Adapt difficulty based on performance

NEW COMPONENTS:
- agents/learning_path_agent.py: Create personalized learning paths
- agents/quiz_agent.py: Generate and grade quizzes
- agents/progress_tracker.py: Track learning progress
- agents/adaptation_agent.py: Adjust difficulty based on performance
- frontend/app.py: Streamlit application

USAGE:
Run `streamlit run frontend/app.py` to start the UI.
"""

from agents.learning_path_agent import create_learning_path, get_lesson_detail
from agents.quiz_agent import generate_quiz, grade_answer
from agents.progress_tracker import ProgressTracker
from agents.adaptation_agent import suggest_difficulty_adjustment, generate_personalized_review

def run_learning_session(topic: str, difficulty: str = "intermediate"):
    """
    Example orchestrator function that could be used programmatically.
    Currently, the Streamlit frontend handles the orchestration interactively.
    """
    print(f"Starting learning session for: {topic} at {difficulty} level.")
    
    # 1. Generate Learning Path
    path = create_learning_path(topic, difficulty)
    print("Learning Path Generated.")
    
    # 2. Generate a Quiz
    quiz = generate_quiz(topic, num_questions=3)
    print(f"Generated {len(quiz)} questions.")
    
    return {
        "path": path,
        "quiz": quiz
    }

if __name__ == "__main__":
    # Test the orchestrator logic
    result = run_learning_session("AWS Cloud Practitioner Basics", "beginner")
    print(result)