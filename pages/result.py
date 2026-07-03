import streamlit as st
from PIL import Image
import tensorflow as tf
import numpy as np
from pathlib import Path
from streamlit_float import float_init
import pandas as pd

st.set_page_config(
    page_title="Diagnosis Result",
    page_icon="🩺",
    layout="centered"
)

float_init()

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "skin_cancer_model.h5"

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(MODEL_PATH, compile=False)

model = load_model()

# Theme sync configuration check
dark = st.session_state.get("dark_mode", True)

if dark:
    bg = "#0E1117"
    text = "white"
    box = "#1E1E1E"
else:
    bg = "#FFFFFF"
    text = "black"
    box = "#F5F5F5"

st.markdown(f"""
<style>
.stApp {{
    background-color:{bg};
}}

.container {{
    background-color:{box};
    padding:40px;
    border-radius:15px;
    margin-top:50px;
    text-align:center;
}}

h1 {{
    color:{text};
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
""", unsafe_allow_html=True)

st.markdown("<div class='container'>", unsafe_allow_html=True)

st.title("Diagnosis Result")

image = st.session_state.get("uploaded_image")

if image is None:
    st.error("No image found.")
    st.stop()

c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image(image, width=300)

# Preprocess uploaded image matrices
img = image.resize((224,224))      
img = np.array(img)

# Convert RGBA matrix structures to flat RGB
if img.shape[-1] == 4:
    img = img[:, :, :3]

img = img / 255.0
img = np.expand_dims(img, axis=0)

# Model analysis prediction
prediction = model.predict(img)
predicted_class = np.argmax(prediction)
confidence = np.max(prediction) * 100

class_names = {
    0: "Actinic Keratoses",
    1: "Basal Cell Carcinoma",
    2: "Benign Keratosis",
    3: "Dermatofibroma",
    4: "Melanoma",
    5: "Melanocytic Nevi",
    6: "Vascular Lesions"
}

# Evaluate classification outputs
if predicted_class in [1, 4]:
    st.markdown("<h2 style='color:red;'>Warning!</h2>", unsafe_allow_html=True)
elif predicted_class in [0]:
    st.markdown("<h2 style='color:orange;'>Safe, but still consult a dermatologist if you notice changes.</h2>", unsafe_allow_html=True)
else:
    st.markdown("<h2 style='color:green;'>Congrats! You are cancer free!</h2>", unsafe_allow_html=True)

st.subheader("Predicted Disease")
st.success(class_names[predicted_class])
st.metric(label="Confidence", value=f"{confidence:.2f}%")

# Generate statistical data chart frame
df = pd.DataFrame(
    {
        "Disease": class_names.values(),
        "Probability": prediction[0]
    }
)

st.subheader("Prediction Probabilities")
st.bar_chart(df.set_index("Disease"))

if st.button("Back"):
    st.switch_page("app.py")

# Close structural main element card tag before handling isolated floating objects
st.markdown("</div>", unsafe_allow_html=True)

# Render standalone isolated floating navigation button wrapper logic safely
with st.container():
    st.markdown('<div class="floating-chat-container">', unsafe_allow_html=True)
    if st.button("💬 Chatbot", key="chat_nav_result"):
        st.switch_page("pages/chatbot.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.divider()
st.caption(
    "⚠️ This application is intended for educational purposes only. "
    "It does not replace professional medical diagnosis. "
    "Please consult a qualified dermatologist for medical advice."
)