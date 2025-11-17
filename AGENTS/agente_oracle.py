"""
Agente Analista de Bases de Datos Oracle con LangChain + Ollama
Este agente se conecta a una base de datos Oracle y proporciona herramientas
para analizar la estructura de la base de datos (SOLO LECTURA).

IMPORTANTE: Este agente NUNCA modifica datos, solo consulta metadata.
"""

import sys
import os

# Configurar codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Añadir el directorio raíz al path para imports
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from langchain_community.llms import Ollama
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_classic.memory import ConversationBufferMemory

try:
    import oracledb
except ImportError:
    print("⚠️  Módulo 'oracledb' no encontrado. Instalando...")
    print("   pip install oracledb")
    sys.exit(1)

from datetime import datetime
import json


# ============================================================================
# CONFIGURACIÓN DE CONEXIÓN ORACLE
# ============================================================================

class OracleConnection:
    """Gestiona la conexión a Oracle con modo de solo lectura."""

    def __init__(self):
        self.connection = None
        self.config = None

    def cargar_configuracion(self):
        """Carga configuración desde archivo config_oracle.py"""
        try:
            config_path = os.path.join(PROJECT_ROOT, 'UTILS', 'config_oracle.py')

            if not os.path.exists(config_path):
                return None

            # Leer el archivo de configuración
            with open(config_path, 'r', encoding='utf-8') as f:
                config_code = f.read()

            # Ejecutar el código y extraer ORACLE_CONFIG
            namespace = {}
            exec(config_code, namespace)
            self.config = namespace.get('ORACLE_CONFIG')
            return self.config

        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return None

    def conectar(self):
        """Establece conexión con Oracle en modo de solo lectura."""
        try:
            if not self.config:
                self.cargar_configuracion()

            if not self.config:
                return "❌ No se encontró configuración. Ejecuta el script de configuración primero."

            # Crear DSN (Data Source Name)
            dsn = oracledb.makedsn(
                self.config['host'],
                self.config['port'],
                service_name=self.config['service_name']
            )

            # Conectar a Oracle
            self.connection = oracledb.connect(
                user=self.config['user'],
                password=self.config['password'],
                dsn=dsn
            )

            # Configurar conexión como READ ONLY
            cursor = self.connection.cursor()
            cursor.execute("SET TRANSACTION READ ONLY")
            cursor.close()

            return f"✅ Conectado a Oracle: {self.config['host']}/{self.config['service_name']} (usuario: {self.config['user']})"

        except Exception as e:
            return f"❌ Error de conexión: {str(e)}"

    def ejecutar_query(self, query: str, params=None):
        """Ejecuta una query de solo lectura y retorna resultados."""
        try:
            if not self.connection:
                return "❌ No hay conexión activa. Usa ConectarOracle primero."

            # SEGURIDAD: Verificar que la query es de solo lectura
            query_upper = query.strip().upper()
            comandos_prohibidos = [
                'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE',
                'ALTER', 'TRUNCATE', 'GRANT', 'REVOKE', 'COMMIT', 'ROLLBACK'
            ]

            for cmd in comandos_prohibidos:
                if cmd in query_upper.split():
                    return f"🚫 PROHIBIDO: Comando '{cmd}' no permitido. Solo lectura."

            cursor = self.connection.cursor()

            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            # Obtener nombres de columnas
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                cursor.close()

                return {
                    'columns': columns,
                    'rows': rows,
                    'count': len(rows)
                }
            else:
                cursor.close()
                return {'columns': [], 'rows': [], 'count': 0}

        except Exception as e:
            return f"❌ Error en query: {str(e)}"

    def cerrar(self):
        """Cierra la conexión a Oracle."""
        if self.connection:
            self.connection.close()
            self.connection = None
            return "✅ Conexión cerrada"
        return "ℹ️  No había conexión activa"


# Instancia global de conexión
oracle_conn = OracleConnection()


# ============================================================================
# HERRAMIENTAS DEL AGENTE (SOLO LECTURA)
# ============================================================================

def conectar_oracle(entrada: str) -> str:
    """
    Establece conexión con la base de datos Oracle.
    Args:
        entrada: No se usa (requerido por interfaz)
    Returns:
        Mensaje de éxito o error
    """
    return oracle_conn.conectar()


