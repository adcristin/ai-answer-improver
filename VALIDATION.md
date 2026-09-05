# Validation Checklist: Answer Improver

This document contains the test cases derived from `SPEC.md` to ensure all validation and error-handling rules are correctly implemented.

## 1. Input Validation Tests

| Test Case | Input: Question | Input: Draft Answer | Expected Outcome | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Empty Question** | `""` (or whitespace) | `"A valid draft answer..."` | Error: "Please enter the question you are answering." | [ ] |
| **Empty Answer** | `"A valid question..."` | `""` (or whitespace) | Error: "Please provide a draft answer to improve." | [ ] |
| **Too Short Answer** | `"A valid question..."` | `"Too short"` | LLM should process normally and identify gaps in `missing_points`/`issues`. | [ ] |
| **Gibberish Answer** | `"A valid question..."` | `"asdfghjkl; 123456789"` | Error: "The provided answer seems nonsensical or contains only random characters. Please provide a valid text response." | [ ] |
| **Max Length (Question)** | 2000+ chars | `"A valid draft answer..."` | Input should be truncated or blocked at 2000 chars. | [ ] |
| **Max Length (Answer)** | `"A valid question..."` | 5000+ chars | Input should be truncated or blocked at 5000 chars. | [ ] |
| **Valid Input** | `"A valid question..."` | `"A detailed draft answer..."` | Successful processing and output display. | [ ] |

## 2. Error Handling & Simulation Tests

| Error Type | Simulation Method | Expected Outcome | Status |
| :--- | :--- | :--- | :--- |
| **API Timeout** | In `llm.py`, temporarily add `time.sleep(60)` before the API call or set a very low timeout in the request config. | Error: "The AI is taking too long to respond. Please try again in a moment." | [ ] |
| **Malformed JSON** | In `llm.py`, mock the API return value to be a plain string (e.g., `"Internal Server Error"`) instead of a JSON object. | Error: "The AI provided a response that couldn't be parsed. This can happen with very long answers." | [ ] |
| **Missing JSON Keys** | In `llm.py`, mock the API to return JSON missing one of the required keys (e.g., missing `improved_answer`). | Error: "The AI provided a response that couldn't be parsed..." | [ ] |
| **Rate Limit (429)** | Use a mock response that returns HTTP 429 status code. | Error: "Too many requests. Please wait a minute before trying again." | [ ] |
| **Network Failure** | Disconnect internet or use a mock that raises a `requests.exceptions.ConnectionError`. | Error: "Network error: Unable to connect to the AI service. Please check your connection." | [ ] |
| **API Key Missing** | Temporarily rename or clear `OPENROUTER_API_KEY` in the `.env` file. | Error: "System Configuration Error: API key not found. Please contact the administrator." | [ ] |

## 3. Output Quality Tests

- [ ] **Missing Points**: Verify it displays as a bulleted list.
- [ ] **Issues**: Verify it displays as a bulleted list.
- [ ] **Improved Answer**: Verify it is a comprehensive rewritten version.
- [ ] **Markdown Support**: Input a question about code and verify that the improved answer renders Markdown code blocks correctly.
- [ ] **Empty Sets**: Provide a perfect answer and verify that "Missing Points" and "Issues" are handled gracefully (e.g., "No issues found").

## Validation Log

### Issue 1 — False positive on length validation
- **Input:** Question: "capital of france?", Answer: "paris"
- **Expected:** Correct answer processed normally
- **Actual:** Blocked by app with "Your answer is too short to provide a meaningful analysis."
- **Cause:** Validation used a character-count threshold, which can't distinguish "too short to be useful" from "short because the correct answer is short."
- **Fix:** Removed the length-based check entirely; validation now only blocks empty/whitespace input. Judgment on answer completeness is left to the model via `missing_points`/`issues`.
- **Status:** ✅ Resolved

### Issue 2 — Generic "Network error" masking the real cause
- **Input:** Same as above, after fixing Issue 1
- **Expected:** Successful API call
- **Actual:** "Network error: Unable to connect to the AI service."
- **Cause:** Broad exception handling was catching a different underlying error and relabeling it generically, hiding the actual issue.
- **Fix:** Added temporary logging of the raw exception to diagnose; investigation led to Issues 3–5 below.
- **Status:** ✅ Resolved (root causes identified separately)

### Issue 3 — Rate limit (429) during rapid testing
- **Input:** Repeated submissions within a short window (curl tests + app retries)
- **Expected:** Clear rate-limit message
- **Actual:** "Too many requests. Please wait a minute before trying again."
- **Cause:** Genuine OpenRouter free-tier rate limiting, correctly caught by the custom `RateLimitError` handler.
- **Fix:** None needed — this is expected behavior, correctly surfaced.
- **Status:** ✅ Confirmed working as intended

### Issue 4 — JSON parse failure on non-trivial answers
- **Input:** Question: "capital of france?", Answer: "france"
- **Expected:** Structured critique flagging the incomplete answer
- **Actual:** "The AI provided a response that couldn't be parsed. This can happen with very long answers." (input was one word — message was misleading as to cause)
- **Cause:** No `max_tokens` was set on the API call; the reasoning model (Nemotron 3.5 Lightning) spent its token budget on an internal reasoning trace, truncating the JSON output before it could close properly. Intermittent — same input passed on a later retry.
- **Fix:** Added explicit `max_tokens=1000` to the API call.
- **Status:** ✅ Resolved (see Issue 5 for a related, deeper cause)

### Issue 5 — Reasoning trace leaking into the content field
- **Input:** Question: "Explain how a for-loop works in Python.", Answer: "A for loop goes through things in a list." (and similar nuanced inputs)
- **Expected:** Clean JSON response
- **Actual:** Raw response began with "Here's a thinking process: 1. Analyze User Input..." instead of JSON — not truncation, the model's internal reasoning was emitted directly as the final content.
- **Cause:** Nemotron 3.5 Lightning is a reasoning model; `response_format={"type":"json_object"}` did not reliably suppress its reasoning trace for longer/nuanced inputs, even after adding `extra_body={"reasoning":{"exclude": True}}`.
- **Fix:** Switched `OPENROUTER_MODEL` to `nvidia/nemotron-3-ultra-550b-a55b:free`, a non-reasoning-leaking model. All 4 standalone test cases (short-correct, over-simplified, colloquial/incomplete, gibberish) passed cleanly.
- **Status:** ✅ Resolved 
