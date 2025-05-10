
---

### 🧠 Enhanced UI Version of `app.py`

```python
import streamlit as st
from together import Together

# Load API key from Streamlit secrets
client = Together(api_key=st.secrets["togetherai_api_key"])

# Page config
st.set_page_config(page_title="✨ Prompt Engineering Playground", layout="wide")

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    model = st.selectbox("🤖 Choose a model", [
        "mistralai/Mistral-7B-Instruct-v0.1",
        "meta-llama/Llama-2-7b-chat-hf",
        "togethercomputer/CodeLlama-7b-Instruct",
        "togethercomputer/RedPajama-INCITE-Chat-3B-v1"
    ])

    technique = st.selectbox("🧪 Prompting Technique", [
        "Zero-Shot",
        "Few-Shot",
        "Chain-of-Thought",
        "Instruction",
        "Role Prompting"
    ])

    max_tokens = st.slider("🔢 Max Tokens", 50, 300, 150)
    temperature = st.slider("🌡️ Temperature (creativity)", 0.0, 1.5, 0.7, 0.1)

# Main area
st.title("🧠 Prompt Engineering Playground")
st.markdown("Explore prompt engineering techniques using [Together AI](https://together.ai). Test different models and see how prompting changes outcomes.")

# Input
base_prompt = st.text_input("📝 Enter a question or topic:", "")

# Templates
few_shot_examples = (
    "Q: What are the benefits of drinking water?\n"
    "A: Water helps maintain bodily fluids, improves skin health, and boosts energy.\n\n"
    "Q: Why is exercise important?\n"
    "A: It helps reduce stress, increases stamina, and improves overall well-being.\n\n"
)

role_description = "You are a helpful and knowledgeable science teacher.\n"
instruction_format = "Provide a clear and concise explanation of the following:\n"
cot_suffix = " Let's think step by step."

# Final prompt construction
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

# Generate output
if st.button("🚀 Generate Response") and final_prompt:
    with st.spinner("Generating response..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": final_prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            output = response.choices[0].message.content.strip()
            st.markdown("### 📤 Model Response")
            st.success(output)
        except Exception as e:
            st.error(f"❌ Error: {e}")
else:
    st.info("💡 Enter a prompt and click 'Generate Response' to see the magic!")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by [Your Name or GitHub](https://github.com/yourusername) · Powered by Together AI")
