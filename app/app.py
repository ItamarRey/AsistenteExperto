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
        
        # --- NUEVA LÓGICA DE LIMPIEZA ---
        texto_final = ""
        
        # 1. Intentar obtener el contenido de forma estándar
        raw_text = getattr(response, 'content', str(response))
        
        # 2. Si raw_text parece una lista/diccionario (lo que te está pasando)
        if raw_text.strip().startswith("[{") and "'text':" in raw_text:
            import ast
            try:
                # Intentamos convertir el string técnico a una lista real de Python
                lista_obj = ast.literal_eval(raw_text)
                # Extraemos el campo 'text' del primer elemento
                texto_final = lista_obj[0].get('text', str(raw_text))
            except:
                texto_final = str(raw_text)
        else:
            texto_final = raw_text

        # 3. Mostrar y guardar
        st.markdown(texto_final)
        st.session_state.messages.append({"role": "assistant", "content": texto_final})