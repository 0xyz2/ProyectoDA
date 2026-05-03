¡Perfecto! Aquí tienes el **README completo** con la sección del **Avance 2** bien explicada, integrada con tu README anterior.

---

## 📄 **README.md completo (copia y pega todo esto):**

```markdown
# 🤖 Asistente Experto de Soporte Técnico con RAG

## 📌 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Asistente Experto basado en RAG (Retrieval-Augmented Generation)** y técnicas de Prompt Engineering, orientado al análisis y solución de problemas de **soporte técnico en entornos informáticos**.

El sistema es capaz de:
- **Leer documentos técnicos** (manuales, guías, instructivos) de forma local
- **Responder preguntas** basándose en el contenido de esos documentos
- **Diagnosticar fallos** y proponer soluciones estructuradas
- **Preservar la privacidad** de los datos al usar embeddings locales

Este desarrollo corresponde al **Avance 1 y Avance 2 del proyecto académico: Desarrollo de un Asistente Experto basado en RAG y Agentes**.

---

## 🎯 Objetivos

### Avance 1 - Prompt Engineering:
- Diseñar un asistente inteligente especializado en soporte técnico
- Aplicar técnicas de **System Prompt** para definir el comportamiento del modelo
- Implementar **Few-Shot Prompting** para guiar el formato de las respuestas
- Utilizar historial conversacional para simular interacción contextual

### Avance 2 - Implementación RAG:
- Crear un flujo RAG completo y funcional
- Seleccionar y cargar documentos PDF para vectorizar
- Dividir documentos en fragmentos (chunks) óptimos
- Generar embeddings de forma local (sin API externa)
- Crear una base de datos vectorial con ChromaDB
- Implementar mecanismo de recuperación de contexto para las consultas

---

## 🧠 Tecnologías Utilizadas

| Componente | Tecnología |
|------------|------------|
| **LLM** | Google Gemini 2.5 Flash (vía API) |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) - **Local** |
| **Vector Store** | ChromaDB |
| **Framework RAG** | LangChain |
| **Carga de PDFs** | PyPDFLoader |
| **Lenguaje** | Python 3.14+ |
| **Entorno** | Virtual env (venv) |

---

## ⚙️ Funcionamiento del Sistema

### Arquitectura RAG implementada:

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO RAG DEL SISTEMA                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  📁 PDFs Técnicos                                            │
│       ↓                                                       │
│  ✂️ División en fragmentos (chunk_size=1000)                 │
│       ↓                                                       │
│  🔢 Embeddings locales (all-MiniLM-L6-v2)                    │
│       ↓                                                       │
│  🗄️ Almacenamiento en ChromaDB (102 fragmentos)              │
│       ↓                                                       │
│  ❓ Pregunta del usuario                                      │
│       ↓                                                       │
│  🔍 Búsqueda por similitud (k=3 fragmentos)                  │
│       ↓                                                       │
│  📝 Prompt aumentado = Contexto + Pregunta                   │
│       ↓                                                       │
│  🤖 Gemini genera respuesta fundamentada                     │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Estructura de cada respuesta:

El asistente responde siempre con el siguiente formato en Markdown:

```markdown
### 🔎 Diagnóstico probable
(explicación técnica breve basada en los manuales)

### 🛠️ Pasos de solución
(lista numerada paso a paso)

### 💡 Recomendación preventiva
(consejo para evitar el error en el futuro)
```

---

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone LINK_DEL_REPOSITORIO
cd NOMBRE_DEL_PROYECTO
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv env
```

### 3️⃣ Activar entorno virtual

**Windows:**
```bash
env\Scripts\activate
```

**Mac/Linux:**
```bash
source env/bin/activate
```

### 4️⃣ Instalar dependencias

```bash
pip install google-genai python-dotenv langchain langchain-community langchain-chroma chromadb pypdf sentence-transformers
```

### 5️⃣ Configurar variable de entorno

Crear un archivo `.env` en la raíz del proyecto:

```
GENAI_API_KEY=tu_api_key_aqui
```

> ⚠️ **Obtener API Key:** https://aistudio.google.com/apikey

### 6️⃣ Preparar los documentos PDF

Crear una carpeta llamada `pdfs_soporte` en la raíz del proyecto y colocar allí los manuales técnicos (formato PDF).

```
📂 Proyecto/
├── 📄 app.py
├── 📂 pdfs_soporte/     ← Tus PDFs aquí
│   ├── manual1.pdf
│   ├── manual2.pdf
│   └── manual3.pdf
├── 📄 .env
└── 📄 README.md
```

### 7️⃣ Ejecutar el asistente

```bash
python app.py
```

---

## 💬 Ejemplos de uso

### Ejemplo 1: Pregunta con información en los manuales

**Usuario:**
> ¿Qué es una máquina virtual y cuál es su función principal?

**Asistente:**
> ### 🔎 Diagnóstico probable
> Los manuales describen las aplicaciones y beneficios de la virtualización...
>
> ### 🛠️ Pasos de solución
> La función principal de las máquinas virtuales es mejorar el rendimiento, la seguridad y la administración...
>
> ### 💡 Recomendación preventiva
> Para una comprensión más profunda, consultar manuales específicos...

