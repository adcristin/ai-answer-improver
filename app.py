import streamlit as st
import llm

def validate_inputs(question, answer):
    """
    Validates that the user has provided input according to SPEC.md.
    Returns (is_valid, error_message).
    """
    if not question.strip():
        return False, "Please enter the question you are answering."
    if not answer.strip():
        return False, "Please provide a draft answer to improve."
    if len(answer) < 20:
        return False, "Your answer is too short to provide a meaningful analysis. Please provide more detail."

    return True, None

def main():
    st.set_page_config(page_title="AI Answer Improver", page_icon="✍️")

    st.title("✍️ AI Answer Improver")
    st.markdown("""
    Improve your academic or technical answers by identifying missing points,
    fixing issues, and generating a polished version.
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

                # Missing Points
                st.subheader("🔍 Missing Points")
                missing = result.get("missing_points", [])
                if missing:
                    for point in missing:
                        st.markdown(f"- {point}")
                else:
                    st.success("Your answer is comprehensive! No critical points missing.")

                # Issues
                st.subheader("⚠️ Issues")
                issues = result.get("issues", [])
                if issues:
                    for issue in issues:
                        st.markdown(f"- {issue}")
                else:
                    st.success("No major issues found in your draft.")

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
                st.error("The AI provided a response that couldn't be parsed. This can happen with very long answers.")
            except llm.LLMValidationError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    main()
