import streamlit as st

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="Português Avançado",
    page_icon="🇵🇹",
    layout="centered"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Módulos de Lição")
tutorial_section = st.sidebar.radio(
    "Escolha uma lição:",
    [
        "1. Saudações (Greetings)", 
        "2. Verbos Essenciais", 
        "3. Gênero dos Substantivos (Nouns)",
        "4. Flashcards de Vocabulário",
        "5. Quiz de Prática"
    ]
)

# --- TITLE ---
st.title("Olá! 🇵🇹 Welcome to Portuguese")
st.write("Seu guia interativo para dominar o idioma.")
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
        st.markdown("* **Eu sou** (I am)\n* **Você é** (You are)\n* **Ele/Ela é** (He/She is)\n* **Nós somos** (We are)")
        st.caption("Example: *Eu sou americano.* (I am American.)")
    with col2:
        st.subheader("Estar (Temporary)")
        st.markdown("* **Eu estou** (I am)\n* **Você está** (You are)\n* **Ele/Ela está** (He/She is)\n* **Nós estamos** (We are)")
        st.caption("Example: *Eu estou cansado.* (I am tired right now.)")

# --- NEW SECTION 3: NOUN GENDERS ---
elif tutorial_section == "3. Gênero dos Substantivos (Nouns)":
    st.header("Lesson 3: Masculine vs. Feminine Nouns")
    st.write("In Portuguese, all nouns have a gender. Articles change based on the word's gender.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("**Masculine (O / Um)**")
        st.write("* Usually ends in **-o**")
        st.write("* **O** livro (The book)")
        st.write("* **Um** carro (A car)")
    with col2:
        st.error("**Feminine (A / Uma)**")
        st.write("* Usually ends in **-a**")
        st.write("* **A** mesa (The table)")
        st.write("* **Uma** maçã (An apple)")

# --- NEW SECTION 4: FLASHCARDS ---
elif tutorial_section == "4. Flashcards de Vocabulário":
    st.header("Interactive Vocabulary Flashcards")
    st.write("Click to reveal the translation!")
    
    card_col1, card_col2, card_col3 = st.columns(3)
    
    with card_col1:
        with st.expander("🇵🇹 A água"):
            st.write("🇺🇸 The water")
    with card_col2:
        with st.expander("🇵🇹 O amigo"):
            st.write("🇺🇸 The friend")
    with card_col3:
        with st.expander("🇵🇹 A casa"):
            st.write("🇺🇸 The house")

# --- SECTION 5: QUIZ ---
elif tutorial_section == "5. Quiz de Prática":
    st.header("Test Your Knowledge! 🧠")
    
    q1 = st.radio("How do you say 'Good morning' in Portuguese?", ["Boa noite", "Bom dia", "Olá", "Por favor"])
    if st.button("Submit Answer 1"):
        if q1 == "Bom dia": st.success("Muito bem! 🎉")
        else: st.error("Try again!")
        
    st.markdown("---")
    
    q2 = st.radio("Which article goes with 'livro' (book)?", ["A (Feminine)", "O (Masculine)"])
    if st.button("Submit Answer 2"):
        if q2 == "O (Masculine)": st.success("Correto! Masculine nouns use 'O'.")
        else: st.error("Not quite! 'Livro' ends in -o, making it masculine.")