def listar_tablas(entrada: str) -> str:
    """
    Lista todas las tablas del usuario en Oracle.
    Args:
        entrada: Filtro opcional (ej: "USER%" para tablas que empiecen con USER)
    Returns:
        Lista de tablas con información básica
    """
    query = """
        SELECT
            table_name,
            tablespace_name,
            num_rows,
            CASE
                WHEN temporary = 'Y' THEN 'TEMPORAL'
                ELSE 'PERMANENTE'
            END as tipo
        FROM user_tables
        ORDER BY table_name
    """

    resultado = oracle_conn.ejecutar_query(query)

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return "ℹ️  No se encontraron tablas"

    # Formatear salida
    output = f"📊 Encontradas {resultado['count']} tablas:\n\n"
    output += f"{'Tabla':<30} {'Tablespace':<20} {'Filas':<10} {'Tipo'}\n"
    output += "=" * 80 + "\n"

    for row in resultado['rows']:
        table_name, tablespace, num_rows, tipo = row
        num_rows_str = str(num_rows) if num_rows else 'N/A'
        output += f"{table_name:<30} {tablespace or 'N/A':<20} {num_rows_str:<10} {tipo}\n"

    return output


def describir_tabla(nombre_tabla: str) -> str:
    """
    Describe la estructura completa de una tabla.
    Args:
        nombre_tabla: Nombre de la tabla a describir
    Returns:
        Estructura detallada de la tabla
    """
    nombre_tabla = nombre_tabla.strip().upper()

    # Query para obtener columnas
    query = """
        SELECT
            column_name,
            data_type,
            data_length,
            data_precision,
            data_scale,
            nullable,
            data_default
        FROM user_tab_columns
        WHERE table_name = :tabla
        ORDER BY column_id
    """

    resultado = oracle_conn.ejecutar_query(query, {'tabla': nombre_tabla})

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return f"❌ Tabla '{nombre_tabla}' no encontrada"

    # Formatear salida
    output = f"🔍 Estructura de {nombre_tabla}:\n\n"
    output += f"{'Columna':<30} {'Tipo':<20} {'Nullable':<10} {'Default'}\n"
    output += "=" * 80 + "\n"

    for row in resultado['rows']:
        col_name, data_type, length, precision, scale, nullable, default = row

        # Formatear tipo de dato
        if data_type in ['NUMBER']:
            if precision:
                tipo = f"{data_type}({precision},{scale or 0})"
            else:
                tipo = data_type
        elif data_type in ['VARCHAR2', 'CHAR']:
            tipo = f"{data_type}({length})"
        else:
            tipo = data_type

        nullable_str = 'SÍ' if nullable == 'Y' else 'NO'
        default_str = str(default)[:20] if default else '-'

        output += f"{col_name:<30} {tipo:<20} {nullable_str:<10} {default_str}\n"

    return output


def obtener_relaciones(entrada: str = "") -> str:
    """
    Obtiene las relaciones (Foreign Keys) de las tablas.
    Args:
        entrada: Nombre de tabla opcional (vacío = todas las relaciones)
    Returns:
        Lista de Foreign Keys
    """
    if entrada.strip():
        tabla = entrada.strip().upper()
        query = """
            SELECT
                a.constraint_name,
                a.table_name,
                a.column_name,
                c_pk.table_name as tabla_referenciada,
                b.column_name as columna_referenciada
            FROM user_cons_columns a
            JOIN user_constraints c ON a.constraint_name = c.constraint_name
            JOIN user_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
            JOIN user_cons_columns b ON c_pk.constraint_name = b.constraint_name
            WHERE c.constraint_type = 'R'
            AND a.table_name = :tabla
            ORDER BY a.table_name, a.constraint_name
        """
        resultado = oracle_conn.ejecutar_query(query, {'tabla': tabla})
    else:
        query = """
            SELECT
                a.constraint_name,
                a.table_name,
                a.column_name,
                c_pk.table_name as tabla_referenciada,
                b.column_name as columna_referenciada
            FROM user_cons_columns a
            JOIN user_constraints c ON a.constraint_name = c.constraint_name
            JOIN user_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
            JOIN user_cons_columns b ON c_pk.constraint_name = b.constraint_name
            WHERE c.constraint_type = 'R'
            ORDER BY a.table_name, a.constraint_name
        """
        resultado = oracle_conn.ejecutar_query(query)

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return "ℹ️  No se encontraron relaciones (Foreign Keys)"

    # Formatear salida
    output = f"🔗 Encontradas {resultado['count']} relaciones:\n\n"

    for row in resultado['rows']:
        fk_name, tabla, columna, tabla_ref, col_ref = row
        output += f"  {tabla}.{columna} → {tabla_ref}.{col_ref}\n"
        output += f"  (FK: {fk_name})\n\n"

    return output


