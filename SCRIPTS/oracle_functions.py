"""
Script rápido para ejecutar consultas Oracle sin LLM (solo lectura).
Permite lanzar comandos como: listar_tablas, describir_tabla <nombre>, obtener_relaciones, obtener_indices <nombre>, generar_diagrama_er, consultar_metadata <tipo>.
Uso:
    py SCRIPTS/oracle_functions.py [comando] [argumento_opcional]
Ejemplos:
    py SCRIPTS/oracle_functions.py listar_tablas
    py SCRIPTS/oracle_functions.py describir_tabla CLIENTES
    py SCRIPTS/oracle_functions.py obtener_relaciones
    py SCRIPTS/oracle_functions.py obtener_indices CLIENTES
    py SCRIPTS/oracle_functions.py generar_diagrama_er
    py SCRIPTS/oracle_functions.py consultar_metadata vistas
"""

import sys
import os

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

def main():
    if len(sys.argv) < 2:
        print("Uso: py SCRIPTS/oracle_functions.py [comando] [argumento_opcional]")
        print("Comandos disponibles: listar_tablas, listar_tablas_todos, describir_tabla <tabla>, obtener_relaciones [tabla], obtener_indices <tabla>, generar_diagrama_er [tablas], consultar_metadata <tipo>")
        sys.exit(1)

    comando = sys.argv[1].lower()
    argumento = sys.argv[2] if len(sys.argv) > 2 else ""

    print("Conectando a Oracle...")
    resultado = conectar_oracle("")
    print(resultado)
    if "❌" in resultado:
        sys.exit(1)

    if comando == "listar_tablas":
        print(listar_tablas(argumento))
    elif comando == "listar_tablas_todos":
        # Consulta ALL_TABLES y agrupa por esquema
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
            for row in resultado['rows'][:100]:  # Mostrar primeras 100
                owner, table_name = row
                print(f"{owner:<20} {table_name}")
            if resultado['count'] > 100:
                print(f"\n... y {resultado['count'] - 100} tablas más")
        else:
            print(resultado)
    elif comando == "describir_tabla":
        if not argumento:
            print("Debes indicar el nombre de la tabla.")
        else:
            print(describir_tabla(argumento))
    elif comando == "obtener_relaciones":
        print(obtener_relaciones(argumento))
    elif comando == "obtener_indices":
        if not argumento:
            print("Debes indicar el nombre de la tabla.")
        else:
            print(obtener_indices(argumento))
    elif comando == "generar_diagrama_er":
        print(generar_diagrama_er(argumento))
    elif comando == "consultar_metadata":
        if not argumento:
            print("Debes indicar el tipo (vistas, secuencias, triggers, procedimientos).")
        else:
            print(consultar_metadata(argumento))
    else:
        print(f"Comando no reconocido: {comando}")

    print("Cerrando conexión...")
    print(oracle_conn.cerrar())

if __name__ == "__main__":
    main()
