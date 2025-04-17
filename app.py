import streamlit as st
from together import Together

# Initialize the Together client
client = Together(api_key=st.secrets["togetherai_api_key"])

st.title("🧠 Prompt Engineering Playground")

user_prompt = st.text_area("📝 Enter your prompt:")
if st.button("Submit"):
    if user_prompt:
        try:
            response = client.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",  # ✅ Serverless-compatible model
                prompt=user_prompt,
                max_tokens=150
            )
            reply = response.choices[0].text
            st.markdown("### 🤖 Response:")
            st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt.")
