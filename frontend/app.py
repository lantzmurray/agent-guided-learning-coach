import streamlit as st
import os
import sys

# Add parent directory to sys.path so we can import agents
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKAGE_ROOT = os.path.dirname(os.path.dirname(PROJECT_ROOT))
sys.path.append(PROJECT_ROOT)
if PACKAGE_ROOT not in sys.path:
    sys.path.insert(0, PACKAGE_ROOT)

from agents.learning_path_agent import create_learning_path, get_lesson_detail
from agents.quiz_agent import generate_quiz, grade_answer
from agents.progress_tracker import ProgressTracker
from agents.adaptation_agent import suggest_difficulty_adjustment, generate_personalized_review
from components import render_app_footer, run_with_status_updates

# Set up page config
st.set_page_config(page_title="AI Learning Coach", layout="wide")

st.title("AI Learning Coach 🎓")
st.write("Create personalized learning paths, take quizzes, and track your progress.")

# Initialize tracker
# Ensure memory directory exists
os.makedirs("memory", exist_ok=True)
tracker = ProgressTracker("memory/progress_store.json")

# Tab navigation
tab1, tab2, tab3, tab4 = st.tabs(["Learn", "Quiz", "Progress", "Review"])

with tab1:
    st.header("Create Learning Path")
    
    topic = st.text_input("What do you want to learn? (e.g., 'AWS Certified Cloud Practitioner')")
    difficulty = st.selectbox("Difficulty", ["beginner", "intermediate", "advanced"])
    time_commitment = st.select_slider("Weekly time", ["30 min", "1 hour", "2 hours", "5+ hours"])
    
    if st.button("Generate Learning Path"):
        path = run_with_status_updates(
            lambda: create_learning_path(topic, difficulty, time_commitment),
            start_message=f"Generating personalized path for {topic}..."
        )
        st.success("Learning path generated!")
        st.markdown(path["path_text"])

with tab2:
    st.header("Take a Quiz")
    
    quiz_topic = st.text_input("Quiz topic (e.g., 'AWS EC2 Basics')")
    num_questions = st.slider("Number of questions", 1, 10, 3)
    
    if st.button("Generate Quiz"):
        questions = run_with_status_updates(
            lambda: generate_quiz(quiz_topic, num_questions),
            start_message="Generating quiz questions..."
        )
        st.session_state["current_quiz"] = questions
        st.session_state["quiz_topic"] = quiz_topic
        st.session_state["answers"] = {}
        st.session_state["graded"] = False
            
    if "current_quiz" in st.session_state and not st.session_state.get("graded", False):
        questions = st.session_state["current_quiz"]
        
        # Display questions
        for i, q in enumerate(questions):
            if "error" in q:
                st.error("Failed to parse questions. Please try again.")
                continue
                
            st.write(f"**Q{i+1}:** {q['question']}")
            if q.get("type") == "multiple_choice":
                # Save user selection to session state
                st.session_state["answers"][i] = st.radio(f"Select answer for Q{i+1}", q["options"], key=f"q_{i}")
        
        if st.button("Submit Answers"):
            answers = dict(st.session_state["answers"])
            quiz_topic_for_log = st.session_state["quiz_topic"]

            def grade_quiz_answers():
                """Grade all submitted answers while the UI posts keep-alive updates."""
                score = 0
                total = len(questions)
                feedback_list = []
                
                for i, q in enumerate(questions):
                    user_ans = answers.get(i, "")
                    # Extract just the letter (e.g., "A") if options are formatted like "A: ..."
                    user_letter = user_ans.split(":")[0].strip() if ":" in user_ans else user_ans
                    
                    grade = grade_answer(q, user_letter)
                    if grade["is_correct"]:
                        score += 1
                    
                    feedback_list.append({
                        "question": q["question"],
                        "user_answer": user_ans,
                        "correct_answer": grade["correct_answer"],
                        "is_correct": grade["is_correct"],
                        "feedback": grade["feedback"]
                    })
                
                # Log the result
                tracker.log_quiz_result(
                    topic=quiz_topic_for_log,
                    score=score,
                    total=total,
                    quiz_questions=feedback_list
                )
                return score, total, feedback_list
            
            score, total, feedback_list = run_with_status_updates(
                grade_quiz_answers,
                start_message="Grading your quiz answers..."
            )
            st.session_state["graded"] = True
            st.session_state["last_score"] = score
            st.session_state["last_total"] = total
            st.session_state["last_feedback"] = feedback_list
            st.rerun()

    elif st.session_state.get("graded", False):
        score = st.session_state["last_score"]
        total = st.session_state["last_total"]
        
        st.success(f"Quiz completed! You scored {score}/{total} ({(score/total)*100:.0f}%)")
        
        for i, f in enumerate(st.session_state["last_feedback"]):
            if f["is_correct"]:
                st.success(f"**Q{i+1}:** {f['question']}\n\n✅ Your answer: {f['user_answer']}\n\n{f['feedback']}")
            else:
                st.error(f"**Q{i+1}:** {f['question']}\n\n❌ Your answer: {f['user_answer']}\n\nCorrect: {f['correct_answer']}\n\n{f['feedback']}")
        
        if st.button("Take Another Quiz"):
            del st.session_state["current_quiz"]
            del st.session_state["graded"]
            st.rerun()

with tab3:
    st.header("Your Progress")
    
    topics = tracker.get_all_topics()
    
    if not topics:
        st.info("Take some quizzes to see your progress here!")
    else:
        for topic in topics:
            prog = tracker.get_topic_progress(topic)
            
            # Use columns to display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Topic", topic)
            with col2:
                st.metric("Quizzes Taken", prog['quizzes_taken'])
            with col3:
                st.metric("Avg Quiz Score", f"{prog['average_quiz_score']:.0f}%")
                
            st.divider()

with tab4:
    st.header("Personalized Review")
    
    if st.button("Analyze Weak Areas & Get Recommendations"):
        weak = tracker.get_weak_areas()
        
        if weak:
            st.warning("Areas to focus on:")
            for area in weak:
                st.write(f"- **{area['topic']}**: {area['average_score']:.0f}% (Attempts: {area['attempts']})")
            
            st.subheader("Actionable Review Plan")
            # We can just pick the first topic or an aggregate
            topics = tracker.get_all_topics()
            if topics:
                prog = tracker.get_topic_progress(topics[-1]) # Or aggregate
                plan = run_with_status_updates(
                    lambda: generate_personalized_review(prog, weak),
                    start_message="Generating your personalized review plan..."
                )
                st.markdown(plan)
        else:
            st.success("No weak areas identified! Keep up the great work!")


render_app_footer()
