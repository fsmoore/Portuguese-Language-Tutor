import streamlit as st
import google.generativeai as genai
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Meu Tutor de Português", page_icon="🇵🇹", layout="centered")

# --- HARDCODED PERMANENT CREDENTIALS MANAGER ---
PERMANENT_GEMINI_API_KEY = "AIzaSy" + "AQ.Ab8RN6LPS7ghlvuLH5dWQSqShHk_wxApxvd9VPSVkp0vFj7Vig" # Fixed API structure
PERMANENT_RECIPIENT_EMAIL = "fsmoore@pacbell.net"
PERMANENT_SENDER_EMAIL = "frankscottmoore@gmail.com"
PERMANENT_SENDER_APP_PASSWORD = "jhnolpnawyjygkcl"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

st.title("🇵🇹 Permanent AI Portuguese Tutor")
st.write("Your credentials are permanently locked into your cloud application pipeline.")
st.markdown("---")

# --- SIDEBAR DISPLAY (READ-ONLY REFERENCE PANEL) ---
st.sidebar.title("Configuração")
st.sidebar.info("🔒 Credentials securely hardcoded into the backend. No configuration required!")
st.sidebar.markdown("---")
st.sidebar.subheader("📬 System Parameters")
st.sidebar.text(f"Recipient: {PERMANENT_RECIPIENT_EMAIL}")
st.sidebar.text(f"Sender: {PERMANENT_SENDER_EMAIL}")

if st.sidebar.button("🗑️ Clear Current Chat History"):
    st.session_state.messages = []
    st.session_state.email_sent = False
    st.rerun()

# --- INITIALIZE CORE AI ENGINE ---
try:
    genai.configure(api_key=PERMANENT_GEMINI_API_KEY)
except Exception as config_err:
    st.error(f"Configuration Initialization Error: {config_err}")

knowledge_base = ""
txt_files = glob.glob("*.txt")
if txt_files:
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as f:
            knowledge_base += f"\n--- Source File: {file} ---\n" + f.read()
else:
    knowledge_base = "Use general high-quality European Portuguese rules focused on daily life, food, and culture in Portugal."

# --- DISPLAY ACTIVE DRILLS ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- THE SAFETY NET: TRANSCRIPT WARNING PROMPT ---
if st.session_state.messages:
    if not st.session_state.email_sent:
        st.error("⚠️ **UNSAVED DRILL SESSION ACTIVE:** Please scroll down and tap the blue button to email your transcript before closing the app, or your current practice data will clear out!")
    else:
        st.success("✅ Transcript emailed successfully! It is now safe to close your app or clear the history.")

if user_prompt := st.chat_input("Ask your tutor anything..."):
    with st.chat_message("user"):
        st.markdown(user_prompt)
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.session_state.email_sent = False 

    system_instruction = (
        f"You are an expert Portuguese language tutor teaching an English speaker. "
        f"Explain grammar and rules entirely in ENGLISH. "
        f"Focus all scenarios on daily life, navigation, traditions, and food in Portugal.\n\n"
        f"Base context rules on this text content:\n{knowledge_base}"
    )

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response = model.generate_content(full_prompt)
            response_placeholder.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.rerun()
    except Exception as e:
        st.error(f"AI Connection Error: {e}")

# --- EMAIL AUTOMATION EXPORT LINK ---
if st.session_state.messages:
    st.markdown("---")
    if st.button("📧 Email Me This Session's Transcript"):
        with st.spinner("Compiling and sending transcript..."):
            email_body = "Here is the transcript of your Portuguese learning session:\n\n"
            for msg in st.session_state.messages:
                speaker = "You" if msg["role"] == "user" else "AI Tutor"
                email_body += f
