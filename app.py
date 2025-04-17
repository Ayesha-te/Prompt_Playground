import streamlit as st
from together import Together

# Initialize the Together AI client
client = Together(api_key=st.secrets["togetherai_api_key"])

st.set_page_config(page_title="🧠 Prompt Style Comparison", layout="wide")
st.title("🧠 Prompt Style Comparison Playground")
st.write("Enter a base topic or question, and we'll show how different prompt styles affect the response.")

# User input
base_prompt = st.text_input("🔤 Base prompt/topic (e.g. 'benefits of drinking water')", "")

# Choose model
model = st.selectbox("🤖 Choose model", [
    "mistralai/Mistral-7B-Instruct-v0.1",
    "meta-llama/Llama-2-7b-chat-hf",
    "togethercomputer/CodeLlama-7b-Instruct",
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1"
])

max_tokens = st.slider("🔢 Max Tokens", 50, 300, 150)

# Generate button
if st.button("🚀 Generate & Compare") and base_prompt:
    # Define different styles
    styles = {
        "🧾 Direct": f"{base_prompt}",
        "📚 Instructive": f"Explain in detail: {base_prompt}",
        "🗣️ Conversational": f"Human: Can you tell me about {base_prompt}?\nAI:",
        "🎓 Academic": f"Write a short academic explanation on the topic: {base_prompt}",
        "🤖 Simplified": f"Explain {base_prompt} like I’m five years old.",
    }

    cols = st.columns(len(styles))  # Create columns for comparison

    for i, (style_name, prompt) in enumerate(styles.items()):
        with cols[i]:
            st.markdown(f"### {style_name}")
            try:
                response = client.completions.create(
                    model=model,
                    prompt=prompt,
                    max_tokens=max_tokens,
                )
                output = response.choices[0].text.strip()
                st.write(output)
            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.info("👈 Enter a prompt and click 'Generate & Compare' to get started.")
