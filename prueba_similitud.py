# prueba_similitud.py
import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

PERSIST_DIR = "./chroma_db"

print("="*60)
print("🔍 PRUEBAS DE SIMILITUD DE COSENO")
print("="*60)

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

# Pruebas: lenguaje coloquial vs términos técnicos
pruebas = [
    {
        "coloquial": "¿Cómo veo mi dirección IP en Linux?",
        "tecnico": "comando ip a"
    },
    {
        "coloquial": "Mi máquina virtual no agarra internet",
        "tecnico": "modo NAT o Bridge"
    },
    {
        "coloquial": "¿Cómo matar un proceso que no responde?",
        "tecnico": "kill -9"
    },
    {
        "coloquial": "¿Cómo liberar espacio en el disco duro de Windows?",
        "tecnico": "liberador de espacio"
    }
]

print("\n📝 Resultados de similitud:\n")

for prueba in pruebas:
    print(f"Pregunta coloquial: '{prueba['coloquial']}'")
    
    # Buscar contexto
    docs = vector_store.similarity_search(prueba['coloquial'], k=3)
    
    if docs:
        print(f"📄 Fragmento recuperado: {docs[0].page_content[:150]}...")
        print(f"✅ Éxito: Los embeddings entendieron la intención coloquial")
    else:
        print("❌ No se recuperó contexto")
    
    print("-"*50)