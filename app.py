import streamlit as st
from PIL import Image
from streamlit_float import float_init
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="Skin Cancer Detection",
    page_icon="🩺",
    layout="centered"
)

# Initialize floating system layout elements
float_init()

# Initialize global chat history across your multipage app
if "messages" not in st.session_state:
    SYSTEM_PROMPT = """
    You are an AI Skin Cancer Assistant.
    Rules:
    1. Answer ONLY questions related to skin cancer, melanoma, dermatology, etc.
    2. If off-topic, reply ONLY: "I'm designed to answer questions related to skin cancer and dermatology only."
    3. Never claim to be a doctor. Recommend consulting a dermatologist.
    4. Keep answers simple, between 80 and 150 words.
    """
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Initialize dark mode theme configuration state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# Theme alignment and top layout setup
col1, col2 = st.columns([8, 1])

with col2:
    if st.toggle("🌙", value=st.session_state.dark_mode):
        st.session_state.dark_mode = True
    else:
        st.session_state.dark_mode = False

# Establish Theme Color Properties
if st.session_state.dark_mode:
    bg_color = "#0E1117"
    text_color = "white"
    card_color = "#1E1E1E"
else:
    bg_color = "#FFFFFF"
    text_color = "#000000"
    card_color = "#F5F5F5"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color:{bg_color};
        color:{text_color};
    }}

    .main-box {{
        background-color:{card_color};
        padding:40px;
        border-radius:15px;
        text-align:center;
        margin-top:100px;
        box-shadow:0 0 15px rgba(0,0,0,0.2);
    }}

    h1 {{
        text-align:center;
        color:{text_color};
    }}

    div.floating-chat-container {{
        position: fixed !important;
        bottom: 30px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        z-index: 999999 !important;
    }}
    
    div.floating-chat-container button {{
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 50% !important;
        width: 60px !important;
        height: 60px !important;
        font-size: 24px !important;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.3) !important;
        border: none !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s ease !important;
    }}

    div.floating-chat-container button:hover {{
        transform: translateX(0) scale(1.08) !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Core layout dashboard panel container
st.markdown('<div class="main-box">', unsafe_allow_html=True)

st.title("Skin Cancer Detection")

uploaded_file = st.file_uploader(
    "Upload Skin Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file)

    if image.mode != "RGB":
        image = image.convert("RGB")

    st.session_state["uploaded_image"] = image
    image.save(BASE_DIR / "uploaded_image.jpg")
    st.image(image, width=300)

if st.button("Result", use_container_width=True):
    if uploaded_file:
        st.switch_page("pages/result.py")
    else:
        st.warning("Please upload an image first.")

st.markdown("</div>", unsafe_allow_html=True)

# Render isolated floating element structure away from parent HTML container bounds
with st.container():
    st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
    if st.button("💬 Chatbot", key="chat_nav_home"):
        st.switch_page("pages/chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)