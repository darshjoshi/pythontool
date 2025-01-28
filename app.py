import streamlit as st
import openai
import os
import difflib

# Load OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit UI
st.title("Python Exercise Generator")
st.sidebar.header("Customize Your Exercise")

difficulty = st.sidebar.selectbox("Choose difficulty level:", ["Beginner", "Intermediate", "Advanced"])
topic = st.sidebar.selectbox("Select topic:", ["Data Types", "Arithmetic Operations", "Variables", "Loops"])
generate_button = st.sidebar.button("Generate Exercise")

if generate_button:
    with st.spinner("Generating your exercise..."):
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python tutor."},
                {"role": "user", "content": f"Create a {difficulty.lower()} level Python exercise about {topic.lower()}."}
            ],
            max_tokens=1000
        )
        exercise = response.choices[0].message.content.strip()
        st.write("### Your Python Exercise")
        st.write(exercise)

        user_code = st.text_area("Write your code here (indentation doesn't matter):")
        if st.button("Submit Code"):
            st.write("Submit button clicked!")  # Debug message
            with st.spinner("Evaluating your code..."):
                try:
                    st.write("Generating solution...")  # Debug message
                    # Generate solution for evaluation
                    solution_response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "You are a Python tutor."},
                            {"role": "user", "content": f"Provide a solution for this exercise: {exercise}"}
                        ],
                        max_tokens=150
                    )
                    solution = solution_response.choices[0].message['content'].strip()
                    st.write("Solution generated!")  # Debug message
        
                    # Normalize indentation and compare user code with solution
                    def normalize_code(code):
                        return "\n".join(line.strip() for line in code.splitlines() if line.strip())
        
                    normalized_user_code = normalize_code(user_code)
                    normalized_solution = normalize_code(solution)
        
                    similarity = difflib.SequenceMatcher(None, normalized_user_code, normalized_solution).ratio()
                    score = round(similarity * 100, 2)
        
                    st.write("### Evaluation Result")
                    st.write(f"Your Score: {score}%")
                    st.write("### Solution")
                    st.code(solution, language='python')
                except Exception as e:
                    st.error(f"An error occurred: {e}")

