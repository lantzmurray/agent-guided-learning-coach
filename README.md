# Project 18: Agent-Guided Learning Coach

An AI-powered learning coach that creates personalized learning paths, quizzes you, tracks progress, and adapts to your learning style. Perfect for certification exam preparation and skill development.

## Features

- **Personalized Learning Paths**: AI-generated curriculum tailored to your topic and skill level
- **Interactive Quizzes**: Auto-generated questions with instant grading and feedback
- **Progress Tracking**: Monitor your learning journey with detailed analytics
- **Adaptive Difficulty**: Automatically adjusts question difficulty based on your performance
- **Multi-Subject Support**: Works with any topic - from AWS certifications to nursing exams
- **Local Processing**: All AI processing runs locally using Ollama LLMs

## Architecture

### Core Agents

1. **Learning Path Agent** (`agents/learning_path_agent.py`)
   - Creates structured learning paths for any subject
   - Breaks down topics into manageable lessons
   - Provides detailed lesson content and objectives

2. **Quiz Agent** (`agents/quiz_agent.py`)
   - Generates relevant quiz questions
   - Provides multiple choice and open-ended questions
   - Grades answers with detailed explanations

3. **Progress Tracker** (`agents/progress_tracker.py`)
   - Tracks quiz performance over time
   - Identifies strengths and weaknesses
   - Provides progress summaries and statistics

4. **Adaptation Agent** (`agents/adaptation_agent.py`)
   - Analyzes performance patterns
   - Suggests difficulty adjustments
   - Generates personalized review materials

### Supporting Components

- **Orchestrator** (`orchestrator.py`) - Coordinates agent workflows
- **Streamlit Frontend** (`frontend/app.py`) - Interactive web interface
- **TinyDB Memory** (`memory/memory_store.json`) - Persistent progress storage

## Installation

### Prerequisites

- Python 3.8 or higher
- Ollama installed and running (for local LLM inference)

### Setup Steps

1. **Navigate to the project directory**:
   ```bash
   cd SchoolOfAI/Official/soai-18-learncoach
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install and start Ollama** (if not already installed):
   ```bash
   # Install Ollama from https://ollama.com
   # Pull a model (llama2 is recommended)
   ollama pull llama2
   # Start Ollama service
   ollama serve
   ```

## Running the Application

1. **Start the Streamlit application**:
   ```bash
   streamlit run frontend/app.py
   ```

2. **Open your browser**: Navigate to `http://localhost:8501`

## Usage

### 1. Create a Learning Path

- Enter your learning topic (e.g., "AWS Cloud Practitioner")
- Select your difficulty level (beginner, intermediate, advanced)
- Click "Generate Learning Path" to create a personalized curriculum

### 2. Take Quizzes

- Navigate to the Quiz tab
- Select a topic or use your current learning path
- Choose the number of questions
- Answer questions and receive instant feedback

### 3. Track Progress

- View your quiz history and scores
- See performance trends over time
- Identify topics that need more practice

### 4. Get Personalized Recommendations

- The adaptation agent analyzes your performance
- Receive suggestions for difficulty adjustments
- Get targeted review materials for weak areas

## Sample Syllabi

Sample syllabus files are included in the `sample_data/` directory:

- `AB-100_Agentic_AI_Architect_Syllabus.txt` - Agentic AI Architect certification
- `AIP-C01_Generative_AI_Developer_Syllabus.txt` - Generative AI Developer certification
- `AWS_Cloud_Practitioner_Syllabus.txt` - AWS Cloud Practitioner exam
- `NCLEX-RN_Nursing_Exam_Syllabus.txt` - NCLEX-RN nursing exam

You can upload your own syllabus or learning materials to create custom learning paths.

## Configuration

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
OLLAMA_MODEL=llama2
OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Ollama Models

The system supports any Ollama model. Recommended models:
- `llama2` - Good balance of speed and accuracy
- `mistral` - Faster inference
- `codellama` - Better for technical topics

To change models, modify the `OLLAMA_MODEL` environment variable or update the model parameter in the UI.

## Workflow

```
Select Topic → Generate Learning Path → Study Lessons → Take Quiz
     ↓                ↓                    ↓              ↓
  Choose       AI creates structured    Review lesson   Answer questions
  subject      curriculum with         content         and get feedback
  & difficulty  lessons & objectives
                                               ↓
                                         Track Progress
                                               ↓
                                         Adapt Difficulty
                                               ↓
                                    Personalized Review
```

## Project Structure

```
soai-18-learncoach/
├── agents/
│   ├── __init__.py
│   ├── base.py                    # Shared LLM and memory utilities
│   ├── learning_path_agent.py      # Creates personalized learning paths
│   ├── quiz_agent.py              # Generates and grades quizzes
│   ├── progress_tracker.py        # Tracks learning progress
│   └── adaptation_agent.py        # Adapts difficulty based on performance
├── sample_data/                   # Sample syllabus files
├── frontend/
│   ├── app.py                    # Streamlit UI
│   └── components.py             # Reusable UI components
├── memory/
│   └── memory_store.json         # TinyDB database (auto-created)
├── orchestrator.py               # Agent workflow coordination
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## Dependencies

- `streamlit` - Web UI framework
- `requests` - HTTP client for Ollama API
- `tinydb` - Lightweight JSON database
- `python-dateutil` - Date/time parsing

## Troubleshooting

### Ollama Connection Issues

If you see connection errors:
1. Verify Ollama is running: `ollama list`
2. Check the API URL: `curl http://localhost:11434/api/generate`
3. Ensure the model is pulled: `ollama pull llama2`

### Memory/Storage Issues

If you encounter database errors:
1. Delete the memory file: `rm memory/memory_store.json`
2. The application will recreate it on next run

### Slow Performance

For faster quiz generation:
1. Use a smaller model like `mistral`
2. Reduce the number of questions per quiz
3. Increase Ollama's GPU resources if available

### Poor Quiz Quality

If quiz questions aren't relevant:
1. Provide more specific topic names
2. Upload a syllabus file for better context
3. Try a different LLM model

## Tips for Best Results

1. **Be Specific**: Use detailed topic names (e.g., "AWS EC2 and S3" instead of "AWS")
2. **Upload Syllabi**: If preparing for an exam, upload the official syllabus
3. **Start Easy**: Begin with beginner difficulty and work your way up
4. **Review Feedback**: Read the explanations after each quiz question
5. **Track Progress**: Regularly check your progress to identify improvement areas

## License

This project is part of the School of AI curriculum.
