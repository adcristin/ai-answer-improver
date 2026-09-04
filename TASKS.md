# Task List: Answer Improver

This checklist tracks the implementation of the Answer Improver application, ordered by dependency.

## Phase 1: Environment Setup
- [ ] Create `requirements.txt` with `streamlit`, `openai`, `python-dotenv`.
- [ ] Create `.env.example` with `OPENROUTER_API_KEY`.

## Phase 2: LLM Logic (`llm.py`)
- [ ] Define custom exceptions in `llm.py` (`ConfigurationError`, `NetworkError`, `RateLimitError`, `TimeoutError`, `ParsingError`, `LLMValidationError`).
- [ ] Implement OpenRouter client initialization in `llm.py` using `python-dotenv`.
- [ ] Implement `improve_answer` function in `llm.py` to send request and return raw response.
- [ ] Implement JSON parsing logic in `llm.py` to return the structured dictionary.

## Phase 3: Prompt Management (`prompts.py`)
- [ ] Define the system prompt constant in `prompts.py` according to the design.
- [ ] Update `llm.py` to use the system prompt from `prompts.py`.

## Phase 4: Application UI (`app.py`)
- [ ] Implement basic Streamlit layout with `st.text_input` for question and `st.text_area` for answer.
- [ ] Integrate `llm.improve_answer` call in `app.py` triggered by a button.
- [ ] Implement display logic for `missing_points` and `issues` (e.g., using `st.write` or `st.markdown`).
- [ ] Implement display logic for `improved_answer` (e.g., using `st.subheader` and `st.markdown`).

## Phase 5: Input & LLM Validation
- [ ] Implement input validation in `app.py` to prevent empty submissions.
- [ ] Implement logic in `llm.py` to detect `error` key in LLM response and raise `LLMValidationError`.

## Phase 6: Error Handling
- [ ] Implement a global `try...except` block in `app.py` to catch custom exceptions from `llm.py`.
- [ ] Map each custom exception to its corresponding user-facing `st.error` message.

## Phase 7: Polish
- [ ] Improve UI layout (e.g., using `st.columns` or `st.container`).
- [ ] Refine user flow and add a "Clear" button or session state management.
