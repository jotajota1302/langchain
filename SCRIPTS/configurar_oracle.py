"""
Script de configuración para el agente Oracle.
Crea el archivo de configuración con las credenciales de la base de datos.
"""

import sys
import os

# Añadir el directorio raíz al path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


def crear_configuracion():
    """
    Crea el archivo de configuración de Oracle de forma interactiva.
    """
    print("=" * 70)
    print("🔧 CONFIGURACIÓN DE ORACLE")
    print("=" * 70)
    print("\nEste script creará el archivo UTILS/config_oracle.py")
    print("con las credenciales de tu base de datos Oracle.\n")

    # Preguntar si usar configuración por defecto
    usar_default = input("¿Usar configuración por defecto? (s/n): ").strip().lower()

    if usar_default == 's':
        # Configuración por defecto proporcionada
        config = {
            'host': 'indudescs.bd.gva.es',
            'port': 1528,
            'service_name': 'indudes',
            'user': 'EXMARTEVALIJA',
            'password': 'Gm6>sq>803xNEDT41LAtlaAEBV'
        }
        print("\n✅ Usando configuración de DESA")
    else:
        # Solicitar configuración personalizada
        print("\nIngresa los datos de conexión:")
        config = {
            'host': input("  Host: ").strip(),
            'port': int(input("  Puerto (default 1521): ").strip() or "1521"),
            'service_name': input("  Service Name/SID: ").strip(),
            'user': input("  Usuario: ").strip(),
            'password': input("  Contraseña: ").strip()
        }

    # Crear contenido del archivo
    contenido = f"""# Configuración de conexión a Oracle
# ⚠️ IMPORTANTE: Este archivo contiene credenciales sensibles
# No lo subas a Git (está en .gitignore)

ORACLE_CONFIG = {{
    'host': '{config['host']}',
    'port': {config['port']},
    'service_name': '{config['service_name']}',
    'user': '{config['user']}',
    'password': '{config['password']}'
}}

# Información de la conexión:
# - Tipo de BD: Oracle
# - Driver: oracledb (python-oracledb)
# - DSN: {config['host']}:{config['port']}/{config['service_name']}
# - Usuario: {config['user']}
"""

    # Guardar archivo
    config_path = os.path.join(PROJECT_ROOT, 'UTILS', 'config_oracle.py')

    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(contenido)

        print(f"\n✅ Archivo creado: {config_path}")
        print("\n📋 Resumen de configuración:")
        print(f"   Host: {config['host']}")
        print(f"   Puerto: {config['port']}")
        print(f"   Service: {config['service_name']}")
        print(f"   Usuario: {config['user']}")
        print(f"   Contraseña: {'*' * len(config['password'])}")

        # Actualizar .gitignore
        gitignore_path = os.path.join(PROJECT_ROOT, '.gitignore')
        gitignore_content = ""

        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r', encoding='utf-8') as f:
                gitignore_content = f.read()

        if 'config_oracle.py' not in gitignore_content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n# Configuración Oracle (credenciales)\n")
                f.write("UTILS/config_oracle.py\n")
            print("\n✅ Añadido config_oracle.py a .gitignore")

        print("\n🚀 ¡Listo! Ahora puedes ejecutar:")
        print("   python AGENTS/agente_oracle.py")

    except Exception as e:
        print(f"\n❌ Error al crear archivo: {e}")
        return False

    return True


def main():
    """Función principal."""
    exito = crear_configuracion()

    if exito:
        print("\n" + "=" * 70)
        print("✅ CONFIGURACIÓN COMPLETADA")
        print("=" * 70)
    else:
        print("\n" + "=" * 70)
        print("❌ ERROR EN LA CONFIGURACIÓN")
        print("=" * 70)


if __name__ == "__main__":
    main()
