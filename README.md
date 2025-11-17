# 🤖 Agentes LangChain + Ollama

Este proyecto contiene **dos agentes inteligentes** construidos con LangChain que utilizan modelos locales a través de Ollama:

1. **Agente de Ejemplo** (`agente_ollama.py`) - Demostración básica con herramientas útiles
2. **Agente de Estimación** (`agente_estimacion.py`) - Sistema profesional para estimar proyectos de desarrollo

## 🚀 Inicio Rápido

### 1. Instalar Ollama

**Windows:**
```bash
winget install Ollama.Ollama
```

**Linux/Mac:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Descargar un Modelo

```bash
# Iniciar Ollama
ollama serve

# En otra terminal, descargar el modelo
ollama pull llama2
```

### 3. Instalar Dependencias de Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac

# Para el agente de ejemplo:
pip install -r UTILS/requirements.txt

# Para el agente de estimación (incluye todo):
pip install -r UTILS/requirements_estimacion.txt
```

### 4. Ejecutar los Agentes

```bash
# Agente de ejemplo
python AGENTS/agente_ollama.py

# Agente de estimación
python AGENTS/agente_estimacion.py

# Ejemplos programáticos de estimación
python SCRIPTS/ejemplo_estimacion.py
```

## 📁 Estructura del Proyecto

```
LANGCHAIN/
├── AGENTS/                               # 🤖 Agentes inteligentes
│   ├── agente_ollama.py                  #   → Agente de ejemplo (básico)
│   └── agente_estimacion.py              #   → Agente de estimación profesional
│
├── PROMPTS/                              # 📝 Prompts de los agentes
│   └── agente-estimacion-desarrollo.md   #   → Prompt experto de estimación
│
├── SCRIPTS/                              # 🔧 Scripts de ejemplo y utilidades
│   ├── ejemplo_estimacion.py             #   → Ejemplos de uso del agente
│   └── procesar_gestic_rd.py             #   → Procesamiento de documentos GESTIC
│
├── INPUT/                                # 📥 Archivos de entrada
│   ├── GESTIC-XXXXXX Proyecto - Descripción.xlsx  # Plantilla Excel GESTIC
│   └── *.docx, *.pdf                     #   → Diseños técnicos a procesar
│
├── OUTPUT/                               # 📤 Resultados generados
│   └── estimacion_*.xlsx                 #   → Estimaciones generadas
│
├── DOC/                                  # 📚 Documentación
│   ├── GUIA_AGENTES_LANGCHAIN.md         #   → Guía completa de agentes
│   └── GUIA_AGENTE_ESTIMACION.md         #   → Guía del agente de estimación
│
├── UTILS/                                # 🛠️ Utilidades y dependencias
│   ├── requirements.txt                  #   → Dependencias básicas
│   ├── requirements_estimacion.txt       #   → Dependencias para estimación
│   └── texto_extraido.txt                #   → Textos extraídos temporales
│
└── README.md                             # Este archivo
```

### 📋 Descripción de Carpetas

| Carpeta | Propósito | Contenido |
|---------|-----------|-----------|
| **AGENTS/** | Agentes LangChain | Archivos `.py` con la lógica de los agentes inteligentes |
| **PROMPTS/** | Prompts del sistema | Archivos `.md` con los prompts y configuraciones de los agentes |
| **SCRIPTS/** | Scripts de ejemplo | Scripts `.py` para ejecutar ejemplos y procesamiento de datos |
| **INPUT/** | Archivos de entrada | Documentos `.docx`, `.pdf`, plantillas `.xlsx` para procesar |
| **OUTPUT/** | Resultados generados | Archivos `.xlsx`, `.json` u otros outputs generados |
| **DOC/** | Documentación | Guías, manuales y documentación del proyecto |
| **UTILS/** | Utilidades | `requirements.txt`, configuraciones, archivos temporales |

## 🛠️ Capacidades de los Agentes

### Agente de Ejemplo (`agente_ollama.py`)

Herramientas básicas para demostración:
- **📊 Calculadora**: Realiza cálculos matemáticos
- **🕐 Fecha/Hora**: Obtiene la fecha y hora actual
- **🌡️ Convertidor de Temperatura**: Convierte entre Celsius y Fahrenheit
- **📝 Analizador de Texto**: Proporciona estadísticas de textos

### Agente de Estimación (`agente_estimacion.py`) ⭐

Sistema profesional de estimación de proyectos:
- **📄 LeerPDF**: Extrae contenido de diseños técnicos en PDF
- **📄 LeerWord**: Extrae contenido de documentos Word (.docx)
- **🔍 ExtraerComponentes**: Detecta automáticamente modelos, servicios, componentes
- **➕ AgregarComponente**: Permite agregar componentes manualmente
- **🧮 CalcularEstimacion**: Aplica ponderaciones GESTIC y factores de ajuste
- **📊 ExportarExcel**: Genera estimación en plantilla Excel GESTIC

## 💬 Ejemplos de Uso

### Agente de Ejemplo

```bash
python AGENTS/agente_ollama.py
```

Preguntas de ejemplo:
```
¿Cuánto es 15 * 8?
¿Qué hora es?
Convierte 25C a Fahrenheit
Analiza este texto: "LangChain es increíble"
```

### Agente de Estimación

```bash
# Modo interactivo
python AGENTS/agente_estimacion.py

