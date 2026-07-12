# 🚀 Asistente Experto en League of Legends - RAG Agent

Este proyecto implementa un asistente inteligente especializado en el análisis de datos de League of Legends mediante una arquitectura **RAG (Retrieval-Augmented Generation)** avanzada integrada en un flujo de agentes cognitivos con **LangGraph**.

---

## 1. Descripción del Dominio Elegido

El dominio seleccionado para este proyecto es el entorno competitivo y estratégico de **League of Legends (LoL)**. La información del juego es masiva, cambia constantemente con los parches y requiere una alta precisión técnica. Para alimentar la base de conocimiento del asistente, los datos se han estructurado en tres grandes bloques a través de archivos JSON locales:

* **Campeones (`league_of_legends_champions.json`):** Contiene el listado de personajes, sus roles, mecánicas básicas y descripciones de habilidades.
* **Objetos (`league_of_legends_items.json`):** Almacena las estadísticas de los ítems, costes de oro, componentes de recetas y efectos pasivos/activos.
* **Macroestrategia (`league_of_legends_macro.json`):** Define conceptos fundamentales del juego de alto nivel, tales como el control de oleadas, gestión de la visión, rotaciones tácticas y toma de objetivos neutrales (Barón/Dragón).

El objetivo del agente es actuar como un analista de eSports capaz de extraer datos exactos de estos archivos para responder dudas complejas sin mezclar conceptos ni inventar datos.

---

## 2. Requisitos del Sistema

Para el correcto funcionamiento de la aplicación, el entorno debe contar con los siguientes elementos:

### Variables de Entorno (API Key)
El sistema requiere acceso a los modelos fundacionales de Google. Es necesario disponer de una clave de API de **Google AI Studio** configurada en el sistema como variable de entorno:
* `GOOGLE_API_KEY` (o en su defecto `GEMINI_API_KEY`)

### Dependencias del Proyecto
El núcleo del software se apoya en el ecosistema moderno de agentes y bases de datos vectoriales. Las librerías obligatorias son:
* `langchain-core` & `langchain-community` (Gestión de componentes y LCEL)
* `langchain-google-genai` (Conexión nativa con los LLM y embeddings de Gemini)
* `chromadb` (Base de datos vectorial para el almacenamiento persistente)
* `langgraph` (Orquestación del flujo del agente basado en grafos de estado)

---

## 3. Instrucciones de Instalación y Ejecución

Sigue estos pasos en tu terminal para clonar, configurar y desplegar el entorno de ejecución de forma limpia:

```bash
python -m venv venv_asistente
source venv_asistente/bin/activate
pip install langchain langchain-community langchain-core langchain-google-genai chromadb langgraph
```

*(Nota para usuarios de Windows: Utilizar `venv_asistente\Scripts\activate` para activar el entorno).*

Para configurar tu API Key en la sesión actual de la terminal ejecutas:

```bash
export GOOGLE_API_KEY="tu_api_key_aqui"
```

*(Nota para usuarios de Windows en CMD: Utilizar `set GOOGLE_API_KEY="tu_api_key_aqui"`).*

### Ejecución del Proyecto
1. Asegúrate de tener los archivos de datos en la ruta `data/`.
2. Ejecuta el script de indexación inicial para generar la base de datos persistente en la carpeta `./chroma_db`.
3. Lanza el archivo principal del agente desde tu entorno de Jupyter Notebook

---

## 4. Justificación del System Prompt y Evolución

El agente utiliza una estructura de dos niveles en LangGraph para alternar de forma eficiente entre la base de datos local y el conocimiento general.

### 4.1. Prompt RAG Principal (`system_prompt_rag`)
Fuerza al modelo a depender exclusivamente del contexto inyectado de ChromaDB.

```text
Eres un Analista Experto en League of Legends de Nivel Competitivo y un asistente RAG especializado. Tu único objetivo es responder a las consultas de los usuarios utilizando exclusivamente los datos proporcionados en el contexto adjunto.

Pautas de comportamiento obligatorias:
1. Confianza Absoluta en el Contexto: Si los datos necesarios para responder a la pregunta no se encuentran explícitamente en el fragmento de texto proporcionado, tu respuesta debe ser textualmente: "No dispongo de esa información en mi base de conocimiento local." No intentes rellenar huecos, deducir datos no escritos ni inventar mecánicas.
2. Neutralidad y Rigor: Mantén un tono técnico, analítico y directo. Evita opiniones personales que no estén respaldadas por los JSON de origen.
3. Tratamiento de Campeones y Objetos: Si te preguntan por un campeón u objeto que aparece en el contexto pero los detalles específicos (como sus builds o estadísticas completas) faltan, indícalo detallando qué información exacta sí tienes disponible.

Formato de Respuesta:
- Usa negritas para destacar palabras clave, nombres de campeones, habilidades u objetos.
- Si vas a listar elementos o estadísticas, estructúralos siempre en listas de puntos limpios.
- Evita párrafos excesivamente largos; prioriza la legibilidad inmediata.

Contexto adjunto: {context}
```

* **Cero Alucinaciones:** Obliga a emitir la negativa exacta si el dato no existe en los JSON.
* **Transparencia:** El modelo admite si conoce el término pero carece de los detalles específicos.

---

### 4.2. Prompt de Escape (`system_prompt_fallback`)
Actúa como red de seguridad si el enrutador condicional detecta el mensaje de bloqueo del RAG.

```text
Eres un Analista Experto en League of Legends de Nivel Competitivo.

La base de conocimiento local no contiene datos específicos para esta consulta. Responde utilizando tu conocimiento general del meta de forma extremadamente concisa, directa y al grano.

Pauta obligatoria: Comienza tu respuesta integrando de forma fluida y profesional en el primer párrafo que, ante la falta de registros específicos en la base local, vas a ofrecer un análisis estratégico basado en los fundamentos generales del juego competitivo. No uses corchetes ni etiquetas robóticas.

Restricciones de formato:
- Limita tu recomendación a un máximo de 2 campeones.
- Para cada campeón, aporta únicamente dos viñetas breves con la razón táctica básica.
- No te extiendas con introducciones extensas ni conclusiones innecesarias.
```

---

### 4.3. Toma de Decisiones y Cambios Aplicados

* **Optimización del Tiempo de Respuesta (Tijeretazo Táctico):** Las primeras pruebas generaban textos demasiado largos. En una fase de selección de campeón (*Champion Select*), el usuario necesita decidir rápido. Se limitó el formato a un **máximo de 2 campeones** y **2 viñetas directas**.
* **Humanización de la Contingencia:** Se eliminaron las etiquetas rígidas entre corchetes (`[Nota del Analista]`) por resultar artificiales. Ahora el analista justifica la falta de datos locales de manera fluida y orgánica en su narrativa inicial, manteniendo la honestidad del RAG sin romper la experiencia de usuario.