def obtener_indices(nombre_tabla: str) -> str:
    """
    Lista los índices de una tabla.
    Args:
        nombre_tabla: Nombre de la tabla
    Returns:
        Lista de índices con sus columnas
    """
    nombre_tabla = nombre_tabla.strip().upper()

    query = """
        SELECT
            i.index_name,
            i.index_type,
            i.uniqueness,
            LISTAGG(ic.column_name, ', ') WITHIN GROUP (ORDER BY ic.column_position) as columnas
        FROM user_indexes i
        LEFT JOIN user_ind_columns ic ON i.index_name = ic.index_name
        WHERE i.table_name = :tabla
        GROUP BY i.index_name, i.index_type, i.uniqueness
        ORDER BY i.index_name
    """

    resultado = oracle_conn.ejecutar_query(query, {'tabla': nombre_tabla})

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return f"ℹ️  No se encontraron índices para {nombre_tabla}"

    # Formatear salida
    output = f"📇 Índices de {nombre_tabla}:\n\n"

    for row in resultado['rows']:
        idx_name, idx_type, uniqueness, columnas = row
        unique_str = '✓ UNIQUE' if uniqueness == 'UNIQUE' else '  Normal'
        output += f"  {unique_str} - {idx_name} ({idx_type})\n"
        output += f"    Columnas: {columnas}\n\n"

    return output


def generar_diagrama_er(entrada: str = "") -> str:
    """
    Genera un diagrama ER en formato Mermaid.
    Args:
        entrada: Lista de tablas separadas por comas (opcional, vacío = todas)
    Returns:
        Código Mermaid con el diagrama ER
    """
    # Obtener relaciones
    query_fk = """
        SELECT
            a.table_name,
            a.column_name,
            c_pk.table_name as tabla_referenciada,
            b.column_name as columna_referenciada
        FROM user_cons_columns a
        JOIN user_constraints c ON a.constraint_name = c.constraint_name
        JOIN user_constraints c_pk ON c.r_constraint_name = c_pk.constraint_name
        JOIN user_cons_columns b ON c_pk.constraint_name = b.constraint_name
        WHERE c.constraint_type = 'R'
        ORDER BY a.table_name
    """

    resultado = oracle_conn.ejecutar_query(query_fk)

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return "ℹ️  No se encontraron relaciones para generar diagrama"

    # Generar código Mermaid
    output = "```mermaid\nerDiagram\n"

    # Mapear relaciones
    relaciones_procesadas = set()

    for row in resultado['rows']:
        tabla, columna, tabla_ref, col_ref = row

        relacion_key = f"{tabla}-{tabla_ref}"
        if relacion_key not in relaciones_procesadas:
            output += f"    {tabla} ||--o{{ {tabla_ref} : \"referencia\"\n"
            relaciones_procesadas.add(relacion_key)

    output += "```\n\n"
    output += f"📈 Diagrama generado con {len(relaciones_procesadas)} relaciones"

    return output


def consultar_metadata(tipo_consulta: str) -> str:
    """
    Consulta metadata específica del diccionario de Oracle.
    Args:
        tipo_consulta: Tipo de metadata (vistas, secuencias, triggers, etc.)
    Returns:
        Información de metadata solicitada
    """
    tipo = tipo_consulta.strip().lower()

    queries = {
        'vistas': "SELECT view_name, text_length FROM user_views ORDER BY view_name",
        'secuencias': "SELECT sequence_name, min_value, max_value, increment_by, last_number FROM user_sequences ORDER BY sequence_name",
        'triggers': "SELECT trigger_name, trigger_type, triggering_event, table_name, status FROM user_triggers ORDER BY trigger_name",
        'procedimientos': "SELECT object_name, object_type, status FROM user_objects WHERE object_type IN ('PROCEDURE', 'FUNCTION', 'PACKAGE') ORDER BY object_name"
    }

    if tipo not in queries:
        return f"❌ Tipo '{tipo}' no reconocido. Opciones: {', '.join(queries.keys())}"

    resultado = oracle_conn.ejecutar_query(queries[tipo])

    if isinstance(resultado, str):
        return resultado

    if resultado['count'] == 0:
        return f"ℹ️  No se encontraron {tipo}"

    # Formatear salida
    output = f"📋 {tipo.upper()} encontrados: {resultado['count']}\n\n"

    # Crear tabla
    headers = resultado['columns']
    output += " | ".join(f"{h:<25}" for h in headers) + "\n"
    output += "-" * (25 * len(headers) + (len(headers) - 1) * 3) + "\n"

    for row in resultado['rows']:
        output += " | ".join(f"{str(v or 'N/A'):<25}" for v in row) + "\n"

    return output


# ============================================================================
# CONFIGURACIÓN DEL AGENTE
# ============================================================================

