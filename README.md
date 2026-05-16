# 🤖 Asistente Experto de Soporte Técnico con RAG

## 📌 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Asistente Experto basado en RAG (Retrieval-Augmented Generation)** y técnicas de Prompt Engineering, orientado al análisis y solución de problemas de **soporte técnico en entornos informáticos**.

El sistema es capaz de:
- **Leer documentos técnicos** (manuales, guías, instructivos) de forma local
- **Responder preguntas** basándose en el contenido de esos documentos
- **Diagnosticar fallos** y proponer soluciones estructuradas
- **Preservar la privacidad** de los datos al usar embeddings locales
- **Interfaz gráfica amigable** para facilitar la interacción

Este desarrollo corresponde al **Avance 1, 2, 3 y 4 del proyecto académico: Desarrollo de un Asistente Experto basado en RAG y Agentes**.

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

### Avance 3 - Evaluación RAGAS:
- Evaluar el desempeño del pipeline RAG usando RAGAS
- Medir métricas de fidelidad, relevancia y precisión contextual
- Analizar resultados y proponer mejoras

### Avance 4 - GUI y Evaluación Final:
- Implementar interfaz gráfica con Gradio
- Realizar pruebas de similitud de coseno
- Evaluar 10 preguntas y analizar resultados
- Demostrar control de alucinaciones

---

## 🧠 Tecnologías Utilizadas

| Componente | Tecnología |
|------------|------------|
| **LLM** | Google Gemini 2.5 Flash (vía API) |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) - **Local** |
| **Vector Store** | ChromaDB |
| **Framework RAG** | LangChain |
| **Interfaz Gráfica** | Gradio |
| **Carga de PDFs** | PyPDFLoader |
| **Lenguaje** | Python 3.14+ |
| **Entorno** | Virtual env (venv) |

---

## ⚙️ Arquitectura del Sistema


Usuario → GUI (Gradio) → Backend RAG → ChromaDB → Gemini → Respuesta
                              ↓
                        Embeddings locales
                        (all-MiniLM-L6-v2)


### Flujo completo:
1. El usuario escribe una pregunta en la interfaz gráfica
2. El sistema recupera fragmentos relevantes de ChromaDB
3. Se construye un prompt aumentado con el contexto
4. Gemini genera una respuesta basada SOLO en los manuales
5. Se muestran las fuentes consultadas

---

## 📊 Parámetros del Sistema

| Parámetro | Valor |
|-----------|-------|
| **Modelo Embeddings** | all-MiniLM-L6-v2 (local) |
| **Dimensión del vector** | 384 |
| **chunk_size** | 1000 |
| **overlap** | 100 |
| **k (chunks recuperados)** | 5 |
| **LLM** | Gemini 2.5 Flash |
| **Temperatura** | 0.2 |
| **Base vectorial** | ChromaDB |

---

## 🔧 Instalación y Ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone LINK_DEL_REPOSITORIO
cd NOMBRE_DEL_PROYECTO


### 2️⃣ Crear entorno virtual

```bash
python -m venv env


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
pip install google-genai python-dotenv langchain langchain-community langchain-chroma chromadb pypdf sentence-transformers gradio
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
├── 📄 app_gradio.py
├── 📂 pdfs_soporte/     ← Tus PDFs aquí
│   ├── pdf1.pdf
│   ├── pdf2.pdf
│   └── pdf3.pdf
├── 📄 .env
└── 📄 README.md
```

### 7️⃣ Ejecutar el asistente

**Versión consola:**
```bash
python app.py
```

**Versión interfaz gráfica (recomendada):**
```bash
python app_gradio.py
```

---

## 🖥️ Interfaz Gráfica (Gradio)

La interfaz permite:
- **Chat interactivo** con el asistente
- **Preguntas sugeridas** para pruebas rápidas
- **Visualización de fuentes** consultadas
- **Respuestas en formato Markdown**

### Capturas de la GUI:

*(Insertar aquí capturas de pantalla de la interfaz)*

---

## 🧪 Pruebas de Similitud de Coseno

Para demostrar que los embeddings entienden lenguaje coloquial:

| Pregunta coloquial | Concepto técnico | ¿Recuperó contexto? |
|-------------------|------------------|---------------------|
| "¿Cómo veo mi dirección IP en Linux?" | comando `ip a` | ✅ Sí |
| "Mi máquina virtual no agarra internet" | Configurar NAT o Bridge | ✅ Sí |
| "¿Cómo matar un proceso que no responde?" | comando `kill -9` | ✅ Sí |

**Ejecutar prueba:**
```bash
python prueba_similitud.py
```

---

## 📊 Evaluación Final (10 preguntas)

### Resultados obtenidos:

