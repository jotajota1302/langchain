# 🤖 Guía Completa: Agentes con LangChain + Ollama

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [¿Qué son los Agentes?](#qué-son-los-agentes)
4. [Componentes de un Agente](#componentes-de-un-agente)
5. [Tipos de Agentes](#tipos-de-agentes)
6. [Cómo Funcionan los Agentes](#cómo-funcionan-los-agentes)
7. [Herramientas (Tools)](#herramientas-tools)
8. [Memoria en Agentes](#memoria-en-agentes)
9. [Ejemplo Práctico](#ejemplo-práctico)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Los **agentes** en LangChain son sistemas inteligentes que pueden:
- 🧠 **Razonar** sobre qué acciones tomar
- 🛠️ **Usar herramientas** para completar tareas
- 🔄 **Iterar** hasta encontrar la respuesta correcta
- 💭 **Mantener memoria** de conversaciones anteriores

A diferencia de una simple llamada a un LLM, los agentes pueden decidir dinámicamente qué herramientas usar y en qué orden, basándose en el input del usuario.

---

## 🔧 Instalación y Configuración

### Paso 1: Instalar Ollama

**En Windows:**
```bash
# Descarga el instalador desde https://ollama.com/download
# O usa winget:
winget install Ollama.Ollama
```

**En Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### Paso 2: Descargar un Modelo

```bash
# Iniciar Ollama (si no está ejecutándose)
ollama serve

# En otra terminal, descargar un modelo
ollama pull llama2          # Modelo general (3.8GB)
# o
ollama pull mistral         # Alternativa más ligera (4.1GB)
# o
ollama pull llama3.2        # Último modelo de Meta (2GB)
```

### Paso 3: Instalar Dependencias de Python

```bash
# Crear un entorno virtual (recomendado)
python -m venv venv

# Activar el entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### Paso 4: Verificar la Instalación

```bash
# Verificar que Ollama está corriendo
ollama list  # Debe mostrar los modelos descargados

# Probar Ollama
ollama run llama2 "Hola, ¿cómo estás?"
```

---

## 🤔 ¿Qué son los Agentes?

Un **agente** es un sistema que usa un LLM como motor de razonamiento para decidir qué acciones tomar y en qué orden.

### Diferencia: Chain vs Agent

| Característica | Chain | Agent |
|----------------|-------|-------|
| **Flujo** | Predefinido y fijo | Dinámico y adaptativo |
| **Decisiones** | No toma decisiones | Decide qué hacer en cada paso |
| **Herramientas** | Usa todas en orden fijo | Elige qué herramientas usar |
| **Iteraciones** | Un solo paso | Múltiples iteraciones |

**Ejemplo de Chain:**
```
Usuario → LLM → Búsqueda Web → LLM → Respuesta
(siempre el mismo flujo)
```

**Ejemplo de Agent:**
```
Usuario: "¿Cuánto es 25°C en Fahrenheit multiplicado por 2?"

Agente piensa → Usa ConvertidorTemperatura (25C)
             → Observa resultado: 77°F
             → Usa Calculadora (77*2)
             → Observa resultado: 154
             → Responde: "154"
```

---

## 🧩 Componentes de un Agente

### 1. **LLM (Large Language Model)**
El cerebro del agente. Razona sobre qué hacer.

```python
from langchain_community.llms import Ollama

llm = Ollama(
    model="llama2",
    temperature=0.7  # Creatividad (0=determinista, 1=creativo)
)
```

### 2. **Herramientas (Tools)**
Capacidades que el agente puede usar.

```python
from langchain.agents import Tool

tool = Tool(
    name="Calculadora",
    func=calculadora,  # Función Python
    description="Para hacer cálculos matemáticos"
)
```

### 3. **Prompt Template**
Instrucciones de cómo debe razonar el agente.

```python
template = """Responde usando este formato:
Pregunta: {input}
Pensamiento: [qué debo hacer]
Acción: [herramienta a usar]
Observación: [resultado]
Respuesta Final: [respuesta]"""
```

### 4. **Memoria (Opcional)**
Recordar conversaciones anteriores.

```python
from langchain.memory import ConversationBufferMemory

memoria = ConversationBufferMemory(
    memory_key="chat_history"
)
```

### 5. **Agent Executor**
Orquestador que ejecuta el ciclo del agente.

```python
from langchain.agents import AgentExecutor

executor = AgentExecutor(
    agent=agente,
    tools=herramientas,
    verbose=True  # Ver el proceso de razonamiento
)
```

---

## 🎭 Tipos de Agentes

### 1. **ReAct Agent** (Recomendado)
- **Patrón:** Reasoning + Acting
- **Ciclo:** Pensamiento → Acción → Observación → Repetir
- **Uso:** Tareas generales con múltiples herramientas

```python
from langchain.agents import create_react_agent

agente = create_react_agent(llm, tools, prompt)
```

### 2. **Zero-shot ReAct**
- Similar a ReAct pero sin ejemplos previos
- Más simple, menos contexto

### 3. **Conversational Agent**
- Optimizado para conversaciones
- Mantiene mejor el contexto del chat

### 4. **Structured Chat Agent**
- Para herramientas con inputs complejos (JSON, etc.)

### 5. **OpenAI Functions Agent**
- Usa function calling de OpenAI
- No compatible con Ollama (requiere OpenAI API)

---

## ⚙️ Cómo Funcionan los Agentes

### Ciclo de Ejecución (ReAct Pattern)

```
┌─────────────────────────────────────────┐
│  1. USUARIO: "¿Cuánto es 15 * 8?"      │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  2. AGENTE PIENSA:                       │
│     "Necesito calcular 15 * 8"           │
│     "Tengo una herramienta Calculadora"  │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  3. AGENTE DECIDE:                       │
│     Acción: Calculadora                  │
│     Input: "15 * 8"                      │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  4. EJECUTA HERRAMIENTA:                 │
│     calculadora("15 * 8")                │
│     → Resultado: 120                     │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  5. OBSERVACIÓN:                         │
│     "El resultado es 120"                │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  6. AGENTE PIENSA:                       │
│     "Ya tengo la respuesta"              │
│     "No necesito más herramientas"       │
└──────────────┬───────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  7. RESPUESTA FINAL:                     │
│     "15 multiplicado por 8 es 120"       │
└──────────────────────────────────────────┘
```

### Ejemplo de Salida Verbose

Cuando ejecutas con `verbose=True`, ves:

```
> Entering new AgentExecutor chain...
Pregunta: ¿Cuánto es 15 * 8?
Pensamiento: Necesito hacer un cálculo matemático
Acción: Calculadora
Entrada de Acción: 15 * 8
Observación: El resultado es: 120
Pensamiento: Ahora sé la respuesta final
Respuesta Final: 15 multiplicado por 8 es 120

> Finished chain.
```

---

## 🛠️ Herramientas (Tools)

### Anatomía de una Herramienta

```python
from langchain.agents import Tool

def mi_funcion(input_texto: str) -> str:
    """Descripción de lo que hace la función"""
    # Lógica aquí
    return "resultado"

herramienta = Tool(
    name="NombreCorto",  # Sin espacios, camelCase
    func=mi_funcion,     # La función Python
    description="Descripción CLARA de cuándo usarla"  # ¡MUY IMPORTANTE!
)
```

### ⚠️ La Descripción es CRÍTICA

El agente decide qué herramienta usar basándose **solo en la descripción**. Debe ser:
- ✅ Clara y específica
- ✅ Indicar qué tipo de input espera
- ✅ Indicar qué devuelve
- ❌ No ambigua
- ❌ No vaga

**Ejemplo MALO:**
```python
description="Una herramienta útil"  # 🚫 Demasiado vaga
```

**Ejemplo BUENO:**
```python
description="Convierte temperaturas entre Celsius y Fahrenheit. Input: '25C' o '77F'"  # ✅
```

### Tipos de Herramientas Comunes

#### 1. Herramientas de Cálculo
```python
def calculadora(expresion: str) -> str:
    resultado = eval(expresion)  # ⚠️ Sanitizar en producción!
    return str(resultado)
```

#### 2. Herramientas de Búsqueda
```python
from langchain.tools import DuckDuckGoSearchRun

search = DuckDuckGoSearchRun()
```

#### 3. Herramientas de Base de Datos
```python
from langchain.tools import QuerySQLDataBaseTool

db_tool = QuerySQLDataBaseTool(db=db)
```

#### 4. Herramientas Personalizadas
```python
@tool
def obtener_clima(ciudad: str) -> str:
    """Obtiene el clima actual de una ciudad"""
    # Llamada a API del clima
    return f"Clima en {ciudad}: 22°C, soleado"
```

---

## 💾 Memoria en Agentes

### Tipos de Memoria

#### 1. **ConversationBufferMemory**
Guarda todo el historial.

```python
from langchain.memory import ConversationBufferMemory

memoria = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

**Ventajas:** Contexto completo
**Desventajas:** Crece indefinidamente

#### 2. **ConversationBufferWindowMemory**
Solo las últimas N interacciones.

```python
from langchain.memory import ConversationBufferWindowMemory

memoria = ConversationBufferWindowMemory(
    k=5,  # Últimas 5 interacciones
    memory_key="chat_history"
)
```

**Ventajas:** Tamaño limitado
**Desventajas:** Pierde contexto antiguo

#### 3. **ConversationSummaryMemory**
Resume conversaciones antiguas.

```python
from langchain.memory import ConversationSummaryMemory

memoria = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history"
)
```

**Ventajas:** Mantiene contexto sin crecer mucho
**Desventajas:** Requiere llamadas extra al LLM

---

## 📝 Ejemplo Práctico

### Caso de Uso: Asistente de Análisis de Datos

```python
from langchain_community.llms import Ollama
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
import pandas as pd

# 1. Herramienta para leer CSV
def leer_csv(archivo: str) -> str:
    """Lee un archivo CSV y devuelve info básica"""
    df = pd.read_csv(archivo)
    return f"Filas: {len(df)}, Columnas: {list(df.columns)}"

# 2. Herramienta para estadísticas
def estadisticas(columna: str) -> str:
    """Calcula estadísticas de una columna"""
    # Asumiendo df global
    stats = df[columna].describe()
    return str(stats)

# 3. Crear herramientas
tools = [
    Tool(name="LeerCSV", func=leer_csv,
         description="Lee CSV. Input: ruta del archivo"),
    Tool(name="Stats", func=estadisticas,
         description="Estadísticas de columna. Input: nombre columna")
]

# 4. Configurar agente
llm = Ollama(model="llama2")
prompt = PromptTemplate(...)  # Template ReAct
agente = create_react_agent(llm, tools, prompt)
executor = AgentExecutor(agent=agente, tools=tools, verbose=True)

# 5. Usar
executor.invoke({"input": "Analiza el archivo ventas.csv"})
```

---

## 🐛 Troubleshooting

### ❌ Error: "Connection refused"

**Problema:** Ollama no está ejecutándose.

**Solución:**
```bash
ollama serve
```

### ❌ Error: "Model not found"

**Problema:** El modelo no está descargado.

**Solución:**
```bash
ollama pull llama2
```

### ❌ El agente no usa las herramientas correctamente

**Problema:** Descripción de herramientas poco clara.

**Solución:**
- Mejorar las descripciones
- Añadir ejemplos de input en la descripción
- Usar un modelo más potente (llama3 > llama2)

### ❌ El agente entra en bucle infinito

**Problema:** No puede decidir qué hacer.

**Solución:**
```python
AgentExecutor(
    agent=agente,
    tools=tools,
    max_iterations=5,  # Limitar iteraciones
    handle_parsing_errors=True  # Manejar errores de parsing
)
```

### ❌ Respuestas muy lentas

**Problema:** Ollama procesando en CPU.

**Solución:**
- Usar un modelo más pequeño (llama3.2 en lugar de llama2)
- Si tienes GPU NVIDIA, Ollama la usará automáticamente
- Reducir `max_iterations`

---

## 🚀 Mejores Prácticas

### 1. Diseño de Herramientas
- ✅ Una herramienta = una responsabilidad
- ✅ Descripciones ultra-claras
- ✅ Manejo de errores robusto
- ✅ Validación de inputs

### 2. Prompts
- ✅ Usar ejemplos en el prompt (few-shot)
- ✅ Ser explícito sobre el formato esperado
- ✅ Indicar cuándo responder directamente vs usar herramientas

### 3. Optimización
- ✅ Limitar `max_iterations` (evitar bucles infinitos)
- ✅ Usar `verbose=True` durante desarrollo
- ✅ Cachear resultados cuando sea posible
- ✅ Usar memoria window en lugar de buffer completo

### 4. Seguridad
- ⚠️ NUNCA uses `eval()` sin sanitizar
- ⚠️ Valida inputs de usuario
- ⚠️ Limita recursos (tiempo, memoria)
- ⚠️ No expongas información sensible en las descripciones

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [Ollama](https://ollama.com/)

### Modelos Recomendados para Agentes
- **llama3.2** (2GB) - Más reciente, buen balance
- **mistral** (4.1GB) - Muy bueno para razonamiento
- **llama2** (3.8GB) - Clásico, estable
- **codellama** (3.8GB) - Para tareas de código

### Comandos Útiles de Ollama
```bash
ollama list                    # Listar modelos instalados
ollama pull <modelo>           # Descargar modelo
ollama rm <modelo>             # Eliminar modelo
ollama show <modelo>           # Info del modelo
ollama run <modelo> "prompt"   # Probar modelo
```

---

## 🎓 Ejercicios Propuestos

1. **Básico:** Añade una herramienta que calcule el IMC (peso/altura²)

2. **Intermedio:** Crea un agente que pueda leer archivos, buscar palabras y contar ocurrencias

3. **Avanzado:** Implementa un agente con acceso a SQLite que pueda crear tablas, insertar datos y hacer queries

---

## 📞 Soporte

Si tienes problemas:
1. Revisa que Ollama esté ejecutándose: `ollama list`
2. Verifica las versiones: `pip list | grep langchain`
3. Prueba con `verbose=True` para ver qué está pasando
4. Revisa los logs de Ollama

---

**¡Buena suerte creando agentes! 🚀**
