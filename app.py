import streamlit as st
from together import Together

# Load API key from Streamlit secrets
client = Together(api_key=st.secrets["togetherai_api_key"])

st.set_page_config(page_title="Prompt Engineering Playground", layout="wide")
st.title("Prompt Engineering Playground")
st.write("Explore different prompt engineering techniques and styles.")

# User input
base_prompt = st.text_input("Enter a question or topic:", "")

# Model selection
model = st.selectbox("Choose a model", [
    "mistralai/Mistral-7B-Instruct-v0.1",
    "meta-llama/Llama-2-7b-chat-hf",
    "togethercomputer/CodeLlama-7b-Instruct",
    "togethercomputer/RedPajama-INCITE-Chat-3B-v1"
])

# Technique selection
technique = st.selectbox("Prompting Technique", [
    "Zero-Shot",
    "Few-Shot",
    "Chain-of-Thought",
    "Instruction",
    "Role Prompting"
])

# Max Tokens
max_tokens = st.slider("Max Tokens", 50, 300, 150)

# Temperature
temperature = st.slider("Temperature (creativity)", 0.0, 1.5, 0.7, 0.1)

# Define examples and templates
few_shot_examples = (
    "Q: What are the benefits of drinking water?\n"
    "A: Water helps maintain bodily fluids, improves skin health, and boosts energy.\n\n"
    "Q: Why is exercise important?\n"
    "A: It helps reduce stress, increases stamina, and improves overall well-being.\n\n"
)

role_description = "You are a helpful and knowledgeable science teacher.\n"
instruction_format = "Provide a clear and concise explanation of the following:\n"
cot_suffix = " Let's think step by step."

# Build final prompt
if base_prompt:
    if technique == "Zero-Shot":
        final_prompt = base_prompt
    elif technique == "Few-Shot":
        final_prompt = f"{few_shot_examples}Q: {base_prompt}\nA:"
    elif technique == "Chain-of-Thought":
        final_prompt = f"{base_prompt}{cot_suffix}"
    elif technique == "Instruction":
        final_prompt = f"{instruction_format}{base_prompt}"
    elif technique == "Role Prompting":
        final_prompt = f"{role_description}Answer the question: {base_prompt}"
    else:
        final_prompt = base_prompt
else:
    final_prompt = ""

# Generate button
if st.button("Generate Response") and final_prompt:
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": final_prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        output = response.choices[0].message.content.strip()
        st.markdown("### Model Response")
        st.write(output)
    except Exception as e:
        st.error(f"Error generating response: {e}")
else:
    st.info("Enter a prompt and click Generate Response.")
