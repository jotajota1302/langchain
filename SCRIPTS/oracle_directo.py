"""
Uso directo de las herramientas de Oracle (SIN LLM - MUY RÁPIDO)
Este script te permite usar todas las funcionalidades sin esperar al agente LLM.
"""

import sys
import os

# Configurar UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from AGENTS.agente_oracle import (
    conectar_oracle,
    listar_tablas,
    describir_tabla,
    obtener_relaciones,
    obtener_indices,
    generar_diagrama_er,
    consultar_metadata,
    oracle_conn
)

def menu():
    """Menú interactivo para usar las herramientas de Oracle."""

    print("=" * 70)
    print("🗄️  HERRAMIENTAS ORACLE - MODO DIRECTO (RÁPIDO)")
    print("=" * 70)
    print("\nEste modo usa las herramientas directamente, SIN agente LLM.")
    print("Es mucho más rápido y perfecto para análisis de BD.\n")

    # Conectar automáticamente
    print("Conectando a Oracle...")
    resultado = conectar_oracle("")
    print(resultado)

    if "❌" in resultado:
        print("\nNo se pudo conectar. Verifica la configuración.")
        return

    while True:
        print("\n" + "=" * 70)
        print("MENÚ DE OPCIONES")
        print("=" * 70)
        print("1. Listar todas las tablas")
        print("2. Describir una tabla específica")
        print("3. Ver relaciones (Foreign Keys)")
        print("4. Ver índices de una tabla")
        print("5. Generar diagrama ER")
        print("6. Consultar metadata (vistas, secuencias, etc.)")
        print("7. Listar tablas por esquema")
        print("0. Salir")
        print("=" * 70)

        opcion = input("\nSelecciona una opción: ").strip()

        if opcion == "0":
            print("\nCerrando conexión...")
            oracle_conn.cerrar()
            print("👋 ¡Hasta luego!")
            break

        elif opcion == "1":
            print("\n" + "-" * 70)
            print(listar_tablas(""))

        elif opcion == "2":
            tabla = input("\n¿Qué tabla quieres describir? ").strip().upper()
            if tabla:
                print("\n" + "-" * 70)
                print(describir_tabla(tabla))

        elif opcion == "3":
            tabla = input("\n¿Tabla específica? (Enter para todas): ").strip().upper()
            print("\n" + "-" * 70)
            print(obtener_relaciones(tabla))

        elif opcion == "4":
            tabla = input("\n¿Qué tabla? ").strip().upper()
            if tabla:
                print("\n" + "-" * 70)
                print(obtener_indices(tabla))

        elif opcion == "5":
            tablas = input("\n¿Tablas separadas por comas? (Enter para todas): ").strip()
            print("\n" + "-" * 70)
            print(generar_diagrama_er(tablas))

        elif opcion == "6":
            print("\nTipos disponibles: vistas, secuencias, triggers, procedimientos")
            tipo = input("¿Qué tipo?: ").strip().lower()
            if tipo:
                print("\n" + "-" * 70)
                print(consultar_metadata(tipo))

        elif opcion == "7":
            # Buscar tablas por esquema
            query = """
                SELECT owner, table_name
                FROM all_tables
                WHERE owner NOT IN ('SYS', 'SYSTEM', 'MDSYS', 'XDB', 'CTXSYS')
                ORDER BY owner, table_name
            """
            resultado = oracle_conn.ejecutar_query(query)
            if isinstance(resultado, dict):
                print(f"\n📊 Tablas por esquema ({resultado['count']} tablas):")
                print(f"{'Esquema':<20} {'Tabla'}")
                print("-" * 70)
                for row in resultado['rows'][:50]:  # Mostrar primeras 50
                    owner, table_name = row
                    print(f"{owner:<20} {table_name}")
                if resultado['count'] > 50:
                    print(f"\n... y {resultado['count'] - 50} tablas más")
            else:
                print(resultado)

        else:
            print("\n❌ Opción inválida")


def main():
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario")
        oracle_conn.cerrar()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        oracle_conn.cerrar()


if __name__ == "__main__":
    main()
