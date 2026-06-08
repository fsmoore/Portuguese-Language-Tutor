import streamlit as st
import google.generativeai as genai
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Meu Tutor de Português", page_icon="🇵🇹", layout="centered")

st.title("🤖 Your Custom AI Portuguese Tutor")
st.write("This AI reads your uploaded notes and documents to teach you!")
st.markdown("---")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("Configuração")
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

# --- NEW FEATURE: EMAIL CREDENTIALS IN SIDEBAR ---
st.sidebar.markdown("---")
st.sidebar.subheader("📬 Email Transcript Setup")
user_email = st.sidebar.text_input("Your Email Address (Recipient):")
sender_email = st.sidebar.text_input("Sender Email Address:")
sender_password = st.sidebar.text_input("Sender App Password:", type="password")
smtp_server = st.sidebar.selectbox("Email Provider:", ["smtp.gmail.com", "smtp.mail.yahoo.com", "smtp-mail.outlook.com"])

if not api_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to wake up your tutor!")
else:
    genai.configure(api_key=api_key)
    
    # --- AUTOMATICALLY READ YOUR UPLOADED CUSTOM FILES ---
    knowledge_base = ""
    txt_files = glob.glob("*.txt")
    if txt_files:
        for file in txt_files:
            with open(file, "r", encoding="utf-8") as f:
                knowledge_base += f"\n--- Source File: {file} ---\n" + f.read()
    else:
        knowledge_base = "No custom documents found yet. Use general high-quality Brazilian or European Portuguese language rules."

    # --- INTERACTIVE CHAT INTERFACE ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_prompt := st.chat_input("Ask your tutor anything..."):
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        system_instruction = (
            f"You are an expert Portuguese language tutor teaching an English speaker. "
            f"CRITICAL RULE 1: You must communicate, explain grammar, and provide feedback entirely in ENGLISH. "
            f"Only the Portuguese vocabulary and practice phrases should be in Portuguese.\n\n"
            f"CRITICAL RULE 2: The absolute concentration of all lessons, vocabulary examples, exercises, and contextual scenarios MUST be daily life, culture, traditions, navigation, and food in Portugal. "
            f"NEVER use examples related to technology, artificial intelligence, Google, or computer programming.\n\n"
            f"Base your lessons primarily on this reference material:\n"
            f"{knowledge_base}\n\n"
            f"Always provide clear English translations for any Portuguese examples you use."
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
            st.error(f"An error occurred while talking to the AI: {e}")

    # --- NEW FEATURE: EMAIL EXPORT BUTTON ---
    if st.session_state.messages:
        st.markdown("---")
        if st.button("📧 Email Me This Session's Transcript"):
            if not user_email or not sender_email or not sender_password:
                st.warning("⚠️ Please configure your email setup details in the sidebar first!")
            else:
                with st.spinner("Compiling and sending transcript..."):
                    # Format the chat history into a clear readable text format
                    email_body = "Here is the transcript of your Portuguese learning session:\n\n"
                    for msg in st.session_state.messages:
                        speaker = "You" if msg["role"] == "user" else "AI Tutor"
                        email_body += f"[{speaker}]: {msg['content']}\n\n"
                        email_body += "-"*40 + "\n\n"

                    try:
                        # Set up the secure email protocol
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = user_email
                        msg['Subject'] = "🇵🇹 My Portuguese Session Transcript"
                        msg.attach(MIMEText(email_body, 'plain'))

                        # Securely connect to the email provider server and send
                        server = smtplib.SMTP(smtp_server, 587)
                        server.starttls()
                        server.login(sender_email, sender_password)
                        server.sendmail(sender_email, user_email, msg.as_string())
                        server.quit()
                        
                        st.success("🎉 Transcript emailed successfully! Check your inbox.")
                    except Exception as email_err:
                        st.error(f"Failed to send email: {email_err}")