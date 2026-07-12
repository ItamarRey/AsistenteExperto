import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, List
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class AgentState(TypedDict):
    question: str
    context: str
    answer: str
    history: List[BaseMessage]
    source: str

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = vector_db.as_retriever(search_kwargs={"k": 3})

llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")

system_prompt_rag = (
    "Eres un Analista Experto en League of Legends de Nivel Competitivo y un asistente RAG especializado.\n\n"
    "Tu misión principal es analizar los datos proporcionados en el contexto (JSON/documentos) y usar tu capacidad de razonamiento "
    "para ofrecer recomendaciones estratégicas personalizadas al usuario.\n\n"
    "Reglas de funcionamiento:\n"
    "1. Base de Verdad: Utiliza la información técnica de los campeones, objetos y mecánicas presentes en el contexto como cimiento "
    "de tu respuesta. No inventes estadísticas que no existan.\n"
    "2. Razonamiento Estratégico: Si el usuario plantea un escenario (ej. 'mi equipo es full AP'), integra los datos de tu base "
    "con conceptos de estrategia (meta, sinergias, counters) para dar una respuesta completa. No te limites a citar el texto; "
    "interpreta los datos para dar una solución.\n"
    "3. Integridad: Si la pregunta requiere datos que NO están en tu base vectorial (ej. 'qué tiempo hace hoy' o 'dime un chiste'), "
    "responde textualmente: 'No dispongo de esa información en mi base de conocimiento local.'\n\n"
    "Formato de Respuesta:\n"
    "- Usa negritas para destacar conceptos clave.\n"
    "- Estructura tu razonamiento en puntos claros.\n"
    "- Limita tu recomendación a un máximo de 2 campeones y, para cada campeón, aporta únicamente dos viñetas breves con la razón táctica básica.\n"
    "- Sé directo, profesional y al grano.\n\n"
    "Contexto adjunto:\n"
    "{context}"
)

system_prompt_fallback = (
    "Eres un Asistente de Análisis de League of Legends. "
    "Tu función es informar al usuario de que la información solicitada no se encuentra en la base de datos local disponible. "
    "No intentes responder con conocimiento general ni inventar datos. "
    "Tu respuesta debe ser siempre: 'Lo siento, no dispongo de esa información técnica específica en mi base de datos. Por favor, intenta reformular tu pregunta sobre campeones, objetos o estrategias incluidas en mis registros.'"
)
prompt_rag = ChatPromptTemplate.from_messages([
    ("system", system_prompt_rag),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

prompt_fallback = ChatPromptTemplate.from_messages([
    ("system", system_prompt_fallback),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

def retrieve_node(state: AgentState):
    question = state["question"]
    try:
        docs = retriever.invoke(question)
        context = "\n\n".join(doc.page_content for doc in docs)
    except Exception:
        context = ""
    return {"context": context}

def generate_rag_node(state: AgentState):
    question = state["question"]
    context = state["context"]
    history = state.get("history", [])
    chain = prompt_rag | llm
    response = chain.invoke({"context": context, "history": history, "input": question})
    
    content = response.content
    if isinstance(content, list):
        clean_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        clean_text = str(content)
        
    updated_history = history + [HumanMessage(content=question), AIMessage(content=clean_text)]
    return {"answer": clean_text, "history": updated_history, "source": "Base de Datos Local (RAG - JSON)"}

def generate_fallback_node(state: AgentState):
    question = state["question"]
    history = state.get("history", [])
    chain = prompt_fallback | llm
    response = chain.invoke({"history": history, "input": question})
    
    content = response.content
    if isinstance(content, list):
        clean_text = "".join([part.get("text", "") if isinstance(part, dict) else str(part) for part in content])
    else:
        clean_text = str(content)
        
    updated_history = history + [HumanMessage(content=question), AIMessage(content=clean_text)]
    return {"answer": clean_text, "history": updated_history, "source": "Conocimiento General (Fallback)"}

def checker_router(state: AgentState):
    answer_str = str(state["answer"]).lower()
    if "no dispongo de esa información" in answer_str:
        return "fallback"
    return "end"

workflow = StateGraph(AgentState)

workflow.add_node("retrieve", retrieve_node)
workflow.add_node("generate_rag", generate_rag_node)
workflow.add_node("generate_fallback", generate_fallback_node)

workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate_rag")

workflow.add_conditional_edges(
    "generate_rag",
    checker_router,
    {
        "fallback": "generate_fallback",
        "end": END
    }
)

workflow.add_edge("generate_fallback", END)
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

st.set_page_config(page_title="Experto en LoL", page_icon="🎮")
st.title("🤖 Experto Analítico de LoL")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = "1"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("¿Qué duda estratégica tienes?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history_lc = []
        for msg in st.session_state.messages[:-1]: 
            if msg["role"] == "user":
                history_lc.append(HumanMessage(content=msg["content"]))
            else:
                history_lc.append(AIMessage(content=msg["content"]))

        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        
        result = app.invoke(
            {"question": prompt, "history": history_lc}, 
            config=config
        )
        
        final_answer = result["answer"]
        
        st.markdown(final_answer)
        st.session_state.messages.append({"role": "assistant", "content": final_answer})