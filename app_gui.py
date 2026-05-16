# app_gradio.py
import gradio as gr
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
PERSIST_DIR = "./chroma_db"

print("📂 Cargando base vectorial...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': True}
)

vector_store = Chroma(
    persist_directory=PERSIST_DIR,
    embedding_function=embeddings,
    collection_name="soporte"
)
print(f"✅ Base cargada con {vector_store._collection.count()} fragmentos")

# ----------------------------
# SYSTEM PROMPT (EL MISMO QUE FUNCIONA)
# ----------------------------
SYSTEM_INSTRUCTION = """
Eres un Analista Experto de Soporte Técnico especializado en:
- Sistemas operativos Linux y Windows
- Redes básicas
- Virtualización
- Configuración de software

REGLAS:
1. Responde en formato Markdown con esta estructura:
   ### 🔎 Diagnóstico probable
   ### 🛠️ Pasos de solución
   ### 💡 Recomendación preventiva
2. Usa la información de los manuales como fuente principal.
3. Si no encuentras la respuesta en los manuales, dilo claramente.
"""

# ----------------------------
# FUNCIÓN PARA BUSCAR CONTEXTO
# ----------------------------
def buscar_contexto(pregunta):
    """Busca información relevante en los PDFs"""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(pregunta)
    
    contexto = ""
    fuentes = []
    for i, doc in enumerate(docs, 1):
        fuente = doc.metadata.get('source', 'desconocido').split('/')[-1]
        pagina = doc.metadata.get('page', '?')
        fuentes.append(f"**Fuente {i}:** {fuente} (Pág. {pagina})")
        contexto += f"[Fuente: {fuente}]\n{doc.page_content}\n\n---\n\n"
    
    return contexto, fuentes

# ----------------------------
# FUNCIÓN PARA RESPONDER
# ----------------------------
def responder_soporte(mensaje_usuario, historial):
    """Genera respuesta usando RAG - MISMA LÓGICA QUE FUNCIONA"""
    
    # Buscar en los PDFs
    contexto, fuentes = buscar_contexto(mensaje_usuario)
    
    # Armar mensaje con contexto
    if contexto:
        mensaje_final = f"""
[INFORMACIÓN DE TUS MANUALES]
{contexto}

[PREGUNTA DEL USUARIO]
{mensaje_usuario}

RESPONDE USANDO SOLO LA INFORMACIÓN DE LOS MANUALES TÉCNICOS.
SI LA RESPUESTA NO ESTÁ EN LOS MANUALES, INDÍCALO CLARAMENTE.
"""
    else:
        mensaje_final = mensaje_usuario
    
    # Actualizar historial
    historial.append({"role": "user", "parts": [{"text": mensaje_final}]})
    
    # Configuración
    configuration = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.4,
        max_output_tokens=2000
    )
    
    # Generar respuesta
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=configuration,
        contents=historial
    )
    
    respuesta = response.text
    
    # Agregar fuentes
    if fuentes:
        respuesta += "\n\n---\n### 📚 Fuentes consultadas\n" + "\n".join(fuentes)
    
    # Actualizar historial con la respuesta
    historial.append({"role": "model", "parts": [{"text": respuesta}]})
    
    return respuesta, historial

# ----------------------------
# FUNCIÓN PARA EL CHAT
# ----------------------------
def chat_response(message, history):
    """Procesa el mensaje y devuelve la respuesta"""
    if not message:
        return "", history
    
    # Convertir historial de Gradio al formato que usa tu backend
    historial_backend = []
    for h in history:
        if h.get('role') == 'user':
            historial_backend.append({"role": "user", "parts": [{"text": h.get('content', '')}]})
        elif h.get('role') == 'assistant':
            historial_backend.append({"role": "model", "parts": [{"text": h.get('content', '')}]})
    
    # Obtener respuesta
    respuesta, nuevo_historial = responder_soporte(message, historial_backend)
    
    # Actualizar historial de Gradio
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": respuesta})
    
    return "", history

# ----------------------------
# INTERFAZ GRADIO (SIN 'type' para compatibilidad)
# ----------------------------
with gr.Blocks(title="Asistente de Soporte Técnico") as demo:
    gr.Markdown("""
    # 🤖 Asistente Experto de Soporte Técnico
    
    **Sistema RAG con búsqueda semántica en manuales técnicos**
    """)
    
    gr.Markdown("---")
    
    # Chatbot (sin parámetro 'type')
    chatbot = gr.Chatbot(label="Chat", height=500)
    
    with gr.Row():
        msg = gr.Textbox(
            label="Escribe tu pregunta",
            placeholder="Ej: ¿Qué modos de red existen en VMware?",
            scale=4,
            lines=2
        )
        submit = gr.Button("📤 Enviar", variant="primary", scale=1)
    
    with gr.Row():
        clear = gr.Button("🗑️ Limpiar chat")
    
    gr.Markdown("---")
    gr.Markdown("### 📋 Preguntas sugeridas")
    
    preguntas = [
        "¿Qué comandos de Linux se mencionan para diagnóstico de red?",
        "¿Qué modos de red existen en VMware?",
        "¿Qué función cumple un hipervisor en una máquina virtual?",
        "¿Cómo puedo verificar las direcciones IP en Linux?",
        "¿Qué hacer si una máquina virtual no tiene conexión a internet?",
        "¿Por qué la virtualización ayuda a optimizar recursos tecnológicos en una empresa?",
        "¿Cuál es el precio oficial de VMware Workstation en 2026?"
    ]
    
    # Botones en filas de 3
    for i in range(0, len(preguntas), 3):
        with gr.Row():
            for j in range(3):
                if i + j < len(preguntas):
                    btn = gr.Button(preguntas[i + j], size="sm")
                    btn.click(fn=lambda x=preguntas[i+j]: x, outputs=msg)
    
    gr.Markdown("---")
    gr.Markdown("### ⚙️ Parámetros del Sistema")
    gr.Markdown("""
    | Parámetro | Valor |
    |-----------|-------|
    | **Embeddings** | all-MiniLM-L6-v2 (local) |
    | **chunk_size** | 1000 |
    | **overlap** | 100 |
    | **k (chunks recuperados)** | 3 |
    | **LLM** | Gemini 2.5 Flash |
    | **Base vectorial** | ChromaDB |
    """)
    
    # Conectar funciones
    submit.click(chat_response, [msg, chatbot], [msg, chatbot])
    msg.submit(chat_response, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ([], ""), None, [chatbot, msg])

# ----------------------------
# EJECUTAR
# ----------------------------
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 INICIANDO ASISTENTE CON GRADIO")
    print("="*50)
    print("📌 Abre en tu navegador: http://localhost:7860")
    print("📌 Presiona Ctrl+C para detener")
    print("="*50 + "\n")
    
    demo.launch()