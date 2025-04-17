import streamlit as st
import together

# Load API key
together.api_key = st.secrets["togetherai_api_key"]

st.title("🧠 Prompt Engineering Playground")

user_prompt = st.text_area("📝 Enter your prompt:")
if st.button("Submit"):
    if user_prompt:
        try:
            response = together.Complete.create(
                model="togethercomputer/llama-2-7b-chat",  # You can change this
                prompt=user_prompt,
                max_tokens=150
            )
            reply = response['output']['choices'][0]['text']
            st.markdown("### 🤖 Response:")
            st.write(reply)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a prompt.")
