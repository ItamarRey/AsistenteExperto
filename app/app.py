import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="Experto en LoL", page_icon="🎮")
st.title("🤖 Experto Analítico de LoL")

if "llm" not in st.session_state:
    st.session_state.llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
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
        
        # --- SOLUCIÓN ROBUSTA ---
        content = response.content
        
        if isinstance(content, list):
            # Si el contenido es una lista (formato complejo), extraemos el texto de cada parte
            final_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
        else:
            # Si es un string simple, lo tomamos directamente
            final_text = content
        # ------------------------

        st.markdown(final_text)
        st.session_state.messages.append({"role": "assistant", "content": final_text})