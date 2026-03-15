# 🤖 Asistente Experto de Soporte Técnico

## 📌 Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Asistente Experto basado en técnicas de Prompt Engineering**, orientado al análisis y solución de problemas de **soporte técnico en entornos informáticos**.

El sistema simula el comportamiento de un analista TI capaz de **diagnosticar fallos, proponer soluciones estructuradas y brindar recomendaciones preventivas**, mediante interacción por consola.

Este desarrollo corresponde al **Avance 1 del proyecto académico: Desarrollo de un Asistente Experto basado en RAG y Agentes**.

---

## 🎯 Objetivos

* Diseñar un asistente inteligente especializado en soporte técnico
* Aplicar técnicas de **System Prompt** para definir el comportamiento del modelo
* Implementar **Few-Shot Prompting** para guiar el formato de las respuestas
* Utilizar historial conversacional para simular interacción contextual
* Generar respuestas estructuradas en formato técnico

---

## 🧠 Tecnologías Utilizadas

* Python
* API Google GenAI
* Prompt Engineering
* Consola (CLI)
* Entorno virtual (venv)

---

## ⚙️ Funcionamiento

El asistente analiza preguntas relacionadas con:

* Redes básicas
* Sistemas operativos Linux y Windows
* Virtualización
* Diagnóstico de errores técnicos
* Configuración de software

Cada respuesta generada sigue la estructura:

* 🔎 Diagnóstico probable
* 🛠️ Pasos de solución
* 💡 Recomendación preventiva

Esto permite una interacción clara y orientada a la resolución de problemas técnicos reales.

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

### 4️⃣ Instalar dependencias

```bash
pip install google-genai python-dotenv
```

### 5️⃣ Configurar variable de entorno

Crear un archivo `.env` y agregar:

```
GENAI_API_KEY=tu_api_key_aqui
```

### 6️⃣ Ejecutar el asistente

```bash
python asistente_soporte.py
```

---

## 💬 Ejemplo de uso

Usuario:

> No puedo hacer ping a otra máquina en la red

Asistente:

* Diagnóstico de posible fallo de conectividad
* Pasos para verificar IP, gateway y configuración de red
* Recomendaciones preventivas

---

## 📚 Conceptos Aplicados

* Prompt Engineering
* Few-Shot Learning
* Diseño de asistentes expertos
* Interacción conversacional con IA
* Diagnóstico técnico automatizado

---

## 📁 Estructura del proyecto

## 📁 Estructura del Proyecto

```
asistente-soporte-tecnico/
│
├── app.py
├── requirements.txt
├── .env
├── README.md
│
└── evidencias/
    ├── ejecucion_consola.png
    ├── pregunta_asistente.png
    └── respuesta_asistente.png
```

---

## 👩‍💻 Autores

**Catalina Gordillo**
Estudiante de Ingeniería de Sistemas
**Sara Murcia**
Estudiante de Ingeniería de Sistemas

Proyecto académico – Desarrollo de aplicaciones con IA
