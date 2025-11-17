"""
Script de prueba simple para verificar conexión a Oracle y listar tablas.
No requiere interacción, ejecuta automáticamente.
"""

import sys
import os

# Configurar UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Añadir el directorio raíz al path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

print("=" * 70)
print("🔍 TEST DE CONEXIÓN A ORACLE")
print("=" * 70)

# Importar módulos necesarios
print("\n1. Importando módulos...")
try:
    import oracledb
    from AGENTS.agente_oracle import oracle_conn, listar_tablas, conectar_oracle
    print("   ✅ Módulos importados correctamente")
except Exception as e:
    print(f"   ❌ Error importando: {e}")
    sys.exit(1)

# Cargar configuración
print("\n2. Cargando configuración...")
try:
    config = oracle_conn.cargar_configuracion()
    if config:
        print(f"   ✅ Configuración encontrada")
        print(f"   - Host: {config['host']}")
        print(f"   - Puerto: {config['port']}")
        print(f"   - Servicio: {config['service_name']}")
        print(f"   - Usuario: {config['user']}")
    else:
        print("   ❌ No se encontró configuración")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    sys.exit(1)

# Conectar a Oracle
print("\n3. Conectando a Oracle...")
try:
    resultado = conectar_oracle("")
    print(f"   {resultado}")

    if "❌" in resultado:
        print("\n⚠️  No se pudo conectar a Oracle")
        print("Verifica que:")
        print("  - El servidor esté accesible desde tu red")
        print("  - Las credenciales sean correctas")
        print("  - El puerto 1528 esté abierto")
        sys.exit(1)
    else:
        print("   ✅ Conexión exitosa")
except Exception as e:
    print(f"   ❌ Error al conectar: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Listar tablas
print("\n4. Listando tablas del esquema...")
try:
    resultado_tablas = listar_tablas("")
    print("\n" + resultado_tablas)

    if "❌" in resultado_tablas:
        print("\n⚠️  Error al listar tablas")
    else:
        print("\n✅ Tablas listadas correctamente")
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Cerrar conexión
print("\n5. Cerrando conexión...")
try:
    resultado_cierre = oracle_conn.cerrar()
    print(f"   {resultado_cierre}")
except Exception as e:
    print(f"   ⚠️  Error al cerrar: {e}")

print("\n" + "=" * 70)
print("✅ TEST COMPLETADO")
print("=" * 70)
