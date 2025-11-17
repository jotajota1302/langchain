"""
Test del agente Oracle con LLM - Ejecución programática
"""

import sys
import os

# Configurar UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

print("=" * 70)
print("🤖 TEST DEL AGENTE ORACLE CON LLM")
print("=" * 70)

# Importar y crear agente
print("\n1. Inicializando agente...")
try:
    from AGENTS.agente_oracle import crear_agente, oracle_conn
    agente = crear_agente()
    print("✅ Agente creado correctamente")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Lista de comandos a ejecutar
comandos = [
    "Conéctate a la base de datos Oracle",
    "¿Cuántos esquemas hay disponibles?",
    "Muéstrame las tablas del esquema ADMIN"
]

# Ejecutar comandos
for i, comando in enumerate(comandos, 1):
    print(f"\n{i}. Ejecutando: '{comando}'")
    print("-" * 70)

    try:
        respuesta = agente.invoke({"input": comando})
        print(f"\n📤 Respuesta del agente:")
        print(respuesta['output'])
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

# Cerrar
print("\n" + "=" * 70)
print("Cerrando conexión...")
oracle_conn.cerrar()
print("✅ TEST COMPLETADO")
print("=" * 70)
