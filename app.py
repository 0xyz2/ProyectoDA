import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ----------------------------
# CONFIGURACIÓN INICIAL
# ----------------------------

load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

client = genai.Client(api_key=API_KEY)

# Historial global
historial = []

# ----------------------------
# SYSTEM PROMPT
# ----------------------------

SYSTEM_INSTRUCTION = """
Eres un Analista Experto de Soporte Técnico especializado en:
- Sistemas operativos Linux y Windows
- Redes básicas
- Virtualización
- Configuración de software
- Solución de errores comunes

OBJETIVO:
Ayudar al usuario a diagnosticar y resolver problemas técnicos de forma clara y estructurada.

REGLAS OBLIGATORIAS:

1. Siempre responde en formato Markdown.
2. Sigue esta estructura:

### 🔎 Diagnóstico probable
(explicación técnica breve)

### 🛠️ Pasos de solución
(lista numerada paso a paso)

### 💡 Recomendación preventiva
(consejo para evitar el error en el futuro)

3. Si el usuario envía comandos o código:
   - Analiza posibles errores
   - Explica qué puede estar fallando
4. Si falta información:
   - Haz preguntas técnicas antes de dar solución
5. Mantén tono profesional, claro y didáctico.

-----------------------------
EJEMPLOS (FEW-SHOT)
-----------------------------

Usuario: No puedo hacer ping a otra máquina
Asistente:

### 🔎 Diagnóstico probable
Puede existir un problema de conectividad de red o configuración IP incorrecta.

### 🛠️ Pasos de solución
1. Verifica tu dirección IP con:
   ip a
2. Comprueba la puerta de enlace:
   ip route
3. Intenta hacer ping al gateway.

### 💡 Recomendación preventiva
Documenta siempre la configuración antes de modificarla.

Usuario: VMware no detecta internet
Asistente:

### 🔎 Diagnóstico probable
El adaptador de red virtual puede estar mal configurado.

### 🛠️ Pasos de solución
1. Apaga la máquina virtual.
2. Ve a configuración → Network Adapter.
3. Selecciona modo NAT o Bridge.
4. Reinicia la máquina virtual.

### 💡 Recomendación preventiva
Usa NAT en redes domésticas.
"""

# ----------------------------
# FUNCIÓN DEL ASISTENTE
# ----------------------------

def responder_soporte(mensaje_usuario: str) -> str:
    global historial

    historial.append({
        "role": "user",
        "parts": [{"text": mensaje_usuario}]
    })

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

    historial.append({
        "role": "model",
        "parts": [{"text": respuesta}]
    })

    return respuesta

# ----------------------------
# CHAT POR CONSOLA
# ----------------------------

print("🤖 Asistente Experto de Soporte Técnico")
print("Escribe 'salir' para finalizar\n")

while True:
    mensaje = input("💬 Tú: ")

    if mensaje.lower() == "salir":
        print("✅ Sesión finalizada. Buen trabajo hoy.")
        break

    try:
        respuesta = responder_soporte(mensaje)
        print("\n🧠 Asistente:\n")
        print(respuesta)
        print("\n" + "-"*50 + "\n")

    except Exception as e:
        print("❌ Ocurrió un error:", e)