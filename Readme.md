# 🚀 Asistente Experto en League of Legends - RAG Agent

## 1. Descripción del dominio elegido
El dominio seleccionado para este proyecto es el entorno competitivo y estratégico de **League of Legends (LoL)**. La información del juego es masiva y cambia constantemente, requiriendo una alta precisión técnica. Para alimentar la base de conocimiento del asistente, los datos se han estructurado en tres bloques clave a través de archivos JSON locales:

* **Campeones:** Roles, mecánicas y habilidades.
* **Objetos:** Estadísticas, costes y efectos pasivos/activos.
* **Macroestrategia:** Control de oleadas, visión y rotaciones.

El objetivo del agente es actuar como un analista de eSports capaz de extraer datos exactos de estos archivos para responder dudas complejas sin mezclar conceptos ni inventar datos.

## 2. Instrucciones de instalación y ejecución
Sigue estos pasos para levantar el entorno:

1. **Clonar el repositorio:** Descarga el proyecto en tu máquina local.
2. **Instalar dependencias:** Ejecuta en tu terminal:
   `pip install -r requirements.txt`
3. **Ejecutar la aplicación:** Lanza la interfaz web con:
   `streamlit run app.py`

*Nota: No es necesario subir la carpeta `chroma_db/` a GitHub. El sistema generará automáticamente la base de datos vectorial local al ejecutar el script de ingesta por primera vez.*

## 3. Justificación del system prompt
Para garantizar la precisión, se ha implementado una arquitectura de doble sistema de prompts (RAG vs Fallback) para asegurar que el agente siempre mantenga su integridad técnica.

### System Prompt RAG (Analista Experto)
Utilizado para procesar consultas con contexto recuperado:

```text
Eres un Analista Experto en League of Legends de Nivel Competitivo y un asistente RAG especializado.

Tu misión principal es analizar los datos proporcionados en el contexto (JSON/documentos) y usar tu capacidad de razonamiento para ofrecer recomendaciones estratégicas personalizadas al usuario.

Reglas de funcionamiento:
1. Base de Verdad: Utiliza la información técnica de los campeones, objetos y mecánicas presentes en el contexto como cimiento de tu respuesta. No inventes estadísticas que no existan.
2. Razonamiento Estratégico: Si el usuario plantea un escenario (ej. 'mi equipo es full AP'), integra los datos de tu base con conceptos de estrategia (meta, sinergias, counters) para dar una respuesta completa. No te limites a citar el texto; interpreta los datos para dar una solución.
3. Integridad: Si la pregunta requiere datos que NO están en tu base vectorial (ej. 'qué tiempo hace hoy' o 'dime un chiste'), responde textualmente: 'No dispongo de esa información en mi base de conocimiento local.'

Formato de Respuesta:
- Usa negritas para destacar conceptos clave.
- Estructura tu razonamiento en puntos claros.
- Limita tu recomendación a un máximo de 2 campeones y, para cada campeón, aporta únicamente dos viñetas breves con la razón táctica básica.
- Sé directo, profesional y al grano.

Contexto adjunto:
{context}
```

### System Prompt Fallback (Red de Seguridad)
```text
Eres un Asistente de Análisis de League of Legends. 

Tu función es informar al usuario de que la información solicitada no se encuentra en la base de datos local disponible. 
No intentes responder con conocimiento general ni inventar datos. Tu respuesta debe ser siempre: 'Lo siento, no dispongo de esa información técnica específica en mi base de datos. Por favor, intenta reformular tu pregunta sobre campeones, objetos o estrategias incluidas en mis registros.'
```

## 4. Requisitos (dependencias, API key de Gemini)
Para el correcto funcionamiento del sistema, asegúrate de tener instalado Python 3.10+ y las siguientes librerías incluidas en `requirements.txt`:

- streamlit
- langchain
- langchain-google-genai
- langgraph
- chromadb
- langchain-chroma
- python-dotenv

**API Key:** Es indispensable configurar tu `GEMINI_API_KEY`. Debes crear un archivo `.env` en la raíz del proyecto con la variable:
`GEMINI_API_KEY=tu_clave_de_api_aqui`

