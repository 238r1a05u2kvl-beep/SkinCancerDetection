import streamlit as st
import ollama

# Configure page
st.set_page_config(
    page_title="AI Skin Cancer Assistant",
    page_icon="🤖",
    layout="wide"
)

# System Prompt
SYSTEM_PROMPT = """
You are an AI Skin Cancer Assistant.

Rules:
1. Answer ONLY questions related to:
- Skin cancer
- Melanoma
- Basal Cell Carcinoma
- Benign skin lesions
- Symptoms
- Prevention
- Diagnosis
- Treatment
- Dermatology

2. If the question is NOT related to skin cancer or dermatology,
reply ONLY:
"I'm designed to answer questions related to skin cancer and dermatology only."

3. Never claim to be a doctor.

4. Always recommend consulting a dermatologist for medical diagnosis.

5. Keep answers simple and easy to understand.

6. Keep responses between 80 and 150 words whenever possible.
"""

# Track Chat History in Streamlit Session State
if "messages" not in st.session_state:
    # Initialize with the system instructions as the very first context message
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

col1, col2, col3 = st.columns([1,2,1])

with col2:
    try:
        st.image("assets/logo.png", width=80)
    except Exception:
        pass  # Prevents crash if logo file is missing

st.title("Diagnosis Result")
st.info(
    "⚠️ This chatbot is for educational purposes only and does not replace professional medical advice."
)

st.success("""
Hello! 👋

I'm your AI Skin Cancer Assistant.

I can help answer questions about:
- Skin cancer
- Melanoma
- Symptoms
- Prevention
- Treatment
- Dermatology

Please remember that I cannot provide a medical diagnosis.
""")

st.divider()

# Displaying previous chat messages (skipping the hidden system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# User input
prompt = st.chat_input("Type your question here...")

if prompt and prompt.strip():

    # Append and display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response from Local Ollama Model
    with st.spinner("Thinking locally..."):
        try:
            response = ollama.chat(
                model="gemma2:2b",
                messages=st.session_state.messages
            )
            answer = response["message"]["content"]
            
        except Exception as e:
            answer = (
                f"⚠️ Unable to contact your local Ollama server. "
                f"Make sure the Ollama app is running on your machine. Error: {str(e)}"
            )

    # Append and display assistant message
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)


# Sidebar
with st.sidebar:
    st.header("Options")

    if st.button("🗑 Clear Chat"):
        # Reset the chat history to just the system instructions
        st.session_state.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]
        st.rerun()

    st.divider()

    if st.button("🏠 Back to Home"):
        st.switch_page("app.py")
        
st.divider()

st.caption(
    "AI responses are generated locally by Ollama. "
    "Always consult a qualified dermatologist for diagnosis and treatment."
)
