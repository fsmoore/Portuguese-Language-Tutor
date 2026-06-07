import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Português Tutorial",
    page_icon="🇵🇹",
    layout="centered"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navegação")
tutorial_section = st.sidebar.radio(
    "Ir para a lição:",
    ["1. Saudações (Greetings)", "2. Verbos Essenciais", "3. Quiz Interativo"]
)

# --- TITLE ---
st.title("Olá! 🇵🇹 Welcome to Portuguese")
st.write("Convertemos o seu Notebook em uma lição interativa.")
st.markdown("---")

# --- SECTION 1: GREETINGS ---
if tutorial_section == "1. Saudações (Greetings)":
    st.header("Lesson 1: Common Greetings")
    st.write("Here are the most common ways to greet people in Portuguese:")
    
    vocab = {
        "Portuguese": ["Olá", "Bom dia", "Boa tarde", "Boa noite", "Por favor", "Obrigado/a"],
        "English": ["Hello / Hi", "Good morning", "Good afternoon", "Good evening / night", "Please", "Thank you (m/f)"]
    }
    st.table(vocab)
    
    st.info("💡 **Quick Tip:** Men say *Obrigado* and women say *Obrigada*, regardless of who they are talking to!")

# --- SECTION 2: ESSENTIAL VERBS ---
elif tutorial_section == "2. Verbos Essenciais":
    st.header("Lesson 2: The Two 'To Be' Verbs")
    st.write("Portuguese uses two different verbs for 'to be': **Ser** (permanent) and **Estar** (temporary).")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ser (Permanent)")
        st.markdown("""
        * **Eu sou** (I am)
        * **Você é** (You are)
        * **Ele/Ela é** (He/She is)
        * **Nós somos** (We are)
        """)
        st.caption("Example: *Eu sou americano.* (I am American.)")

    with col2:
        st.subheader("Estar (Temporary)")
        st.markdown("""
        * **Eu estou** (I am)
        * **Você está** (You are)
        * **Ele/Ela está** (He/She is)
        * **Nós estamos** (We are)
        """)
        st.caption("Example: *Eu estou cansado.* (I am tired right now.)")

# --- SECTION 3: INTERACTIVE QUIZ ---
elif tutorial_section == "3. Quiz Interativo":
    st.header("Test Your Knowledge! 🧠")
    st.write("Answer the question below to test your skills.")
    
    q1 = st.radio(
        "How do you say 'Good morning' in Portuguese?",
        ["Boa noite", "Bom dia", "Olá", "Por favor"]
    )
    
    if st.button("Submit Answer"):
        if q1 == "Bom dia":
            st.success("Muito bem! 🎉 'Bom dia' is correct!")
        else:
            st.error("Not quite! Try again. (Hint: 'Dia' means day).")