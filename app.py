import streamlit as st
import google.generativeai as genai
import glob
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Meu Tutor de Português", page_icon="🇵🇹", layout="centered")

# --- NATIVE PERMANENT BROWSER QUERY STORAGE ---
# Retrieves values locked into your unique private URL browser state
query_params = st.query_params

saved_api_key = query_params.get("api", "")
saved_user_email = query_params.get("recip", "")
saved_sender_email = query_params.get("send", "")
saved_sender_pwd = query_params.get("pwd", "")

# Manage session memory arrays natively
if "messages" not in st.session_state:
    st.session_state.messages = []

if "email_sent" not in st.session_state:
    st.session_state.email_sent = False

st.title("🇵🇹 Persistent AI Portuguese Tutor")
st.write("Your conversation data is preserved safely during your active sessions.")

# --- GLITCH 1 FIX: DYNAMIC VISUAL PROMPT ALERT ---
if st.session_state.messages and not st.session_state.email_sent:
    st.warning("⚠️ **Unsaved Drill Session Active!** Remember to tap the blue 'Email Me' button at the bottom of the screen to back up your notes before closing this browser window.")
elif st.session_state.email_sent:
    st.success("✅ Your current session transcript has been securely emailed and backed up!")

st.markdown("---")

# --- SIDEBAR CONFIGURATION (PRE-FILLED FROM URL COOKIE STATE) ---
st.sidebar.title("Configuração")
api_key = st.sidebar.text_input("Enter Gemini API Key:", value=saved_api_key, type="password")
st.sidebar.markdown("---")
st.sidebar.subheader("📬 Email Transcript Setup")
user_email = st.sidebar.text_input("Your Email Address (Recipient):", value=saved_user_email)
sender_email = st.sidebar.text_input("Sender Email Address:", value=saved_sender_email)
sender_password = st.sidebar.text_input("Sender App Password:", value=saved_sender_pwd, type="password")
smtp_server = st.sidebar.selectbox("Email Provider:", ["smtp.gmail.com", "smtp.mail.yahoo.com", "smtp-mail.outlook.com"])

# --- GLITCH 2 FIX: THE PERMANENT AUTO-LOCK BUTTON ---
if st.sidebar.button("🔒 Lock Credentials to My Phone"):
    st.query_params["api"] = api_key
    st.query_params["recip"] = user_email
    st.query_params["send"] = sender_email
    st.query_params["pwd"] = sender_password
    st.sidebar.success("🎉 Keys locked to your browser! Bookmark this page now to save them.")

if st.sidebar.button("🗑️ Clear Current Chat History"):
    st.session_state.messages = []
    st.session_state.email_sent = False
    st.rerun()

if not api_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to wake up your tutor!")
else:
    genai.configure(api_key=api_key)
    
    knowledge_base = ""
    txt_files = glob.glob("*.txt")
    if txt_files:
        for file in txt_files:
            with open(file, "r", encoding="utf-8") as f:
                knowledge_base += f"\n--- Source File: {file} ---\n" + f.read()
    else:
        knowledge_base = "Use general high-quality European Portuguese rules focused on daily life, food, and culture in Portugal."

    # --- DISPLAY INTERACTIVE CHAT ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask your tutor anything..."):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.session_state.email_sent = False 

        system_instruction = (
            f"You are an expert Portuguese language tutor teaching an English speaker. "
            f"Explain grammar and rules entirely in ENGLISH. "
            f"Focus all scenarios on daily life, navigation, traditions, and food in Portugal."
        )

        try:
            model = genai.GenerativeModel('gemini-2.5-flash')
            full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response = model.generate_content(full_prompt)
                response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")

    # --- EMAIL EXPORT MODULE ---
    if st.session_state.messages:
        st.markdown("---")
        if st.button("📧 Email Me This Session's Transcript"):
            if not user_email or not sender_email or not sender_password:
                st.warning("⚠️ Please fill out your email parameters in the sidebar setup configuration first!")
            else:
                with st.spinner("Compiling and sending transcript..."):
                    email_body = "Here is the transcript of your Portuguese learning session:\n\n"
                    for msg in st.session_state.messages:
                        speaker = "You" if msg["role"] == "user" else "AI Tutor"
                        email_body += f"[{speaker}]: {msg['content']}\n\n"
                        email_body += "-"*40 + "\n\n"

                    try:
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = user_email
                        msg['Subject'] = "🇵🇹 My Portuguese Session Transcript"
                        msg.attach(MIMEText(email_body, 'plain'))

                        server = smtplib.SMTP_SSL(smtp_server, 465)
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, user_email, msg.as_string())
                        server.quit()
                        
                        st.session_state.email_sent = True
                        st.rerun()
                    except Exception as email_err:
                        st.error(f"Failed to send email: {email_err}")
