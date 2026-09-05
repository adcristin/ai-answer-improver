# AI Answer Improver

This application helps students refine their academic and technical answers by analyzing gaps in their drafts and providing a polished version.

## How it Works
The app follows a linear workflow:
1. **Input**: The user provides the question they are answering and their draft response.
2. **Validation**: The system checks for empty fields or answers that are too short (<20 characters).
3. **AI Analysis**: The inputs are sent to an LLM via the OpenRouter API. The model is forced to return a structured JSON object containing a gap analysis and a rewrite.
4. **Output**: The app displays "Missing Points" (concepts the student overlooked), "Issues" (errors or weak phrasing), and the "Improved Answer."

## Prompt Structure
The app uses a structured system prompt to ensure consistent output:
> "You are an expert Academic Tutor. Your task is to analyze a student's draft answer based on a provided question. Instructions: 1. Identify Missing Points... 2. Identify Issues... 3. Provide Improved Answer... You MUST return ONLY a valid JSON object."

The prompt enforces a strict JSON schema with `missing_points`, `issues`, and `improved_answer` keys.

## Error Handling
The app maps technical failures to clear user notifications as defined in `SPEC.md`:
- **API Timeout**: "The AI is taking too long to respond."
- **Malformed JSON**: "The AI provided a response that couldn't be parsed."
- **Rate Limit**: "Too many requests. Please wait a minute."
- **Network Failure**: "Unable to connect to the AI service."
- **Configuration Error**: "API key not found."

## Educational Workflow
Unlike a generic chatbot that simply provides a correct answer, this tool functions as an AI tutor. By explicitly separating "Missing Points" and "Issues" from the final result, it highlights the student's specific knowledge gaps. This forces the user to recognize what they missed and why their draft was insufficient, turning a simple generation task into a learning experience centered on gap analysis.
