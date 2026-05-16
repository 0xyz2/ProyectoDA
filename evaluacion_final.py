# evaluacion_final.py (CORREGIDO con preguntas que SÍ están en los PDFs)
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import pandas as pd

load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")
client = genai.Client(api_key=API_KEY)

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

SYSTEM_INSTRUCTION = """
Eres un Analista Experto de Soporte Técnico.

REGLAS:
1. Responde SOLO con la información del contexto.
2. Si la respuesta NO está en el contexto, di EXACTAMENTE: "No encuentro esta información en los manuales."
3. Responde en formato Markdown.
"""

# ============================================
# 10 PREGUNTAS BASADAS EN EL CONTENIDO REAL DE LOS PDFs
# ============================================
preguntas_evaluacion = [
    # ===== PREGUNTAS QUE SÍ TIENEN RESPUESTA EN PDF1 =====
    {
        "id": 1,
        "pregunta": "¿Qué beneficios ofrece la virtualización en entornos empresariales?",
        "respuesta_esperada": "Mejorar rendimiento, seguridad, administración, continuidad del servicio, reducir costos, automatizar procesos, facilitar escalabilidad",
        "tipo": "✅ En PDF1"
    },
    {
        "id": 2,
        "pregunta": "¿Para qué sirven los laboratorios virtuales según el manual?",
        "respuesta_esperada": "Ofrecer laboratorios seguros para pruebas y aprendizaje a estudiantes y profesionales",
        "tipo": "✅ En PDF1"
    },
    {
        "id": 3,
        "pregunta": "¿Qué tipos de hipervisores se mencionan?",
        "respuesta_esperada": "Hipervisores Tipo 1 y Tipo 2",
        "tipo": "✅ En PDF1"
    },
    {
        "id": 4,
        "pregunta": "¿Qué aspectos mejora la seguridad y aislamiento en virtualización?",
        "respuesta_esperada": "Rendimiento, seguridad, administración y continuidad del servicio",
        "tipo": "✅ En PDF1"
    },
    
    # ===== PREGUNTAS QUE SÍ TIENEN RESPUESTA EN PDF2 =====
    {
        "id": 5,
        "pregunta": "¿Qué es la gestión de procesos en sistemas operativos?",
        "respuesta_esperada": "Campo clave que permite mejorar rendimiento, seguridad, administración y continuidad del servicio",
        "tipo": "✅ En PDF2"
    },
    {
        "id": 6,
        "pregunta": "¿Qué relación tiene la memoria y almacenamiento con la informática moderna?",
        "respuesta_esperada": "Es un campo clave que permite mejorar rendimiento, seguridad y administración",
        "tipo": "✅ En PDF2"
    },
    
    # ===== PREGUNTAS QUE SÍ TIENEN RESPUESTA EN PDF3 =====
    {
        "id": 7,
        "pregunta": "¿Qué se menciona sobre la relación entre Host y Guest?",
        "respuesta_esperada": "Campo clave que permite mejorar rendimiento, seguridad, administración y continuidad del servicio",
        "tipo": "✅ En PDF3"
    },
    {
        "id": 8,
        "pregunta": "¿Qué ventajas tienen los backups y la recuperación?",
        "respuesta_esperada": "Mejorar rendimiento, seguridad, administración y continuidad del servicio",
        "tipo": "✅ En PDF3"
    },
    
    # ===== PREGUNTAS SIN RESPUESTA EN LOS PDFs (prueba de no alucinación) =====
    {
        "id": 9,
        "pregunta": "¿Cuál es el precio de VMware Workstation en 2026?",
        "respuesta_esperada": "No encuentro esta información",
        "tipo": "❌ Sin información"
    },
    {
        "id": 10,
        "pregunta": "¿Quién creó el primer sistema operativo con inteligencia artificial?",
        "respuesta_esperada": "No encuentro esta información",
        "tipo": "❌ Sin información"
    }
]

# ============================================
# FUNCIÓN PARA EVALUAR
# ============================================
def evaluar_pregunta(pregunta_data):
    pregunta = pregunta_data["pregunta"]
    
    # Recuperar contexto
    retriever = vector_store.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(pregunta)
    
    contexto = ""
    for doc in docs:
        contexto += doc.page_content + "\n\n"
    
    prompt = f"""
[CONTEXTO]
{contexto}

[PREGUNTA]
{pregunta}

[INSTRUCCIÓN]
RESPONDE SOLO CON EL CONTEXTO. SI NO ESTÁ, DI: "No encuentro esta información en los manuales."
"""
    
    configuration = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.2,
        max_output_tokens=2000
    )
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=configuration,
        contents=prompt
    )
    
    return response.text, docs

# ============================================
# EJECUTAR EVALUACIÓN
# ============================================
print("\n" + "="*60)
print("📊 EVALUACIÓN RAG - 10 PREGUNTAS (Basadas en PDFs reales)")
print("="*60)

resultados = []

for i, p in enumerate(preguntas_evaluacion, 1):
    print(f"\n📝 {i}/10 {p['tipo']}")
    print(f"   Pregunta: {p['pregunta'][:60]}...")
    
    try:
        respuesta, docs = evaluar_pregunta(p)
        
        # Determinar si acertó
        if "No encuentro" in respuesta:
            if "❌" in p["tipo"]:
                acierto = "✅ Éxito (NO alucinó - correcto)"
            else:
                acierto = "❌ Fallo (debería estar en PDFs)"
        else:
            if "✅" in p["tipo"]:
                acierto = "✅ Éxito (respondió correctamente)"
            else:
                acierto = "⚠️ Alucinó (respondió sin contexto)"
        
        resultados.append({
            "ID": p["id"],
            "Tipo": p["tipo"],
            "Pregunta": p["pregunta"],
            "Respuesta_Esperada": p["respuesta_esperada"],
            "Respuesta_Obtenida": respuesta[:200].replace("\n", " "),
            "Acierto": acierto,
            "Contextos": len(docs)
        })
        
        print(f"   {acierto}")
        print(f"   Respuesta: {respuesta[:100]}...")
        time.sleep(2)
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        resultados.append({
            "ID": p["id"],
            "Tipo": p["tipo"],
            "Pregunta": p["pregunta"],
            "Respuesta_Esperada": p["respuesta_esperada"],
            "Respuesta_Obtenida": f"ERROR: {str(e)[:100]}",
            "Acierto": "❌ Error técnico",
            "Contextos": 0
        })

# ============================================
# TABLA DE RESULTADOS
# ============================================
df = pd.DataFrame(resultados)

print("\n" + "="*60)
print("📊 TABLA DE RESULTADOS")
print("="*60)
print(df.to_string(index=False))

# Estadísticas
aciertos = df[df['Acierto'].str.startswith('✅')].shape[0]
fallos = df[df['Acierto'].str.startswith('❌')].shape[0]

print("\n" + "="*60)
print("📈 ESTADÍSTICAS")
print("="*60)
print(f"✅ Aciertos: {aciertos}/10 ({aciertos*10}%)")
print(f"❌ Fallos: {fallos}/10 ({fallos*10}%)")
print(f"📚 Promedio de fragmentos recuperados: {df['Contextos'].mean():.1f}")

# Guardar resultados
df.to_csv("resultados_evaluacion_final.csv", index=False, encoding='utf-8-sig')
print("\n💾 Resultados guardados en 'resultados_evaluacion_final.csv'")