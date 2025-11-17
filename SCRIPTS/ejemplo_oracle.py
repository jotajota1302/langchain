"""
Script de ejemplo de uso del Agente Oracle
Muestra diferentes formas de interactuar con el agente de forma programática.
"""

import sys
import os

# Añadir el directorio raíz al path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Importar el agente
from AGENTS.agente_oracle import crear_agente, oracle_conn


def ejemplo_1_exploracion_basica():
    """
    Ejemplo 1: Exploración básica de la base de datos.
    Conecta, lista tablas y describe una.
    """
    print("=" * 70)
    print("EJEMPLO 1: Exploración Básica")
    print("=" * 70 + "\n")

    agente = crear_agente()

    # Secuencia de comandos
    comandos = [
        "Conéctate a la base de datos Oracle",
        "Muéstrame todas las tablas que hay",
        "Describe la estructura de una tabla interesante que encuentres"
    ]

    for i, comando in enumerate(comandos, 1):
        print(f"\n[{i}] Comando: {comando}")
        print("-" * 70)
        resultado = agente.invoke({"input": comando})
        print(f"Respuesta: {resultado['output']}\n")

    oracle_conn.cerrar()


def ejemplo_2_analisis_relaciones():
    """
    Ejemplo 2: Análisis de relaciones entre tablas.
    Identifica Foreign Keys y genera diagrama ER.
    """
    print("=" * 70)
    print("EJEMPLO 2: Análisis de Relaciones")
    print("=" * 70 + "\n")

    agente = crear_agente()

    comandos = [
        "Conéctate a Oracle",
        "Muéstrame todas las relaciones (Foreign Keys) que existen",
        "Genera un diagrama ER con las principales tablas relacionadas"
    ]

    for i, comando in enumerate(comandos, 1):
        print(f"\n[{i}] Comando: {comando}")
        print("-" * 70)
        resultado = agente.invoke({"input": comando})
        print(f"Respuesta: {resultado['output']}\n")

    oracle_conn.cerrar()


def ejemplo_3_analisis_tabla_especifica():
    """
    Ejemplo 3: Análisis completo de una tabla específica.
    Solicita al usuario el nombre de una tabla y la analiza en profundidad.
    """
    print("=" * 70)
    print("EJEMPLO 3: Análisis Completo de Tabla")
    print("=" * 70 + "\n")

    agente = crear_agente()

    # Primero conectar
    print("[1] Conectando a Oracle...")
    agente.invoke({"input": "Conéctate a Oracle"})

    # Listar tablas
    print("\n[2] Listando tablas disponibles...")
    resultado = agente.invoke({"input": "Lista todas las tablas"})
    print(f"\n{resultado['output']}\n")

    # Solicitar nombre de tabla
    tabla = input("\n¿Qué tabla quieres analizar? (escribe el nombre): ").strip().upper()

    if tabla:
        # Análisis completo
        comandos = [
            f"Describe la estructura completa de la tabla {tabla}",
            f"Muéstrame los índices de {tabla}",
            f"¿Qué relaciones (FK) tiene la tabla {tabla}?"
        ]

        for i, comando in enumerate(comandos, 3):
            print(f"\n[{i}] Comando: {comando}")
            print("-" * 70)
            resultado = agente.invoke({"input": comando})
            print(f"Respuesta: {resultado['output']}\n")

    oracle_conn.cerrar()


def ejemplo_4_metadata_avanzada():
    """
    Ejemplo 4: Consulta de metadata avanzada.
    Explora vistas, secuencias, triggers y procedimientos.
    """
    print("=" * 70)
    print("EJEMPLO 4: Metadata Avanzada")
    print("=" * 70 + "\n")

    agente = crear_agente()

    comandos = [
        "Conéctate a Oracle",
        "Muéstrame todas las vistas que existen",
        "Lista las secuencias del esquema",
        "¿Qué triggers hay definidos?",
        "Muéstrame los procedimientos y funciones"
    ]

    for i, comando in enumerate(comandos, 1):
        print(f"\n[{i}] Comando: {comando}")
        print("-" * 70)
        resultado = agente.invoke({"input": comando})
        print(f"Respuesta: {resultado['output']}\n")

    oracle_conn.cerrar()


def ejemplo_5_conversacion_natural():
    """
    Ejemplo 5: Conversación natural con el agente.
    Demuestra la capacidad del agente de entender lenguaje natural.
    """
    print("=" * 70)
    print("EJEMPLO 5: Conversación Natural")
    print("=" * 70 + "\n")

    agente = crear_agente()

    comandos = [
        "Hola, necesito que te conectes a la base de datos",
        "¿Cuántas tablas hay en total?",
        "Busca tablas que puedan estar relacionadas con usuarios o clientes",
        "De esas tablas, ¿cuál parece ser la principal?",
        "Analízala completamente y dame un resumen"
    ]

    for i, comando in enumerate(comandos, 1):
        print(f"\n[{i}] Tú: {comando}")
        print("-" * 70)
        resultado = agente.invoke({"input": comando})
        print(f"Agente: {resultado['output']}\n")

    oracle_conn.cerrar()


