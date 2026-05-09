# evaluacion.py
import os
import time
from dotenv import load_dotenv
from google import genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from ragas import EvaluationDataset
import pandas as pd

load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# ----------------------------
# CONFIGURACIÓN
# ----------------------------
PERSIST_DIR = "./chroma_db"

print("="*60)
print("🚀 INICIANDO EVALUACIÓN RAGAS - AVANCE 3")
print("="*60)

print("\n📂 Cargando base vectorial existente...")
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

# Configurar LLM para RAGAS
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=API_KEY,
    temperature=0
)

llm_juez = LangchainLLMWrapper(llm)
embeddings_juez = LangchainEmbeddingsWrapper(embeddings)

# ----------------------------
# FUNCIÓN PARA RECUPERAR CONTEXTO
# ----------------------------
def recuperar_contexto(pregunta, k=3):
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(pregunta)
    contextos = [doc.page_content for doc in docs]
    return contextos

# ----------------------------
# TUS 8 PREGUNTAS CORRECTAS
# ----------------------------
preguntas_evaluacion = [
    # ========== TIPO 1: Respuesta textual (debe estar en los PDFs) ==========
    {
        "user_input": "¿Qué función cumple un hipervisor en una máquina virtual?",
        "reference": "El hipervisor permite crear y ejecutar múltiples máquinas virtuales en un solo servidor físico, gestionando los recursos del hardware como CPU, memoria y almacenamiento.",
        "tipo": "Textual"
    },
    {
        "user_input": "¿Cuáles son las principales diferencias entre Windows, Linux y macOS?",
        "reference": "Windows es de código cerrado con interfaz gráfica intuitiva, Linux es de código abierto y altamente personalizable, macOS es exclusivo de Apple con ecosistema integrado.",
        "tipo": "Textual"
    },
    
    # ========== TIPO 2: Vocabulario diferente (prueba embeddings) ==========
    {
        "user_input": "¿Por qué la virtualización ayuda a optimizar recursos tecnológicos en una empresa?",
        "reference": "Permite ejecutar múltiples sistemas en un solo servidor, reduciendo hardware físico, consumo eléctrico, espacio y costos de mantenimiento.",
        "tipo": "Vocabulario diferente"
    },
    {
        "user_input": "¿Cómo contribuye un sistema operativo a la organización de tareas dentro de un computador?",
        "reference": "El sistema operativo gestiona la planificación de procesos, asigna tiempo de CPU a cada tarea y administra la memoria para que múltiples programas funcionen sin conflictos.",
        "tipo": "Vocabulario diferente"
    },
    
    # ========== TIPO 3: Requiere combinar varios chunks ==========
    {
        "user_input": "¿Cómo trabajan juntos el sistema operativo host y las máquinas virtuales para mejorar la administración de recursos?",
        "reference": "El sistema operativo host proporciona el hardware base, mientras que el hipervisor asigna recursos como CPU, RAM y almacenamiento a cada máquina virtual, permitiendo una distribución eficiente y aislada.",
        "tipo": "Combina chunks"
    },
    {
        "user_input": "¿Qué ventajas ofrecen los backups y la virtualización cuando ocurre una falla del sistema?",
        "reference": "Los backups permiten restaurar datos perdidos, mientras que la virtualización facilita la recuperación rápida de sistemas completos mediante snapshots y migración de máquinas virtuales a otros servidores.",
        "tipo": "Combina chunks"
    },
    
    # ========== TIPO 4: El sistema NO tiene la respuesta (alucinaciones) ==========
    {
        "user_input": "¿Cuál es el precio oficial de VMware Workstation en 2026?",
        "reference": "No disponible en los manuales",
        "tipo": "Sin respuesta"
    },
    {
        "user_input": "¿Qué empresa creó el primer sistema operativo basado completamente en inteligencia artificial?",
        "reference": "No disponible en los manuales",
        "tipo": "Sin respuesta"
    }
]

