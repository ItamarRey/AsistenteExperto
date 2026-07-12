import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Mi IA de League of Legends", page_icon="🎮")
st.title("🤖 Consultor Estratégico LoL")

# Inicializar modelo (usando secret para la API Key)
if "llm" not in st.session_state:
    st.session_state.llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        google_api_key=st.secrets["GOOGLE_API_KEY"]
    )

# Historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input del usuario
if prompt := st.chat_input("¿Qué duda estratégica tienes?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Respuesta de la IA
    with st.chat_message("assistant"):
        response = st.session_state.llm.invoke(prompt)
        st.markdown(response.content)
        st.session_state.messages.append({"role": "assistant", "content": response.content})