# Modo programático (ejemplos)
python SCRIPTS/ejemplo_estimacion.py 1  # Estimación manual completa
python SCRIPTS/ejemplo_estimacion.py 2  # Estimación rápida
python SCRIPTS/ejemplo_estimacion.py 3  # Comparación de escenarios
```

Ejemplo de conversación:
```
👤 Tú: Lee el archivo INPUT/GESTIC-833509_Diseno_Tecnico_Detalle_RD_v2.docx
🤖 Agente: [Lee y extrae contenido]

👤 Tú: Extrae los componentes técnicos del diseño
🤖 Agente: Detectados: 5 modelos, 3 servicios, 8 componentes...

👤 Tú: Agrega Servicio|EmailService|3|10|0|5|8
🤖 Agente: ✅ Componente agregado

👤 Tú: Calcula estimación con Media|Si|Mid
🤖 Agente: Total: 456 horas (distribución por fases...)

👤 Tú: Exporta a estimacion_crm.xlsx
🤖 Agente: ✅ Excel generado en OUTPUT/estimacion_crm.xlsx
```

## 📚 Documentación

### Guías Disponibles

**1. [GUIA_AGENTES_LANGCHAIN.md](DOC/GUIA_AGENTES_LANGCHAIN.md)** - Fundamentos de Agentes
- Conceptos fundamentales de agentes
- Tipos de agentes y cuándo usar cada uno
- Cómo crear herramientas personalizadas
- Gestión de memoria
- Troubleshooting
- Mejores prácticas

**2. [GUIA_AGENTE_ESTIMACION.md](DOC/GUIA_AGENTE_ESTIMACION.md)** - Agente de Estimación ⭐
- Instalación y configuración
- Arquitectura del agente
- Herramientas disponibles
- Flujo de trabajo completo
- Ejemplos prácticos
- Estructura del Excel GESTIC
- Personalización y troubleshooting

**3. [agente-estimacion-desarrollo.md](PROMPTS/agente-estimacion-desarrollo.md)** - Prompt Experto
- Criterios de estimación profesional
- Métricas de referencia por tecnología
- Factores multiplicadores
- Formato de salida detallado

## 🔧 Configuración

### Cambiar el Modelo

Edita `AGENTS/agente_ollama.py` y modifica esta línea:

```python
llm = Ollama(
    model="llama2",  # Cambia a "mistral", "llama3.2", etc.
    temperature=0.7
)
```

### Modelos Disponibles

```bash
# Ver modelos instalados
ollama list

# Descargar otros modelos
ollama pull mistral
ollama pull llama3.2
ollama pull codellama
```

## ⚠️ Troubleshooting

### Error: "Connection refused"
Asegúrate de que Ollama está ejecutándose:
```bash
ollama serve
```

### El agente no responde correctamente
Prueba con un modelo más potente:
```bash
ollama pull mistral
```

### Errores de importación
Reinstala las dependencias:
```bash
pip install -r UTILS/requirements.txt --upgrade
```

## 🎯 Próximos Pasos

1. Lee la [GUIA_AGENTES_LANGCHAIN.md](DOC/GUIA_AGENTES_LANGCHAIN.md) completa
2. Experimenta añadiendo tus propias herramientas en `AGENTS/`
3. Prueba diferentes modelos de Ollama
4. Implementa memoria para conversaciones más largas
5. Coloca tus diseños técnicos en `INPUT/` y procésalos con el agente de estimación

## 📝 Notas Importantes

- **Organización**: El proyecto está estructurado para facilitar la navegación y escalabilidad
- **INPUT/OUTPUT**: Los archivos de entrada van en `INPUT/`, los resultados se generan en `OUTPUT/`
- **Offline**: El agente funciona completamente offline (modelo local)
- **Sin API Key**: No se requiere API key ni conexión a internet
- **Extensible**: Agrega nuevos agentes en `AGENTS/`, nuevos prompts en `PROMPTS/`

## 🗂️ Buenas Prácticas de Organización

1. **INPUT/**: Coloca aquí todos los documentos que vayas a procesar (.docx, .pdf, .xlsx)
2. **OUTPUT/**: Todos los resultados generados se guardarán aquí automáticamente
3. **SCRIPTS/**: Scripts de prueba y ejemplos de uso programático
4. **AGENTS/**: Solo código de agentes, mantén la lógica separada
5. **PROMPTS/**: Guarda tus prompts en archivos .md para reutilizarlos
6. **DOC/**: Documenta todo cambio importante o nueva funcionalidad

---

**¿Necesitas ayuda?** Consulta la guía completa en [GUIA_AGENTES_LANGCHAIN.md](DOC/GUIA_AGENTES_LANGCHAIN.md)