### Ejemplo 2: Pregunta SIN información en los manuales

**Usuario:**
> ¿Cuál es la diferencia entre un hipervisor tipo 1 y tipo 2?

**Asistente:**
> ### 🔎 Diagnóstico probable
> La información específica sobre la diferencia entre hipervisor Tipo 1 y Tipo 2 no se encuentra en los fragmentos de texto suministrados.
>
> ### 🛠️ Pasos de solución
> La información solicitada no está disponible en los manuales técnicos proporcionados.
>
> ### 💡 Recomendación preventiva
> Sería necesario consultar documentación adicional que profundice en la arquitectura de cada tipo de hipervisor.

---

## 📊 Avance 2: Detalle Técnico del Pipeline RAG

### 1. Selección y Carga de Documentos
- **Formato soportado:** PDF
- **Ubicación:** Carpeta `pdfs_soporte/`
- **Loader utilizado:** `PyPDFLoader` de LangChain
- **Documentos procesados:** 3 manuales técnicos (30 páginas totales)

### 2. División en Fragmentos (Chunking)
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Caracteres por fragmento
    chunk_overlap=100,    # Solapamiento entre fragmentos
    separators=["\n\n", "\n", ".", " "]
)
```
- **Fragmentos generados:** 102
- **Estrategia:** División recursiva priorizando párrafos y oraciones completas

### 3. Vectorización (Embeddings)
- **Modelo utilizado:** `sentence-transformers/all-MiniLM-L6-v2`
- **Ejecución:** **Totalmente local** (no consume API ni tiene límites de cuota)
- **Dimensión del vector:** 384 dimensiones
- **Ventaja:** Preserva la privacidad de los datos

### 4. Base de Datos Vectorial
- **Tecnología:** ChromaDB
- **Almacenamiento persistente:** Carpeta `chroma_db/`
- **Métrica de similitud:** Coseno (`cosine`)
- **Colección:** `soporte`

### 5. Mecanismo de Recuperación (Retrieval)
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 3})
```
- **Número de fragmentos recuperados:** 3 por consulta
- **Métrica:** Similitud coseno
- **Salida:** Fragmentos más relevantes + metadatos (fuente, página)

### 6. Prompt Aumentado
```python
mensaje_final = f"""
[INFORMACIÓN DE TUS MANUALES]
{contexto}

[PREGUNTA DEL USUARIO]
{pregunta}

RESPONDE USANDO SOLO LA INFORMACIÓN DE LOS MANUALES TÉCNICOS.
"""
```

### 7. Generación de Respuesta
- **Modelo LLM:** Gemini 2.5 Flash
- **Temperature:** 0.4 (respuestas precisas y determinísticas)
- **Máximo de tokens:** 2000

---

## 📁 Estructura del Proyecto

```
asistente-soporte-tecnico/
│
├── app.py                          # Código principal del asistente
├── requirements.txt                # Dependencias del proyecto
├── .env                            # Variables de entorno (API Key)
├── README.md                       # Documentación
│
├── 📂 pdfs_soporte/                # Carpeta con los manuales PDF
│   ├── pdf1.pdf
│   ├── pdf2.pdf
│   └── pdf3.pdf
│
├── 📂 chroma_db/                   # Base vectorial (se genera automáticamente)
│   └── (archivos de ChromaDB)
│
└── 📂 env/                         # Entorno virtual
```

---

## 📚 Conceptos Técnicos Aplicados

| Concepto | Aplicación |
|----------|------------|
| **RAG (Retrieval-Augmented Generation)** | Pipeline completo de recuperación + generación |
| **Chunking** | División óptima de documentos para embeddings |
| **Embeddings locales** | Modelo sentence-transformers sin API externa |
| **Vector Store** | ChromaDB para búsqueda semántica |
| **Prompt Engineering** | System Prompt, Few-Shot, delimitadores |
| **LangChain** | Framework para orquestar el flujo RAG |

---

## 🔒 Privacidad y Seguridad

- ✅ **Embeddings locales:** Los documentos nunca salen de tu máquina
- ✅ **Sin dependencia de API externa para vectorización**
- ✅ **Base vectorial persistente en disco**
- ✅ **Solo el LLM (Gemini) consume API, no tus documentos**

---

## 🐛 Solución de Problemas Comunes

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError` | Ejecutar `pip install -r requirements.txt` |
| `429 RESOURCE_EXHAUSTED` | Usar embeddings locales (ya implementado) |
| `No se encontró la carpeta pdfs_soporte` | Crear la carpeta manualmente |
| `API Key no válida` | Verificar el archivo `.env` |

---

## 👩‍💻 Autoras

**Catalina Gordillo** - Estudiante de Ingeniería de Sistemas  
**Sara Murcia** - Estudiante de Ingeniería de Sistemas

---

## 📅 Estado del Proyecto

| Avance | Estado | Fecha |
|--------|--------|-------|
| Avance 1 - Prompt Engineering | ✅ Completado | - |
| Avance 2 - Implementación RAG | ✅ Completado | - |
| Avance 3 - Agentes | ⏳ Pendiente | - |

---

**Proyecto académico – Desarrollo de aplicaciones con IA**
```