## 5. Demo de consulta

A continuación se presentan 5 ejemplos representativos de las capacidades del sistema, donde el modelo aplica razonamiento sobre el contexto cargado en la base de datos vectorial para ofrecer recomendaciones tácticas.

### Pregunta 1: Estrategia de inicio en línea
* **Pregunta:** Con Aatrox, ¿qué habilidad debo priorizar al nivel 1 para asegurar un tradeo favorable y cuál es mi mayor power spike en los primeros niveles?

    > **Respuesta del sistema:**
    > * Para asegurar un tradeo favorable con **Aatrox** en el nivel 1, tu elección estratégica debe ser:
    >  **Prioridad de habilidad:** Debes subir **"La Espada de los Darkin" (Q)**.
    >    *   **Razonamiento:** Es tu fuente principal de daño y control de masas. Al nivel 1, te permite realizar el *poke* o el intercambio de daño manteniéndote a una distancia segura. Si logras conectar el "borde" (el *sweet spot*) de la Q, no solo infliges daño aumentado, sino que también aplicas un efecto de levantamiento (*knock-up*), lo que te permite ganar el intercambio sin recibir daño de retorno significativo de la mayoría de los campeones cuerpo a cuerpo.
    > *  **Power Spike en los primeros niveles:** Tu mayor pico de poder reside en el **Nivel 3**.
    >    *   **Razonamiento:** En el nivel 3, desbloqueas el combo completo de tus habilidades básicas: **Q, W y E**.
    >       *   La **Q** te proporciona el daño y control.
    >        *   La **W (Cadenas infernales)** te permite asegurar el impacto de las siguientes activaciones de tu Q al ralentizar al enemigo y atraerlo al centro.
    >        *   La **E (Deslizamiento oscuro)** es crítica aquí: te permite reposicionarte para asegurar el *sweet spot* de la Q mientras infliges daño, y te otorga **omnivampirismo**, permitiéndote sostener el intercambio de vida de manera mucho más eficiente que tu oponente.
    > * **Consejo táctico:** No busques un intercambio prolongado en el nivel 1. Utiliza la Q para desgastar, y espera al nivel 3 para buscar una rotación completa de habilidades que fuerce un *flash* o asegure una ventaja de vida definitiva en la línea.
### Pregunta 2: Counterplay de objetos
* **Pregunta:** El rival se ha comprado Corazón de Acero de primer ítem. ¿Qué objeto debo comprar yo para contrarrestar su escalado de vida y no perder el 1v1 en línea?

    > **Respuesta del sistema:**
    >
    > Para contrarrestar un **Corazón de Acero** (Heartsteel) en fase de líneas, el objetivo principal no es solo comprar daño, sino **daño porcentual de vida** y **penetración de armadura**.
    >
    > Basándome en la premisa de que estás jugando con un coloso (como Aatrox, según tu consulta anterior, u otros campeones similares), aquí tienes la mejor estrategia de itemización:
    >
    > * **Tu objeto clave: Desgarrador Divino (o Eclipse, dependiendo del caso):**
    >   * Si buscas una respuesta directa al escalado de vida, el **Desgarrador Divino** (si está disponible en tu versión actual) o el **Eclipse** son fundamentales. El **Eclipse** te otorga daño basado en la vida máxima del objetivo, lo cual neutraliza la ventaja que el rival obtiene al acumular salud con el Corazón de Acero.
    >
    > * **Opción de daño por vida máxima: Rencor de Serylda o Recordatorio Mortal:**
    >   * Al comprar el Corazón de Acero, el rival inevitablemente también ganará una cantidad significativa de armadura en su *build* posterior. Priorizar un objeto con **penetración de armadura porcentual** (como el **Rencor de Serylda**) te permitirá seguir perforando su defensa aunque tenga una barra de vida masiva.
    >
    > * **El factor "Daño por Vida Máxima":**
    >   * Si tu campeón permite el uso de **Botarruinas** (si es un atacante básico) o **Desgarrador**, priorízalos. El daño porcentual es el único lenguaje que entiende un rival que apuesta todo a la vida máxima.
    >
    > **Análisis Estratégico para el 1v1:**
    > 1. **No busques el *all-in* prolongado:** El Corazón de Acero se carga cuando el rival te golpea. Si peleas de forma extendida, le permites aplicar la pasiva del objeto varias veces.
    > 2. **Gestiona los tiempos:** Si ves que el rival tiene la carga lista (el sonido característico del objeto), **retrocede**. Es mejor ceder unos súbditos que permitirle obtener 50-100 de vida máxima gratis.
    > 3. **Prioriza el escalado:** Si compras objetos con daño porcentual, escalarás mejor que él en el *mid-game*, ya que el Corazón de Acero es un objeto de "bola de nieve" que se vuelve menos efectivo a medida que tus objetos de penetración comienzan a completar su *build*.
    >
    > **Nota:** Si el rival está usando campeones como **Skarner, Mordekaiser o Nasus**, recuerda que el daño porcentual es obligatorio, ya que estos campeones escalan sus propias defensas o curaciones basándose en los intercambios largos que el Corazón de Acero fomenta.

