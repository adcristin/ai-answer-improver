import streamlit as st
import llm
from typing import Tuple, Optional

def validate_inputs(question: str, answer: str) -> Tuple[bool, Optional[str]]:
    """
    Validates that the user has provided input according to SPEC.md.
    Returns (is_valid, error_message).
    """
    if not question.strip():
        return False, "Please enter the question you are answering."
    if not answer.strip():
        return False, "Please provide a draft answer to improve."

    return True, None

def main() -> None:
    """
    The main entry point for the AI Answer Improver application.
    Handles UI layout, user input, and AI response orchestration.
    """
    st.set_page_config(page_title="AI Answer Improver", page_icon="✍️")

    st.title("✍️ AI Answer Improver")
    st.markdown("""
    Improve your academic or technical answers by identifying missing points,
    fixing issues, and generating a polished version.
    """)

    with st.expander("💡 How to use this tool"):
        st.markdown("""
        1. **Enter the Question**: Paste the full prompt or question you are answering.
        2. **Enter your Draft**: Provide your initial attempt at the answer.
        3. **Click 'Improve Answer'**: The AI will analyze your draft for gaps and errors, then provide a rewritten version.

        **Example:**
        - *Question:* What is photosynthesis?
        - *Draft Answer:* It's how plants make food using light.
        - *AI Result:* Will suggest adding details about chlorophyll, carbon dioxide, and oxygen.
        """)

    # Input Section
    with st.container():
        question = st.text_area("Question", placeholder="Enter the question you are responding to...", height=150, max_chars=2000)
        answer = st.text_area("Draft Answer", placeholder="Enter your initial attempt...", height=250, max_chars=5000)

        improve_btn = st.button("Improve Answer", type="primary")

    if improve_btn:
        # 1. Input Validation
        is_valid, error_msg = validate_inputs(question, answer)
        if not is_valid:
            st.warning(error_msg)
            st.stop()

        # 2. AI Processing
        with st.spinner("Analyzing and improving your answer..."):
            try:
                result = llm.improve_answer(question, answer)

                # 3. Output Display
                st.divider()

                # Analysis Dashboard
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("🔍 Missing Points")
                    missing = result.get("missing_points", [])
                    if missing:
                        for point in missing:
                            st.markdown(f"- {point}")
                    else:
                        st.success("Your answer is comprehensive! No critical points missing.")

                with col2:
                    st.subheader("⚠️ Issues")
                    issues = result.get("issues", [])
                    if issues:
                        for issue in issues:
                            st.markdown(f"- {issue}")
                    else:
                        st.success("No major issues found in your draft.")

                st.divider()

                # Improved Answer
                st.subheader("✨ Improved Answer")
                st.markdown(result.get("improved_answer", "No improved answer generated."))

            except llm.ConfigurationError as e:
                st.error("System Configuration Error: API key not found. Please contact the administrator.")
            except llm.NetworkError as e:
                st.error("Network error: Unable to connect to the AI service. Please check your connection.")
            except llm.RateLimitError as e:
                st.error("Too many requests. Please wait a minute before trying again.")
            except llm.TimeoutError as e:
                st.error("The AI is taking too long to respond. Please try again in a moment.")
            except llm.ParsingError as e:
                st.error(f"The AI provided a response that couldn't be parsed: {str(e)}")
            except llm.LLMValidationError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