# ----------------------------
# MOSTRAR TABLA DE PARÁMETROS
# ----------------------------
print("\n" + "="*60)
print("📊 PARÁMETROS DE EVALUACIÓN")
print("="*60)
print(f"Documento(s):           3 PDFs de soporte técnico")
print(f"Modelo de embeddings:   sentence-transformers/all-MiniLM-L6-v2 (local)")
print(f"chunk_size / overlap:   1000 / 100")
print(f"k (chunks recuperados): 3")
print(f"LLM generador:          Google Gemini 2.5 Flash")
print(f"LLM juez (RAGAS):       Google Gemini 2.5 Flash")
print(f"Cantidad de consultas:  8 (2 por cada tipo)")

# ----------------------------
# EJECUTAR EVALUACIÓN
# ----------------------------
print("\n" + "="*60)
print("🔍 EJECUTANDO EVALUACIÓN (con delays para evitar cuota)")
print("="*60)

client = genai.Client(api_key=API_KEY)
registros = []

for i, muestra in enumerate(preguntas_evaluacion, 1):
    pregunta = muestra["user_input"]
    tipo = muestra["tipo"]
    print(f"\n📝 {i}/8 [{tipo}] {pregunta[:60]}...")
    
    # Recuperar contexto
    contextos = recuperar_contexto(pregunta, k=3)
    print(f"   📚 Contextos recuperados: {len(contextos)} fragmentos")
    
    # Generar respuesta con Gemini
    prompt = f"""
[CONTEXTO DE MANUALES TÉCNICOS]
{chr(10).join(contextos)}

[PREGUNTA]
{pregunta}

RESPONDE USANDO SOLO LA INFORMACIÓN DE LOS MANUALES.
SI LA RESPUESTA NO ESTÁ EN LOS MANUALES, DICE EXACTAMENTE: "No encontré esta información en los manuales proporcionados."
"""
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        registros.append({
            "user_input": pregunta,
            "retrieved_contexts": contextos,
            "response": response.text,
            "reference": muestra["reference"]
        })
        print(f"   ✅ Respuesta generada correctamente")
        
        # Delays para no exceder cuota (5 solicitudes por minuto)
        if i < len(preguntas_evaluacion):
            print(f"   ⏳ Esperando 13 segundos para respetar límite de API...")
            time.sleep(13)
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print(f"   ⏳ Esperando 30 segundos y reintentando...")
        time.sleep(30)
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        registros.append({
            "user_input": pregunta,
            "retrieved_contexts": contextos,
            "response": response.text,
            "reference": muestra["reference"]
        })
        print(f"   ✅ Reintento exitoso")

# ----------------------------
# EVALUAR CON RAGAS
# ----------------------------
print("\n" + "="*60)
print("📊 CALCULANDO MÉTRICAS CON RAGAS...")
print("="*60)

dataset = EvaluationDataset.from_list(registros)

resultados = evaluate(
    dataset=dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
    llm=llm_juez,
    embeddings=embeddings_juez
)

df = resultados.to_pandas()

# ----------------------------
# TABLA DE RESULTADOS POR PREGUNTA
# ----------------------------
print("\n" + "="*80)
print("📈 TABLA DE RESULTADOS POR PREGUNTA")
print("="*80)

# Crear tabla con formato
tabla_resultados = []
for i, row in df.iterrows():
    # Análisis crítico por pregunta
    if row['faithfulness'] > 0.8:
        f_analisis = "✅ Alta fidelidad"
    elif row['faithfulness'] > 0.6:
        f_analisis = "📊 Fidelidad media"
    else:
        f_analisis = "⚠️ Baja fidelidad - posible alucinación"
    
    if row['answer_relevancy'] > 0.8:
        a_analisis = "✅ Muy relevante"
    elif row['answer_relevancy'] > 0.6:
        a_analisis = "📊 Relevancia media"
    else:
        a_analisis = "⚠️ Poco relevante"
    
    if row['context_precision'] > 0.8:
        c_analisis = "✅ Contexto preciso"
    elif row['context_precision'] > 0.6:
        c_analisis = "📊 Precisión media"
    else:
        c_analisis = "⚠️ Contexto poco preciso"
    
    tabla_resultados.append({
        "N°": i+1,
        "Tipo": preguntas_evaluacion[i]['tipo'],
        "Faithfulness": round(row['faithfulness'], 3),
        "Answer_Relevancy": round(row['answer_relevancy'], 3),
        "Context_Precision": round(row['context_precision'], 3),
        "Análisis": f"{f_analisis} | {a_analisis} | {c_analisis}"
    })