def crear_agente():
    """
    Crea y configura el agente Oracle con Ollama y sus herramientas.
    Returns:
        AgentExecutor configurado y listo para usar
    """

    # 1. Inicializar el modelo local de Ollama
    print("🔧 Inicializando modelo Ollama...")
    llm = Ollama(
        model="qwen3:4b",  # Modelo Qwen más rápido
        temperature=0.3,  # Baja temperatura para respuestas más precisas
    )

    # 2. Definir las herramientas disponibles (SOLO LECTURA)
    herramientas = [
        Tool(
            name="ConectarOracle",
            func=conectar_oracle,
            description="Conecta a la base de datos Oracle. Usar al inicio de la sesión."
        ),
        Tool(
            name="ListarTablas",
            func=listar_tablas,
            description="Lista todas las tablas del usuario con información básica (nombre, filas, tipo)."
        ),
        Tool(
            name="DescribirTabla",
            func=describir_tabla,
            description="Describe la estructura de una tabla específica. Entrada: nombre de la tabla."
        ),
        Tool(
            name="ObtenerRelaciones",
            func=obtener_relaciones,
            description="Obtiene las Foreign Keys y relaciones entre tablas. Entrada: nombre de tabla (opcional)."
        ),
        Tool(
            name="ObtenerIndices",
            func=obtener_indices,
            description="Lista los índices de una tabla. Entrada: nombre de la tabla."
        ),
        Tool(
            name="GenerarDiagramaER",
            func=generar_diagrama_er,
            description="Genera un diagrama ER en formato Mermaid. Entrada: lista de tablas (opcional)."
        ),
        Tool(
            name="ConsultarMetadata",
            func=consultar_metadata,
            description="Consulta metadata del diccionario Oracle. Entrada: tipo (vistas, secuencias, triggers, procedimientos)."
        )
    ]

    # 3. Crear el prompt template (simplificado para mejor rendimiento)
    template = """Eres un analista experto de bases de datos Oracle. Solo puedes LEER datos, NUNCA modificar.

Tienes estas herramientas:
{tools}

Herramientas disponibles: {tool_names}

Formato de respuesta:

Pregunta: la pregunta
Pensamiento: qué hacer
Acción: herramienta a usar [{tool_names}]
Entrada de Acción: parámetros
Observación: resultado
... (repetir si necesario)
Pensamiento: tengo la respuesta
Respuesta Final: respuesta clara

Historial: {chat_history}

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
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=8
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
    print("🗄️  AGENTE ANALISTA DE ORACLE (SOLO LECTURA)")
    print("=" * 70)
    print("\nCapacidades del agente:")
    print("  🔌 Conectar a base de datos Oracle")
    print("  📊 Listar tablas y estructuras")
    print("  🔍 Describir tablas en detalle")
    print("  🔗 Analizar relaciones (Foreign Keys)")
    print("  📇 Ver índices y constraints")
    print("  📈 Generar diagramas ER (Mermaid)")
    print("  📋 Consultar metadata del diccionario")
    print("\n⚠️  MODO SOLO LECTURA - No se pueden modificar datos")
    print("\nEscribe 'salir' o 'exit' para terminar\n")
    print("=" * 70 + "\n")

    # Verificar configuración
    print("🔍 Verificando configuración...")
    config = oracle_conn.cargar_configuracion()

    if not config:
        print("\n⚠️  No se encontró archivo de configuración.")
        print("Ejecuta primero: python SCRIPTS/configurar_oracle.py")
        print("\nO crea manualmente UTILS/config_oracle.py con la estructura:")
        print("""
ORACLE_CONFIG = {
    'host': 'tu_host',
    'port': 1521,
    'service_name': 'tu_servicio',
    'user': 'tu_usuario',
    'password': 'tu_password'
}
        """)
        return

    print(f"✅ Configuración encontrada: {config['user']}@{config['host']}")

    # Crear el agente
    try:
        agente = crear_agente()
        print("✅ Agente inicializado correctamente\n")
    except Exception as e:
        print(f"❌ Error al inicializar el agente: {e}")
        print("\n⚠️  Asegúrate de que Ollama está ejecutándose:")
        print("   ollama serve")
        print("   ollama pull qwen3:4b")
        return

    # Loop de conversación
    while True:
        try:
            # Obtener entrada del usuario
            pregunta = input("👤 Tú: ").strip()

            # Verificar si quiere salir
            if pregunta.lower() in ['salir', 'exit', 'quit']:
                oracle_conn.cerrar()
                print("\n👋 ¡Hasta luego!")
                break

            # Verificar que no esté vacío
            if not pregunta:
                continue

            # Ejecutar el agente
            print("\n🤖 Agente:")
            respuesta = agente.invoke({"input": pregunta})

            # Mostrar la respuesta final
            print("\n" + "=" * 70)
            print(f"📤 Respuesta:\n{respuesta['output']}")
            print("=" * 70 + "\n")

        except KeyboardInterrupt:
            oracle_conn.cerrar()
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")


if __name__ == "__main__":
    main()
