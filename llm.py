import os
import json
import re
from openai import OpenAI, APIError, APIConnectionError, RateLimitError as OpenAI_RateLimitError
from dotenv import load_dotenv
from prompts import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

# --- Custom Exceptions ---

class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass

class ConfigurationError(LLMError):
    """Raised when API keys or configuration are missing."""
    pass

class NetworkError(LLMError):
    """Raised when the API request fails due to network issues."""
    pass

class RateLimitError(LLMError):
    """Raised when the API rate limit is exceeded."""
    pass

class TimeoutError(LLMError):
    """Raised when the API request times out."""
    pass

class ParsingError(LLMError):
    """Raised when the LLM response cannot be parsed as JSON."""
    pass

class LLMValidationError(LLMError):
    """Raised when the LLM response is valid JSON but fails business validation."""
    pass

# --- Client Initialization ---

def get_client():
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ConfigurationError("OPENROUTER_API_KEY not found in environment variables.")

    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

def improve_answer(question: str, answer: str) -> dict:
    """
    Sends the question and answer to OpenRouter and returns a structured dictionary.
    """
    try:
        client = get_client()
    except ConfigurationError:
        raise

    try:
        # OpenRouter supports standard OpenAI API.
        # The 'timeout' parameter in the create call ensures the 15s limit.
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Question: {question}\n\nDraft Answer: {answer}"}
            ],
            response_format={"type": "json_object"},
            timeout=15.0
        )
    except OpenAI_RateLimitError:
        raise RateLimitError("AI service rate limit exceeded. Please try again later.")
    except APIConnectionError:
        raise NetworkError("Unable to connect to the AI service. Please check your connection.")
    except APIError as e:
        # Check if it's a timeout (usually wrapped in APIError or occurs as a specific exception)
        if "timeout" in str(e).lower():
            raise TimeoutError("The AI is taking too long to respond. Please try again in a moment.")
        raise NetworkError(f"AI service returned an error: {str(e)}")
    except Exception as e:
        # Catch-all for other unexpected errors during the request
        raise NetworkError(f"An unexpected error occurred: {str(e)}")

    content = response.choices[0].message.content or ""
    return _parse_json_response(content)

def _parse_json_response(content: str) -> dict:
    """
    Parse the model's response into the expected JSON schema,
    with fallbacks for markdown-wrapped or loosely-formed JSON.
    """
    # 1. Happy path — model returned clean JSON
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # 2. Strip markdown code fences (```json ... ``` or ``` ... ```)
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", content, re.DOTALL)
    if fence_match:
        try:
            return json.loads(fence_match.group(1))
        except json.JSONDecodeError:
            pass

    # 3. Last resort — extract first { to last } and try again
    brace_match = re.search(r"\{.*\}", content, re.DOTALL)
    if brace_match:
        try:
            return json.loads(brace_match.group(0))
        except json.JSONDecodeError:
            pass

    # 4. Nothing worked — fail loudly
    raise ParsingError(
        f"Could not parse model response as JSON. Raw response: {content[:200]}"
    )

if __name__ == "__main__":
    # Test cases to verify LLM logic standalone
    test_cases = [
        {
            "question": "What is the capital of France?",
            "answer": "Paris.",
            "label": "Short but correct"
        },
        {
            "question": "Explain how a for-loop works in Python.",
            "answer": "A for loop goes through things in a list.",
            "label": "Over-simplified"
        },
        {
            "question": "What is photosynthesis?",
            "answer": "It's how plants eat sunlight.",
            "label": "Colloquial/Incomplete"
        },
        {
            "question": "What is 2+2?",
            "answer": "asdfghjkl",
            "label": "Gibberish (Validation check)"
        }
    ]

    print("🚀 Starting standalone tests for llm.py...")
    print("Note: Requires a valid OPENROUTER_API_KEY in .env\n")

    for i, case in enumerate(test_cases, 1):
        print(f"Test {i}: {case['label']}")
        print(f"Q: {case['question']}")
        print(f"A: {case['answer']}")
        try:
            result = improve_answer(case['question'], case['answer'])
            print("Result:")
            print(json.dumps(result, indent=2))
        except LLMError as e:
            print(f"Caught expected/unexpected LLMError: {type(e).__name__} - {e}")
        except Exception as e:
            print(f"Unexpected crash: {e}")
        print("-" * 40)