| ID | Tipo | Pregunta | ¿Acertó? |
|----|------|----------|----------|
| 1 | ✅ En PDF1 | ¿Qué beneficios ofrece la virtualización? | ✅ |
| 2 | ✅ En PDF1 | ¿Para qué sirven los laboratorios virtuales? | ✅ |
| 3 | ✅ En PDF1 | ¿Qué tipos de hipervisores se mencionan? | ✅ |
| 4 | ✅ En PDF1 | ¿Qué mejora la seguridad y aislamiento? | ✅ |
| 5 | ✅ En PDF2 | ¿Qué es la gestión de procesos? | ✅ |
| 6 | ✅ En PDF2 | ¿Relación entre memoria y almacenamiento? | ✅ |
| 7 | ✅ En PDF3 | ¿Qué se menciona sobre Host y Guest? | ✅ |
| 8 | ✅ En PDF3 | ¿Qué ventajas tienen los backups? | ✅ |
| 9 | ❌ Sin información | Precio VMware Workstation 2026 | ✅ (No alucinó) |
| 10 | ❌ Sin información | SO con inteligencia artificial | ✅ (No alucinó) |

### Estadísticas:

| Métrica | Resultado |
|---------|-----------|
| **Aciertos** | 8/8 (100%) en preguntas con información |
| **Control de alucinaciones** | 2/2 (100%) |
| **Fragmentos recuperados promedio** | 5.0 |

### Ejecutar evaluación:
```bash
python evaluacion_final.py
```

---

## 💬 Ejemplos de uso

### Ejemplo 1: Pregunta con información en los manuales

**Usuario:**
> ¿Qué beneficios ofrece la virtualización en entornos empresariales?

**Asistente:**
> ### 🔎 Diagnóstico probable
> La virtualización mejora el rendimiento, la seguridad, la administración y la continuidad del servicio.
>
> ### 🛠️ Pasos de solución
> 1. Reduce costos operativos
> 2. Automatiza procesos
> 3. Facilita la escalabilidad
>
> ### 💡 Recomendación preventiva
> Implementar virtualización para optimizar recursos empresariales.

### Ejemplo 2: Pregunta SIN información (prueba de no alucinación)

**Usuario:**
> ¿Cuál es el precio de VMware Workstation en 2026?

**Asistente:**
> No encuentro esta información en los manuales técnicos proporcionados.

---

## 📁 Estructura del Proyecto

```
asistente-soporte-tecnico/
│
├── app.py                          # Código principal (consola)
├── app_gradio.py                   # Interfaz gráfica con Gradio
├── evaluacion_final.py             # Evaluación de 10 preguntas
├── prueba_similitud.py             # Pruebas de similitud coseno
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
│
└── 📂 env/                         # Entorno virtual
```

---

## 📊 Avance 2: Detalle Técnico del Pipeline RAG

### 1. Selección y Carga de Documentos
- **Formato soportado:** PDF
- **Ubicación:** Carpeta `pdfs_soporte/`
- **Loader utilizado:** `PyPDFLoader` de LangChain
- **Documentos procesados:** 3 manuales técnicos

### 2. División en Fragmentos (Chunking)
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,      # Caracteres por fragmento
    chunk_overlap=100,    # Solapamiento entre fragmentos
)
```
- **Fragmentos generados:** 102
- **Estrategia:** División recursiva priorizando párrafos

### 3. Vectorización (Embeddings)
- **Modelo utilizado:** `sentence-transformers/all-MiniLM-L6-v2`
- **Ejecución:** **Totalmente local** (sin límites de cuota)
- **Dimensión del vector:** 384 dimensiones
- **Ventaja:** Preserva la privacidad de los datos

### 4. Base de Datos Vectorial
- **Tecnología:** ChromaDB
- **Métrica de similitud:** Coseno (`cosine`)

### 5. Mecanismo de Recuperación
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
```
- **Fragmentos recuperados:** 5 por consulta

### 6. Generación de Respuesta
- **Modelo LLM:** Gemini 2.5 Flash
- **Temperature:** 0.2 (más fiel al contexto)

---

## 🔒 Privacidad y Seguridad

- ✅ **Embeddings locales:** Los documentos nunca salen de tu máquina
- ✅ **Sin dependencia de API externa para vectorización**
- ✅ **Base vectorial persistente en disco**
- ✅ **Solo el LLM (Gemini) consume API**

---

## 🐛 Solución de Problemas Comunes

| Error | Solución |
|-------|----------|
| `ModuleNotFoundError` | Ejecutar `pip install -r requirements.txt` |
| `429 RESOURCE_EXHAUSTED` | Esperar 24 horas o usar otra API Key |
| `No se encontró la carpeta pdfs_soporte` | Crear la carpeta manualmente |
| `API Key no válida` | Verificar el archivo `.env` |

---

## 📅 Estado del Proyecto

| Avance | Estado | Fecha |
|--------|--------|-------|
| Avance 1 - Prompt Engineering | ✅ Completado | - |
| Avance 2 - Implementación RAG | ✅ Completado | - |
| Avance 3 - Evaluación RAGAS | ✅ Completado | - |
| Avance 4 - GUI y Evaluación Final | ✅ Completado | - |

---

## 👩‍💻 Autoras

**Catalina Gordillo** - Estudiante de Ingeniería de Sistemas  
**Sara Murcia** - Estudiante de Ingeniería de Sistemas

---


