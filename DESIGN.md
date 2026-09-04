# Design Document: Answer Improver

## 1. File Structure

```text
.
├── app.py              # Streamlit UI: Input handling, validation, and output display
├── llm.py              # API Logic: OpenRouter client, response parsing, and custom exceptions
├── prompts.py          # Prompt Management: System prompt and LLM instructions
├── requirements.txt    # Dependencies: streamlit, openai, python-dotenv
└── .env.example       # Environment variable template
```

## 2. Module Specifications

### `llm.py`
This module encapsulates all communication with the OpenRouter API.

**Function Signature:**
`improve_answer(question: str, answer: str) -> dict`

- **Input**: 
  - `question`: The academic/technical question.
  - `answer`: The student's draft response.
- **Output**: A dictionary matching the following schema:
  ```json
  {
    "missing_points": ["string", ...],
    "issues": ["string", ...],
    "improved_answer": "string"
  }
  ```
- **Behavior**: 
  1. Loads `OPENROUTER_API_KEY` from `.env`.
  2. Sends a chat completion request using the system prompt from `prompts.py`.
  3. Parses the response as JSON.
  4. Detects LLM-side validation errors (Gibberish/Language Mismatch) via specific JSON keys.

### `prompts.py`
Contains the static text for LLM instructions to keep `llm.py` clean.

**System Prompt:**
```text
You are an expert Academic Tutor. Your task is to analyze a student's draft answer based on a provided question.

Instructions:
1. Identify Missing Points: List critical concepts or facts that are absent from the draft but necessary for a complete answer.
2. Identify Issues: List errors, misconceptions, or areas where the phrasing is weak or incorrect.
3. Provide Improved Answer: Rewrite the answer to be comprehensive, professional, and accurate. Preserve any Markdown code blocks provided in the original.

Validation Rules:
- If the draft answer is nonsensical, consists of random characters, or is gibberish, return: {"error": "gibberish"}
- If the draft answer is in a different language than the question, return: {"error": "language_mismatch"}

Output Format:
You MUST return ONLY a valid JSON object. Do not include markdown code blocks (like ```json) in your response.
Schema:
{
  "missing_points": ["point 1", "point 2"], // Empty array [] if comprehensive
  "issues": ["issue 1", "issue 2"],      // Empty array [] if no issues
  "improved_answer": "The polished version..."
}
```

## 3. Error Handling & Propagation

### Exception Mapping
`llm.py` will raise custom exceptions which `app.py` will catch to display the specific `st.error` messages defined in `SPEC.md`.

| Exception (llm.py) | Technical Cause | `st.error` Message (app.py) |
| :--- | :--- | :--- |
| `ConfigurationError` | Missing `OPENROUTER_API_KEY` | "System Configuration Error: API key not found. Please contact the administrator." |
| `NetworkError` | DNS/Connection failure | "Network error: Unable to connect to the AI service. Please check your connection." |
| `RateLimitError` | HTTP 429 | "Too many requests. Please wait a minute before trying again." |
| `TimeoutError` | Request timeout | "The AI is taking too long to respond. Please try again in a moment." |
| `ParsingError` | Invalid JSON response | "The AI provided a response that couldn't be parsed. This can happen with very long answers." |
| `LLMValidationError` | `error` key in JSON | (Based on error type) "The provided answer seems nonsensical..." OR "The answer provided is in a different language..." |

### Propagation Flow
1. `app.py` $\rightarrow$ calls `llm.improve_answer()`.
2. `llm.py` $\rightarrow$ catches `openai.APIError` or `json.JSONDecodeError` $\rightarrow$ raises custom exception (e.g., `ParsingError`).
3. `app.py` $\rightarrow$ `try...except` block catches the custom exception $\rightarrow$ `st.error(exception.message)`.