### Pregunta 3: Macrogame y toma de decisiones
* **Pregunta:** Estoy en una situación de macrogame complicada: hemos ganado una pelea en top, pero el dragón está activo y el equipo enemigo está pusheando mid. ¿Qué es mejor: priorizar la torre de tier 1 en top para abrir el mapa o rotar inmediatamente a asegurar el dragón?

    > **Respuesta del sistema:**
    >
    > Para tomar la decisión correcta, debemos aplicar el principio de **Gestión de Prioridades de Mapa** y **Valor de Objetivos**. Aquí tienes el análisis estratégico para tu situación:
    >
    > **1. La Regla de Oro: El Dragón como Prioridad de Equipo**
    > Si el dragón está activo y tu equipo ha ganado una pelea en top (especialmente si has forzado muertes o retiradas), la **rotación inmediata al dragón** suele ser la jugada de mayor valor competitivo por las siguientes razones:
    >
    > * **Control de la "Soul" y Buffs Permanentes:** Los dragones proporcionan beneficios globales acumulativos que escalan durante toda la partida. Una torre de Tier 1, aunque abre el mapa, es un objetivo estático que puedes tomar después. El dragón es un objetivo que el equipo enemigo puede disputar o robar si tardas demasiado.
    > * **Neutralización de la presión en Mid:** Al rotar al dragón, estás obligando al equipo enemigo a elegir: o defienden el dragón (abandonando el push en mid) o continúan en mid (cediendo el dragón). Si tú rotas primero, ganas la **iniciativa de posición** (*set-up*), permitiéndote colocar visión y forzar al enemigo a caminar hacia una zona donde ustedes ya tienen la ventaja numérica.
    >
    > **2. ¿Cuándo sí deberías priorizar la Torre de Top?**
    > Solo debes ignorar la rotación al dragón si se cumplen estas condiciones específicas:
    > * **El estado de la línea:** Si la oleada en top está estrellada contra su torre y puedes derribarla rápidamente (menos de 5-8 segundos) antes de que el enemigo se organice.
    > * **El tipo de Dragón:** Si es un dragón poco relevante (ej. el primer dragón de la partida) y tu equipo está muy bajo de vida, arriesgarse a una pelea de dragón puede ser un error. En ese caso, asegurar el oro de la torre es una ganancia garantizada.
    > * **Tu capacidad de empuje:** Si eres un *splitpusher* con gran capacidad de derribar estructuras rápidamente, el valor de la torre puede ser mayor si eso obliga a un miembro clave del enemigo a dejar de presionar mid para ir a responderte a ti en top, aliviando la presión en el resto del mapa.
    >
    > **3. Recomendación Táctica (El "Macro" Óptimo)**
    > En un nivel competitivo, la secuencia correcta suele ser:
    > 1. **Limpiar la oleada:** Si puedes, empuja la oleada de top rápidamente bajo su torre para que la estructura sufra daño por sí sola o para que el enemigo tenga que decidir si defenderla.
    > 2. **Rotación inmediata:** Múvete hacia el dragón pasando por la jungla enemiga para **limpiar visión**.
    > 3. **Presión de mapa:** Al ganar el dragón, tu equipo tendrá la ventaja necesaria para reagruparse y rotar a mid con superioridad numérica, neutralizando el push que ellos estaban intentando.
    >
    > **Veredicto:** **Prioriza el dragón.** Es el objetivo que define el ritmo del juego en el *mid-game*. La torre de top es una ganancia menor que no compensa el riesgo de perder un dragón y, consecuentemente, ceder el control del río.

