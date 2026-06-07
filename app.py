import streamlit as st
import google.generativeai as genai
import glob

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Meu Tutor de Português", page_icon="🇵🇹", layout="centered")

st.title("🤖 Your Custom AI Portuguese Tutor")
st.write("This AI reads your uploaded notes and documents to teach you!")
st.markdown("---")

# --- SIDEBAR CONFIGURATION ---
st.sidebar.title("Configuração")
# This text box allows you to paste the API key you just copied
api_key = st.sidebar.text_input("Enter Gemini API Key:", type="password")

if not api_key:
    st.info("💡 Please enter your Gemini API Key in the sidebar to wake up your tutor!")
else:
    # Safely activate the Google AI engine using your key
    genai.configure(api_key=api_key)
    
    # --- AUTOMATICALLY READ YOUR UPLOADED CUSTOM FILES ---
    # The app looks for any text files (.txt) uploaded alongside app.py on GitHub
    knowledge_base = ""
    txt_files = glob.glob("*.txt")
    
    if txt_files:
        for file in txt_files:
            with open(file, "r", encoding="utf-8") as f:
                knowledge_base += f"\n--- Source File: {file} ---\n" + f.read()
    else:
        # If you haven't uploaded any text files yet, it uses this default standard guideline
        knowledge_base = "No custom documents found yet. Use general high-quality Brazilian or European Portuguese language rules."

    # --- INTERACTIVE CHAT INTERFACE ---
    # Initialize an internal chat memory tracking so the AI remembers previous questions
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past conversation logs seamlessly on your phone screen
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Wait for you to type a prompt (e.g., "Give me a quiz based on my notes")
    if user_prompt := st.chat_input("Ask your tutor anything..."):
        # Display your new question on the screen instantly
        with st.chat_message("user"):
            st.markdown(user_prompt)
        st.session_state.messages.append({"role": "user", "content": user_prompt})

        # Secret framing background rules injected into the AI's persona
        system_instruction = (
            f"You are a strict, helpful, and highly encouraging Portuguese language tutor. "
            f"You must base your lessons, custom vocabulary, translation examples, and quizzes primarily on the following reference material:\n"
            f"{knowledge_base}\n\n"
            f"If the user attempts a quiz or types in Portuguese, evaluate their spelling/grammar and provide clear feedback."
        )

        try:
            # Wake up the fast, smart Gemini 1.5 Flash model
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Combine the systemic rule constraint with your literal message prompt
            full_prompt = f"{system_instruction}\n\nUser Request: {user_prompt}"
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                response = model.generate_content(full_prompt)
                response_placeholder.markdown(response.text)
                
            # Log the AI's response into memory
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"An error occurred while talking to the AI: {e}")