# Specification: Answer Improver App

The Answer Improver is a Streamlit application designed to help students refine their academic or technical answers by providing automated analysis and an improved version of their draft using a Large Language Model (LLM).

## 1. User Flow
1. **Input Phase**:
   - The user arrives at the home page.
   - The user enters the **Question** they are trying to answer.
   - The user enters their **Draft Answer**.
2. **Action Phase**:
   - The user clicks the **"Improve Answer"** button.
3. **Processing Phase**:
   - The app validates the inputs.
   - If valid, the app sends the question and answer to the LLM via the OpenRouter API.
   - The app parses the structured JSON response from the LLM.
4. **Output Phase**:
   - The app displays the results in a structured layout:
     - **Missing Points**: A bulleted list of key concepts the student missed.
     - **Issues**: A bulleted list of errors or areas for improvement in the draft.
     - **Improved Answer**: A rewritten, comprehensive version of the answer.

## 2. Input Fields & Constraints

| Field | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| **Question** | Text Area | Required, Max 2000 chars | The prompt or question the student is responding to. |
| **Draft Answer** | Text Area | Required, Max 5000 chars | The student's initial attempt at the answer. |

## 3. Output Schema (LLM Response)
The LLM must return a valid JSON object. To prevent UI crashes, the model is prompted to return empty arrays `[]` rather than `null` for empty sets.

```json
{
  "missing_points": ["point 1", "point 2", "..."],
  "issues": ["issue 1", "issue 2", "..."],
  "improved_answer": "The full rewritten version of the answer..."
}
```

- `missing_points`: `Array<string>`. A list of critical information absent from the draft. Must be `[]` if the answer is comprehensive.
- `issues`: `Array<string>`. A list of errors or areas for improvement. Must be `[]` if no issues are found.
- `improved_answer`: `string`. A polished, comprehensive version of the answer. If the original is already optimal, the LLM should still return a version with optimized phrasing and professional tone.

## 4. Validation Rules

| Scenario | Validation Rule | User Notification |
| :--- | :--- | :--- |
| **Empty Question** | `if not question.strip():` | "Please enter the question you are answering." |
| **Empty Answer** | `if not answer.strip():` | "Please provide a draft answer to improve." |
| **Insufficient Detail** | `if len(answer) < 20:` | "Your answer is too short to provide a meaningful analysis. Please provide more detail." |
| **Language Mismatch** | LLM-side detection | "The answer provided is in a different language than the question. Please ensure both are in the same language for best results." |
| **Gibberish/Nonsense** | LLM-side detection | "The provided answer seems nonsensical or contains only random characters. Please provide a valid text response." |
| **Code Content** | Support for Markdown | *No notification; system expects and preserves Markdown code blocks in the improved answer.* |

## 5. Error Handling

| Error Type | Technical Cause | User-Facing Message | Recovery Action |
| :--- | :--- | :--- | :--- |
| **API Timeout** | Request exceeds timeout limit | "The AI is taking too long to respond. Please try again in a moment." | User clicks "Improve" again. |
| **Malformed JSON** | LLM returns non-JSON or truncated response | "The AI provided a response that couldn't be parsed. This can happen with very long answers." | Suggest shorter input or click "Improve" to retry. |
| **Rate Limit** | OpenRouter 429 Too Many Requests | "Too many requests. Please wait a minute before trying again." | Exponential backoff or manual wait. |
| **Network Failure** | DNS failure, No internet, Connection reset | "Network error: Unable to connect to the AI service. Please check your connection." | Check internet and retry. |
| **API Key Missing** | `.env` not loaded or `OPENROUTER_API_KEY` empty | "System Configuration Error: API key not found. Please contact the administrator." | Developer fix in `.env`. |

## 6. Rubric Satisfaction Mapping

| Rubric Bullet | Spec Implementation |
| :--- | :--- |
| **Usable Interface** | Defined as a clear 4-phase user flow (Input $\rightarrow$ Action $\rightarrow$ Process $\rightarrow$ Output) in a single-page Streamlit layout. |
| **Text Input** | Explicitly requires two text areas: one for the Question and one for the Draft Answer. |
| **Meaningful AI Feature** | Implements automated gap analysis (missing points), error detection (issues), and content synthesis (improved answer). |
| **Prompt-based Generation** | Utilizes a structured JSON prompt to ensure the LLM returns data in the exact schema required for the UI. |
| **Input Validation** | Comprehensive rules for empty strings, minimum length, and nonsensical input. |
| **Error Handling** | Detailed recovery paths for timeouts, malformed responses, rate limits, and network failures. |
| **Clear Output Display** | Structured output separated into distinct sections (Missing Points, Issues, Improved Answer) for readability. |
| **Clean User Flow** | A linear, logical sequence from input to result, preventing processing until inputs are validated. |