### Pregunta 4: Equilibrio de composición
* **Pregunta:** Mi equipo es full AP y nos falta daño físico para cerrar la partida. De todos los campeones que tienes en tu base de datos, ¿cuál encaja mejor para balancear la composición y ser efectivo en teamfights de late game?

    > **Respuesta del sistema:**
    >
    > Analizando los campeones disponibles en tu base de datos (**Aphelios, Alistar, Dr. Mundo**) y considerando el problema de un equipo **full AP**, la elección estratégica es clara:
    >
    > **El Campeón Recomendado: Aphelios**
    >
    > Para balancear una composición que sufre por la falta de daño físico (*AD*), **Aphelios** es la opción superior. Aquí el razonamiento estratégico:
    >
    > * **Daño Físico Puro y Escalado de *Late Game*:** A diferencia de los otros candidatos, Aphelios es un tirador (*ADC*) que escala extremadamente bien con objetos de crítico y penetración. En una composición full AP, el equipo enemigo probablemente priorizará ítems de **Resistencia Mágica** (como *Fuerza de la Naturaleza* o *Máscara Abisal*). Aphelios obligará al rival a dividir sus recursos defensivos entre Armadura y Resistencia Mágica, anulando la eficiencia de su *itemización*.
    > * **Versatilidad de Kit (Sinergia de Armas):**
    >   * **Calibrum (Rifle):** Te permite castigar a los enemigos desde una distancia segura mientras tus aliados AP inician.
    >   * **Severum (Pistola):** Te da *sustain* en peleas prolongadas.
    >   * **Gravitum (Cañón):** Ofrece el control de masas (*CC*) que un equipo AP suele carecer, facilitando que tus aliados lancen sus habilidades de área (aoe) sobre objetivos inmovilizados.
    > * **Eficiencia en Teamfights:** Un equipo full AP suele ser "de ráfaga" (*burst*). Aphelios aporta el **daño sostenido (DPS)** necesario para destruir tanques enemigos que hayan acumulado mucha vida, especialmente si usas **Infernum** (lanzallamas) para aplicar daño en área durante las peleas de equipo.
    >
    > **¿Por qué descartar las otras opciones?**
    > * **Alistar:** Aunque proporciona un gran *engage* y *peel* (protección), no soluciona tu carencia de daño físico. Añadir un Alistar a un equipo full AP solo hace que el equipo sea más resistente, pero incapaz de derribar torres o atravesar una composición con alta regeneración de vida o escudos.
    > * **Dr. Mundo:** Si bien es un coloso poderoso, su daño es mayoritariamente mágico (debido a su escalado con vida y la naturaleza de sus habilidades en el contexto actual). Añadir a Mundo no corrige el déficit de daño físico de tu composición; simplemente añadirías más *AP/Magic Damage* a la mezcla.
    >
    > **Recomendación Táctica para el cierre de partida:**
    > Si seleccionas a **Aphelios**, tu equipo debe jugar en torno a ti como el "seguro de vida". Dado que el enemigo se armará contra AP, tu **penetración de armadura** (ítems como *Recordatorio Mortal* o *Serylda*) será el factor determinante que les impedirá ganar las peleas de equipo en el *late game*.
    >
    > **Posicionamiento:** Mantente en la retaguardia. Tu equipo AP debe gastar sus *cooldowns* para obligar al enemigo a gastar sus defensas, y tú debes entrar una vez que las amenazas de *backline* enemigas hayan sido comprometidas por tus aliados.

