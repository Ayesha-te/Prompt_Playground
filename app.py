import streamlit as st
from together import Together

# Initialize Together AI client
client = Together(api_key=st.secrets["togetherai_api_key"])

st.set_page_config(page_title="Prompt Style Comparison", layout="wide")
st.title("Prompt Style Comparison Playground")
st.write("Enter a base topic or question, and we'll show how different prompt styles and techniques affect the response.")

# User input
base_prompt = st.text_input("Base prompt/topic (e.g. 'benefits of drinking water')", "")

# Choose model
model = st.selectbox("Choose model", [
    "mistralai/Mistral-7B-Instruct-v0.1",
    "meta-llama/Llama-2-7b-chat-hf",
    "togethercomputer/CodeLlama-7b-Instruct",
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1"
])

# Choose prompting technique
technique = st.selectbox("Select Prompting Technique", ["Zero-Shot", "Few-Shot"])

# Max tokens
max_tokens = st.slider("Max Tokens", 50, 300, 150)

# Define few-shot examples
few_shot_examples = (
    "Q: What are the benefits of drinking water?\n"
    "A: Drinking water helps maintain body fluids, energizes muscles, and improves skin.\n\n"
    "Q: How does exercise benefit mental health?\n"
    "A: Exercise reduces stress and anxiety by releasing endorphins and improving sleep.\n\n"
)

# Generate button
if st.button("Generate & Compare") and base_prompt:

    styles = {
        "Direct": f"{base_prompt}",
        "Instructive": f"Explain in detail: {base_prompt}",
        "Conversational": f"Human: Can you tell me about {base_prompt}?\nAI:",
        "Academic": f"Write a short academic explanation on the topic: {base_prompt}",
        "Simplified": f"Explain {base_prompt} like I’m five years old.",
    }

    cols = st.columns(len(styles))

    for i, (style_name, prompt) in enumerate(styles.items()):
        with cols[i]:
            st.markdown(f"### {style_name}")
            try:
                if technique == "Few-Shot":
                    full_prompt = f"{few_shot_examples}Q: {prompt}\nA:"
                else:
                    full_prompt = prompt

                response = client.completions.create(
                    model=model,
                    prompt=full_prompt,
                    max_tokens=max_tokens,
                )

                output = response.choices[0].text.strip()
                st.write(output)
            except Exception as e:
                st.error(f"Error: {e}")

else:
    st.info("Enter a prompt and click 'Generate & Compare' to get started.")
