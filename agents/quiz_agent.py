"""
Quiz Agent - Generate and grade quizzes.

ROLE:
Create quizzes from learning content, grade user answers, 
provide explanations and track performance.

QUESTION TYPES:
- Multiple choice
- True/False
- Short answer
- Fill in the blank
"""

from agents.base import call_llm
from typing import List, Dict
import json

def generate_quiz(topic: str, num_questions: int = 5, 
                  question_types: List[str] = None) -> List[Dict]:
    """
    Generate a quiz on a topic.
    
    Args:
        topic: Quiz subject
        num_questions: How many questions
        question_types: List of types ["multiple_choice", "true_false", "short_answer"]
        
    Returns:
        List of question dicts
    """
    if question_types is None:
        question_types = ["multiple_choice"]
        
    types_str = ", ".join(question_types)
        
    prompt = f"""Generate a {num_questions}-question quiz about "{topic}".
    
Question types to include: {types_str}

For multiple choice:
- Provide 4 options (A, B, C, D)
- Only ONE correct answer
- Include a brief explanation of why the correct answer is right

For true/false:
- Make statement clearly true or false
- Include explanation

For short answer:
- Ask a question requiring 1-3 sentence answer
- Provide sample ideal answer

Return ONLY a JSON array with this format:
[
  {{
    "type": "multiple_choice",
    "question": "...",
    "options": ["A: ...", "B: ...", "C: ...", "D: ..."],
    "correct": "A",
    "explanation": "..."
  }}
]
"""

    result = call_llm(prompt)
    
    # Parse JSON response
    try:
        # Extract JSON from response
        json_str = result[result.find("["):result.rfind("]")+1]
        questions = json.loads(json_str)
        return questions
    except Exception as e:
        return [{"error": "Failed to parse quiz", "raw": result}]

def grade_answer(question: Dict, user_answer: str) -> Dict:
    """
    Grade a user's quiz answer.
    
    Args:
        question: Question dict from generate_quiz
        user_answer: User's submitted answer
        
    Returns:
        Dict with: is_correct, feedback, explanation
    """
    correct = question.get("correct", "").upper()
    user = user_answer.upper().strip()
    
    # Check if multiple choice and user just typed the letter
    if question.get("type") == "multiple_choice":
        is_correct = user == correct or user == question.get("correct_answer", "").lower()
    else:
        is_correct = user == correct
    
    prompt = f"""Grade this quiz answer:

Question: {question['question']}
Correct answer: {question.get('correct', 'N/A')}
User's answer: {user_answer}

Provide:
1. Whether the answer is correct (yes/no)
2. Brief explanation of why
3. If wrong, what the correct answer is
"""

    feedback = call_llm(prompt)
    
    return {
        "is_correct": is_correct,
        "feedback": feedback,
        "correct_answer": question.get("correct")
    }