### Pregunta 5: Adaptación contra amenazas específicas
* **Pregunta:** El equipo enemigo tiene un Zed fedeado y mucha capacidad de CC. ¿Debería cambiar mi build estándar para priorizar supervivencia o es mejor ajustar mi estilo de juego para no ser el objetivo principal en las teamfights?

    > **Respuesta del sistema:**
    >
    > Contra un **Zed** fedeado, la supervivencia no es una opción, es una **necesidad estratégica**. Si intentas mantener tu *build* estándar, Zed te eliminará en su rotación de habilidades (*burst*) antes de que puedas aportar tu daño al equipo.
    >
    > Aquí tienes el análisis para ajustar tu configuración y tu juego:
    >
    > **1. Ajuste de Build (Prioriza la Supervivencia Activa)**
    > No sacrifiques todo tu daño, pero integra elementos de **supervivencia defensiva** que anulen el daño explosivo de Zed:
    >
    > * **Reloj de Arena de Zhonya (Si usas AP) o Ángel Guardián (Si usas AD):** 
    >   * **Zhonya** es el *hard counter* definitivo contra la definitiva de Zed (**Marca de la Muerte**). Debes activarlo justo antes de que la marca explote para ignorar el daño acumulado.
    >   * **Ángel Guardián** te da una segunda oportunidad. Si Zed gasta todos sus recursos en matarte, su equipo quedará 4v5 mientras tú revives.
    > * **Encantamiento o Ítems de reducción de daño:** Si el enemigo tiene mucho **CC**, considera el **Crisol de Mikael** (si eres soporte) o simplemente asegúrate de tener **Botas de Mercurio**. La tenacidad es vital; si Zed te lanza su combo y logras sobrevivir con poca vida, el CC enemigo será lo que te termine de matar. Necesitas reducir ese tiempo de inmovilización para poder reposicionarte.
    > * **Faja de Mercurio (QSS):** Es obligatoria si el CC enemigo es de tipo supresión o *stun* encadenado. Si Zed te marca, y al mismo tiempo un CC enemigo te inmoviliza, el QSS es tu única vía de escape.
    >
    > **2. Ajuste de Estilo de Juego (El factor "Target Selection")**
    > Cambiar tu *build* es solo el 50% de la solución. El otro 50% es tu disciplina táctica:
    >
    > * **El "Fog of War" es tu mayor enemigo:** Un Zed fedeado no está en la pelea, está **esperando en la sombra**. Nunca te muestres en la línea si no ves a Zed en el mapa. Si no aparece, asume que está flanqueando tu posición.
    > * **Posicionamiento de "Segunda Línea":** No seas el primero en entrar. Deja que tu *tank* (ej. Alistar o un campeón con CC) inicie. Zed buscará al objetivo más frágil y vulnerable. Si te mantienes cerca de tus aliados que tienen CC de área, puedes forzar a Zed a cometer un error si intenta entrar agresivamente.
    > * **Control de Visión:** Compra un **Centinela de Control** y colócalo en los flancos, no solo en los arbustos de la línea. Zed necesita ángulos de entrada. Si le quitas la capacidad de sorprenderte, su efectividad cae un 60%.
    >
    > **Razonamiento Estratégico:**
    > * **¿Cambiar la build o el estilo?** **Ambos.** Si solo cambias la *build*, te faltará daño para ganar la pelea. Si solo cambias el estilo, Zed seguirá encontrando oportunidades de *pick-off* porque eres un objetivo prioritario.
    > * **Mentalidad de equipo:** Comunícate con tu equipo. Si tú eres el objetivo principal, diles: *"Guarden el CC para cuando Zed aparezca"*. Un Zed fedeado es un campeón de "todo o nada". Si fallan su combo o son interrumpidos por un CC justo después de entrar, se quedan totalmente expuestos y mueren al instante.
    >
    > **Conclusión:** Prioriza un objeto defensivo que ofrezca **invulnerabilidad temporal o revivificación**. En el *macrogame*, obliga a Zed a ser el que tenga que arriesgarse; no le regales la iniciación caminando solo por la jungla.