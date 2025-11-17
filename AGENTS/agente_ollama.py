"""
Agente de ejemplo con LangChain + Ollama
Este script demuestra cómo crear un agente que usa un modelo local de Ollama
con herramientas personalizadas.
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

from langchain_community.llms import Ollama
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.memory import ConversationBufferMemory
import re
from datetime import datetime


# ============================================================================
# DEFINICIÓN DE HERRAMIENTAS (TOOLS)
# ============================================================================

def calculadora(expresion: str) -> str:
    """
    Herramienta para realizar cálculos matemáticos básicos.
    Args:
        expresion: Expresión matemática a evaluar (ej: "2+2", "10*5")
    Returns:
        El resultado del cálculo
    """
    try:
        # Sanitizar la expresión para seguridad
        expresion_limpia = re.sub(r'[^0-9+\-*/().\s]', '', expresion)
        resultado = eval(expresion_limpia)
        return f"El resultado es: {resultado}"
    except Exception as e:
        return f"Error al calcular: {str(e)}"


def obtener_fecha_hora(entrada: str) -> str:
    """
    Herramienta que devuelve la fecha y hora actual.
    Args:
        entrada: No se usa, pero es requerido por la interfaz
    Returns:
        Fecha y hora actual formateada
    """
    ahora = datetime.now()
    return f"Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}"


def convertidor_temperatura(entrada: str) -> str:
    """
    Convierte temperaturas entre Celsius y Fahrenheit.
    Formato esperado: "25C" o "77F"
    Args:
        entrada: Temperatura con unidad (ej: "25C", "77F")
    Returns:
        Temperatura convertida
    """
    try:
        entrada = entrada.strip().upper()
        if entrada.endswith('C'):
            celsius = float(entrada[:-1])
            fahrenheit = (celsius * 9/5) + 32
            return f"{celsius}°C equivale a {fahrenheit:.2f}°F"
        elif entrada.endswith('F'):
            fahrenheit = float(entrada[:-1])
            celsius = (fahrenheit - 32) * 5/9
            return f"{fahrenheit}°F equivale a {celsius:.2f}°C"
        else:
            return "Formato inválido. Usa '25C' o '77F'"
    except Exception as e:
        return f"Error al convertir: {str(e)}"


def analizador_texto(texto: str) -> str:
    """
    Analiza un texto y devuelve estadísticas básicas.
    Args:
        texto: Texto a analizar
    Returns:
        Estadísticas del texto
    """
    palabras = texto.split()
    caracteres = len(texto)
    caracteres_sin_espacios = len(texto.replace(" ", ""))
    lineas = texto.count('\n') + 1

    return f"""Análisis del texto:
- Palabras: {len(palabras)}
- Caracteres (con espacios): {caracteres}
- Caracteres (sin espacios): {caracteres_sin_espacios}
- Líneas: {lineas}
- Palabra más larga: {max(palabras, key=len) if palabras else 'N/A'}"""


# ============================================================================
# CONFIGURACIÓN DEL AGENTE
# ============================================================================

def crear_agente():
    """
    Crea y configura el agente con Ollama y sus herramientas.
    Returns:
        AgentExecutor configurado y listo para usar
    """

    # 1. Inicializar el modelo local de Ollama
    print("🔧 Inicializando modelo Ollama...")
    llm = Ollama(
        model="llama2",  # Cambia esto por el modelo que tengas instalado
        temperature=0.7,
        # base_url="http://localhost:11434"  # URL por defecto de Ollama
    )

    # 2. Definir las herramientas disponibles para el agente
    herramientas = [
        Tool(
            name="Calculadora",
            func=calculadora,
            description="Útil para realizar cálculos matemáticos. Entrada: expresión matemática como '2+2' o '10*5'"
        ),
        Tool(
            name="FechaHora",
            func=obtener_fecha_hora,
            description="Obtiene la fecha y hora actual. No requiere entrada específica."
        ),
        Tool(
            name="ConvertidorTemperatura",
            func=convertidor_temperatura,
            description="Convierte temperaturas entre Celsius y Fahrenheit. Entrada: temperatura con unidad como '25C' o '77F'"
        ),
        Tool(
            name="AnalizadorTexto",
            func=analizador_texto,
            description="Analiza un texto y devuelve estadísticas (palabras, caracteres, etc.). Entrada: el texto a analizar"
        )
    ]

    # 3. Crear el prompt template para el agente ReAct
    template = """Eres un asistente útil que tiene acceso a las siguientes herramientas:

{tools}

Nombres de las herramientas: {tool_names}

Para responder, sigue este formato:

Pregunta: la pregunta de entrada que debes responder
Pensamiento: siempre debes pensar qué hacer
Acción: la acción a tomar, debe ser una de [{tool_names}]
Entrada de Acción: la entrada para la acción
Observación: el resultado de la acción
... (este Pensamiento/Acción/Entrada de Acción/Observación puede repetirse N veces)
Pensamiento: Ahora sé la respuesta final
Respuesta Final: la respuesta final a la pregunta original

Comienza!

Historial de conversación:
{chat_history}

Pregunta: {input}
Pensamiento: {agent_scratchpad}"""

    prompt = PromptTemplate(
        template=template,
        input_variables=["input", "chat_history", "agent_scratchpad", "tools", "tool_names"]
    )

    # 4. Crear memoria para el agente
    memoria = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # 5. Crear el agente ReAct
    agente = create_react_agent(
        llm=llm,
        tools=herramientas,
        prompt=prompt
    )

    # 6. Crear el ejecutor del agente
    agente_executor = AgentExecutor(
        agent=agente,
        tools=herramientas,
        memory=memoria,
        verbose=True,  # Muestra el proceso de razonamiento
        handle_parsing_errors=True,
        max_iterations=5  # Máximo de iteraciones para evitar bucles infinitos
    )

    return agente_executor


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que ejecuta el agente en modo interactivo.
    """
    print("=" * 70)
    print("🤖 AGENTE LANGCHAIN + OLLAMA")
    print("=" * 70)
    print("\nEste agente tiene las siguientes capacidades:")
    print("  📊 Realizar cálculos matemáticos")
    print("  🕐 Obtener fecha y hora actual")
    print("  🌡️  Convertir temperaturas (C ↔ F)")
    print("  📝 Analizar textos")
    print("\nEscribe 'salir' o 'exit' para terminar\n")
    print("=" * 70 + "\n")

    # Crear el agente
    try:
        agente = crear_agente()
        print("✅ Agente inicializado correctamente\n")
    except Exception as e:
        print(f"❌ Error al inicializar el agente: {e}")
        print("\n⚠️  Asegúrate de que Ollama está ejecutándose con:")
        print("   ollama serve")
        print("   ollama pull llama2")
        return

    # Loop de conversación
    while True:
        try:
            # Obtener entrada del usuario
            pregunta = input("👤 Tú: ").strip()

            # Verificar si quiere salir
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                print("\n👋 ¡Hasta luego!")
                break

            # Verificar que no esté vacío
            if not pregunta:
                continue

            # Ejecutar el agente
            print("\n🤖 Agente:", end=" ")
            respuesta = agente.invoke({"input": pregunta})

            # Mostrar la respuesta final
            print("\n" + "=" * 70)
            print(f"📤 Respuesta: {respuesta['output']}")
            print("=" * 70 + "\n")

        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
