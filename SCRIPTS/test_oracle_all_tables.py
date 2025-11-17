"""
Script para verificar tablas en todos los esquemas accesibles
"""

import sys
import os

# Configurar UTF-8
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

print("=" * 70)
print("🔍 BÚSQUEDA DE TABLAS EN TODOS LOS ESQUEMAS")
print("=" * 70)

from AGENTS.agente_oracle import oracle_conn

# Conectar
print("\n1. Conectando a Oracle...")
resultado = oracle_conn.conectar()
print(f"   {resultado}")

if "❌" in resultado:
    print("Error de conexión")
    sys.exit(1)

# Buscar en USER_TABLES
print("\n2. Buscando en USER_TABLES (tablas propias)...")
query_user = "SELECT COUNT(*) FROM user_tables"
resultado = oracle_conn.ejecutar_query(query_user)
if isinstance(resultado, dict):
    count = resultado['rows'][0][0]
    print(f"   Encontradas: {count} tablas")
else:
    print(f"   Error: {resultado}")

# Buscar en ALL_TABLES (todos los esquemas accesibles)
print("\n3. Buscando en ALL_TABLES (todos los esquemas accesibles)...")
query_all = """
    SELECT owner, COUNT(*) as num_tables
    FROM all_tables
    GROUP BY owner
    ORDER BY num_tables DESC
"""
resultado = oracle_conn.ejecutar_query(query_all)
if isinstance(resultado, dict):
    print(f"\n   Esquemas con tablas accesibles ({resultado['count']} esquemas):")
    print(f"   {'Esquema':<30} {'Num Tablas'}")
    print("   " + "-" * 50)
    for row in resultado['rows'][:15]:  # Mostrar top 15
        owner, num = row
        print(f"   {owner:<30} {num}")
else:
    print(f"   Error: {resultado}")

# Listar tablas del esquema con más tablas (primeros 20)
print("\n4. Listando primeras 20 tablas del esquema principal...")
query_sample = """
    SELECT table_name, owner
    FROM all_tables
    WHERE ROWNUM <= 20
    ORDER BY owner, table_name
"""
resultado = oracle_conn.ejecutar_query(query_sample)
if isinstance(resultado, dict):
    print(f"\n   Muestra de tablas:")
    print(f"   {'Tabla':<30} {'Esquema'}")
    print("   " + "-" * 50)
    for row in resultado['rows']:
        table, owner = row
        print(f"   {table:<30} {owner}")
else:
    print(f"   Error: {resultado}")

# Cerrar
oracle_conn.cerrar()

print("\n" + "=" * 70)
print("✅ BÚSQUEDA COMPLETADA")
print("=" * 70)
