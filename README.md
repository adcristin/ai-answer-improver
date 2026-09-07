# ✍️ AI Answer Improver

The **AI Answer Improver** is a professional-grade Streamlit application designed to help students and professionals refine their academic or technical answers. By leveraging a Large Language Model (LLM), the app analyzes a draft answer against a specific question to identify gaps in knowledge, highlight technical errors, and generate a comprehensive, polished version of the response.

## 🚀 Key Features
- **Gap Analysis**: Automatically identifies critical points missing from the draft answer.
- **Issue Detection**: Highlights errors, phrasing issues, or lack of clarity.
- **Content Synthesis**: Generates a rewritten, high-quality version of the answer that incorporates all necessary points.
- **Robust Error Handling**: Gracefully manages API timeouts, rate limits, and malformed AI responses.

## 🛠️ Tech Stack
- **Frontend**: [Streamlit](https://streamlit.io/)
- **LLM Gateway**: [OpenRouter API](https://openrouter.ai/)
- **Language**: Python 3.x

## 📦 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ai-answer-improver
```

### 2. Install Dependencies
It is recommended to use a virtual environment:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```
*(Note: If `requirements.txt` is not present, install the core dependencies: `pip install streamlit python-dotenv`)*

### 3. Configure Environment Variables
Create a `.env` file in the root directory and add your OpenRouter API key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

## 🖥️ Usage
Launch the application using the following command:
```bash
streamlit run app.py
```

## 📝 Project Structure
- `app.py`: Main Streamlit UI and input validation logic.
- `llm.py`: Handles all API interactions and robust JSON parsing.
- `prompts.py`: Contains the system prompts and output schemas for the LLM.
- `SPEC.md`: Detailed technical specifications and rubric mapping.
- `VALIDATION.md`: Test cases and historical issue log.

## 🎯 Internship Rubric Compliance
This project is designed to satisfy the following requirements:
- **Usable Interface**: Clean, linear flow from input to results.
- **Text Input**: Dedicated fields for question and draft answer.
- **Meaningful AI Feature**: Three-tier analysis (Gaps $\rightarrow$ Issues $\rightarrow$ Synthesis).
- **Prompt-based Generation**: Structured JSON output for reliable UI rendering.
- **Input Validation**: Prevents empty submissions and handles edge cases.
- **Error Handling**: User-friendly notifications for all API failure modes.
- **Clear Output Display**: Side-by-side analysis dashboard and formatted improved answer.
