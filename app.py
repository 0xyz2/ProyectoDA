import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Usar embeddings locales en lugar de los de Google
from langchain_community.embeddings import HuggingFaceEmbeddings

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)
historial = []

# Carpeta con tus PDFs
CARPETA_PDFS = "pdfs_soporte"

# ----------------------------
# CREAR BASE VECTORIAL CON EMBEDDINGS LOCALES
# ----------------------------
def crear_base_vectorial():
    """Carga tus PDFs y crea la base de datos con embeddings locales"""
    documentos = []
    
    print("📂 Leyendo tus PDFs...")
    for archivo in os.listdir(CARPETA_PDFS):
        if archivo.endswith('.pdf'):
            ruta = os.path.join(CARPETA_PDFS, archivo)
            print(f"   Cargando: {archivo}")
            loader = PyPDFLoader(ruta)
            documentos.extend(loader.load())
    
    print(f"📄 Total páginas: {len(documentos)}")
    
    # Dividir en fragmentos
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(documentos)
    print(f"✂️ Fragmentos creados: {len(chunks)}")
    
    # ✅ USAR EMBEDDINGS LOCALES (GRATIS, SIN LÍMITES)
    print("🔄 Generando embeddings locales (sin usar API)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    # Crear base vectorial
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory="./chroma_db",
        collection_name="soporte"
    )
    
    print(f"✅ Base creada con {vector_store._collection.count()} fragmentos")
    return vector_store

# ----------------------------
# BUSCAR EN TUS PDFS
# ----------------------------
def buscar_contexto(vector_store, pregunta):
    """Busca información relevante en tus PDFs"""
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(pregunta)
    
    contexto = ""
    for i, doc in enumerate(docs, 1):
        fuente = doc.metadata.get('source', 'desconocido')
        contexto += f"[Fuente: {fuente}]\n{doc.page_content}\n\n---\n\n"
    
    return contexto

# ----------------------------
# SYSTEM PROMPT
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
# RESPONDER CON RAG
# ----------------------------
vector_store = None

def responder_soporte(mensaje_usuario: str) -> str:
    global vector_store, historial
    
    # Buscar en tus PDFs
    contexto = ""
    if vector_store:
        contexto = buscar_contexto(vector_store, mensaje_usuario)
        if contexto:
            print(f"📚 Encontré información en los PDFs")
    
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
    
    historial.append({"role": "user", "parts": [{"text": mensaje_final}]})
    
    configuration = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.4,
        max_output_tokens=2000
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=configuration,
        contents=historial
    )
    
    respuesta = response.text
    historial.append({"role": "model", "parts": [{"text": respuesta}]})
    
    return respuesta

# ----------------------------
# INICIAR
# ----------------------------
print("="*50)
print("🚀 ASISTENTE RAG - AVANCE 2")
print("="*50)

# Crear la base con tus PDFs
if os.path.exists(CARPETA_PDFS):
    # Eliminar base anterior si existe para evitar conflictos
    if os.path.exists("./chroma_db"):
        import shutil
        shutil.rmtree("./chroma_db")
        print("🗑️ Base anterior eliminada")
    
    vector_store = crear_base_vectorial()
    print("\n✅ ¡Listo! Puedes hacer preguntas sobre tus PDFs\n")
else:
    print(f"\n❌ ERROR: No encuentro la carpeta '{CARPETA_PDFS}'")
    print("   Crea esa carpeta y pon tus 3 PDFs allí\n")
    exit()

# Chat
print("🤖 Asistente de Soporte Técnico (con RAG local)")
print("   Pregúntame sobre lo que contienen tus manuales")
print("   Escribe 'salir' para terminar\n")

while True:
    mensaje = input("💬 Tú: ")
    if mensaje.lower() == "salir":
        print("✅ Hasta luego")
        break
    
    try:
        respuesta = responder_soporte(mensaje)
        print("\n🧠 Asistente:\n")
        print(respuesta)
        print("\n" + "-"*50 + "\n")
    except Exception as e:
        print(f"❌ Error: {e}")