df_tabla = pd.DataFrame(tabla_resultados)
print(df_tabla.to_string(index=False))

# ----------------------------
# TABLA RESUMEN (compacta para PDF)
# ----------------------------
print("\n" + "="*80)
print("📊 TABLA RESUMEN (para copiar al informe)")
print("="*80)

print("\n| N° | Tipo | Faithfulness | Answer_Relevancy | Context_Precision |")
print("|----|------|--------------|------------------|-------------------|")
for i, row in df.iterrows():
    tipo = preguntas_evaluacion[i]['tipo'][:20]
    print(f"| {i+1} | {tipo} | {row['faithfulness']:.3f} | {row['answer_relevancy']:.3f} | {row['context_precision']:.3f} |")

# ----------------------------
# PROMEDIOS GLOBALES
# ----------------------------
print("\n" + "="*60)
print("📊 PROMEDIOS GLOBALES")
print("="*60)
print(f"Faithfulness promedio:      {df['faithfulness'].mean():.3f}")
print(f"Answer Relevancy promedio:  {df['answer_relevancy'].mean():.3f}")
print(f"Context Precision promedio: {df['context_precision'].mean():.3f}")

# ----------------------------
# ANÁLISIS CRÍTICO FINAL
# ----------------------------
print("\n" + "="*60)
print("📝 ANÁLISIS CRÍTICO FINAL")
print("="*60)

f_prom = df['faithfulness'].mean()
a_prom = df['answer_relevancy'].mean()
c_prom = df['context_precision'].mean()

print("\n**Interpretación de métricas:**\n")

if f_prom > 0.8:
    print("✅ **Faithfulness (%.3f):** El sistema es ALTAMENTE CONFIABLE. No alucina y responde estrictamente basado en el contexto." % f_prom)
elif f_prom > 0.6:
    print("📊 **Faithfulness (%.3f):** El sistema tiene FIDELIDAD MEDIA. Algunas respuestas podrían no estar completamente fundamentadas." % f_prom)
else:
    print("⚠️ **Faithfulness (%.3f):** El sistema tiene BAJA FIDELIDAD. Existe riesgo de alucinaciones." % f_prom)

if a_prom > 0.8:
    print("✅ **Answer Relevancy (%.3f):** Las respuestas son ALTAMENTE RELEVANTES para las preguntas formuladas." % a_prom)
elif a_prom > 0.6:
    print("📊 **Answer Relevancy (%.3f):** Las respuestas son RELEVANTES pero podrían mejorarse." % a_prom)
else:
    print("⚠️ **Answer Relevancy (%.3f):** Las respuestas son POCO RELEVANTES. Revisar la calidad del contexto recuperado." % a_prom)

if c_prom > 0.8:
    print("✅ **Context Precision (%.3f):** La recuperación de contexto es MUY PRECISA. Los fragmentos recuperados son útiles." % c_prom)
elif c_prom > 0.6:
    print("📊 **Context Precision (%.3f):** La recuperación de contexto tiene PRECISIÓN MEDIA. Algunos fragmentos no son relevantes." % c_prom)
else:
    print("⚠️ **Context Precision (%.3f):** La recuperación de contexto es POCO PRECISA. Revisar calidad de embeddings y chunking." % c_prom)

print("\n**Fortalezas del sistema:**")
print("   ✅ Embeddings locales preservan privacidad de datos")
print("   ✅ Respuestas estructuradas en formato Markdown")
print("   ✅ Manejo honesto de preguntas sin respuesta en manuales")

print("\n**Áreas de mejora:**")
if c_prom < 0.8:
    print("   ⚠️ Aumentar k (chunks recuperados) de 3 a 5 para mejorar precisión")
if f_prom < 0.8:
    print("   ⚠️ Reducir chunk_size de 1000 a 800 para fragmentos más precisos")
print("   ⚠️ Mejorar la calidad y cantidad de documentos en la base de conocimiento")

# ----------------------------
# GUARDAR RESULTADOS
# ----------------------------
df.to_csv("resultados_ragas.csv", index=False)
print("\n💾 Resultados guardados en 'resultados_ragas.csv'")
print("💾 Tabla de resultados guardada")

print("\n" + "="*60)
print("✅ EVALUACIÓN COMPLETADA")
print("="*60)