def ejemplo_6_generacion_documentacion():
    """
    Ejemplo 6: Generación de documentación técnica.
    Pide al agente que genere documentación completa del esquema.
    """
    print("=" * 70)
    print("EJEMPLO 6: Generación de Documentación")
    print("=" * 70 + "\n")

    agente = crear_agente()

    comandos = [
        "Conéctate a Oracle",
        "Necesito documentar la base de datos. Primero, dame un resumen general: número de tablas, vistas, secuencias",
        "Ahora identifica las 5 tablas más importantes basándote en las relaciones",
        "Genera un diagrama ER que muestre cómo se relacionan esas 5 tablas",
        "Para cada una de esas 5 tablas, dame un resumen de su estructura (columnas principales, PKs, FKs)"
    ]

    for i, comando in enumerate(comandos, 1):
        print(f"\n[{i}] Solicitud: {comando}")
        print("-" * 70)
        resultado = agente.invoke({"input": comando})
        print(f"\nRespuesta:\n{resultado['output']}\n")
        print("=" * 70)

    oracle_conn.cerrar()


def menu_principal():
    """
    Menú interactivo para ejecutar los ejemplos.
    """
    ejemplos = {
        '1': ('Exploración Básica', ejemplo_1_exploracion_basica),
        '2': ('Análisis de Relaciones', ejemplo_2_analisis_relaciones),
        '3': ('Análisis de Tabla Específica', ejemplo_3_analisis_tabla_especifica),
        '4': ('Metadata Avanzada', ejemplo_4_metadata_avanzada),
        '5': ('Conversación Natural', ejemplo_5_conversacion_natural),
        '6': ('Generación de Documentación', ejemplo_6_generacion_documentacion),
    }

    while True:
        print("\n" + "=" * 70)
        print("EJEMPLOS DE USO DEL AGENTE ORACLE")
        print("=" * 70)
        print("\nSelecciona un ejemplo:")
        for num, (nombre, _) in ejemplos.items():
            print(f"  {num}. {nombre}")
        print("  0. Salir")
        print("=" * 70)

        opcion = input("\nOpción: ").strip()

        if opcion == '0':
            print("\n👋 ¡Hasta luego!")
            break
        elif opcion in ejemplos:
            print("\n")
            _, funcion = ejemplos[opcion]
            try:
                funcion()
            except KeyboardInterrupt:
                print("\n\n⚠️  Ejemplo interrumpido")
            except Exception as e:
                print(f"\n❌ Error: {e}")

            input("\nPresiona ENTER para continuar...")
        else:
            print("\n❌ Opción inválida")


def main():
    """
    Función principal.
    """
    print("=" * 70)
    print("🗄️  AGENTE ORACLE - EJEMPLOS DE USO")
    print("=" * 70)
    print("\nEste script muestra diferentes formas de usar el Agente Oracle.")
    print("\n⚠️  Requisitos:")
    print("  1. Ollama ejecutándose (ollama serve)")
    print("  2. Modelo descargado (ollama pull llama2)")
    print("  3. Configuración en UTILS/config_oracle.py")
    print("\n")

    # Verificar configuración
    config = oracle_conn.cargar_configuracion()
    if not config:
        print("❌ No se encontró configuración de Oracle.")
        print("Ejecuta: python SCRIPTS/configurar_oracle.py")
        return

    print(f"✅ Configuración encontrada: {config['user']}@{config['host']}\n")

    # Si se pasa un argumento, ejecutar ese ejemplo directamente
    if len(sys.argv) > 1:
        ejemplo_num = sys.argv[1]
        ejemplos_directos = {
            '1': ejemplo_1_exploracion_basica,
            '2': ejemplo_2_analisis_relaciones,
            '3': ejemplo_3_analisis_tabla_especifica,
            '4': ejemplo_4_metadata_avanzada,
            '5': ejemplo_5_conversacion_natural,
            '6': ejemplo_6_generacion_documentacion,
        }

        if ejemplo_num in ejemplos_directos:
            ejemplos_directos[ejemplo_num]()
        else:
            print(f"❌ Ejemplo '{ejemplo_num}' no encontrado")
            print(f"Opciones válidas: {', '.join(ejemplos_directos.keys())}")
    else:
        # Mostrar menú interactivo
        menu_principal()


if __name__ == "__main__":
    main()
