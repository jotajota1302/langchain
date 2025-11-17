# CLAUDE.md - Contexto del Proyecto

## Objetivo del Proyecto

Sistema de **agentes inteligentes con LangChain + Ollama** para automatizar estimaciones de desarrollo de software. Procesa documentos técnicos (PDF/Word) y genera estimaciones profesionales en formato Excel GESTIC.

**Características principales**:
- Offline: modelos LLM locales (sin API keys)
- Procesamiento de documentos técnicos
- Generación automática de estimaciones GESTIC
- Sistema conversacional basado en agentes

## Estructura del Proyecto

```
LANGCHAIN/
├── AGENTS/          # Código de los agentes inteligentes (.py)
├── PROMPTS/         # Prompts del sistema en archivos .md
├── SCRIPTS/         # Scripts de ejemplo y utilidades
├── INPUT/           # Documentos de entrada (.docx, .pdf, templates .xlsx)
├── OUTPUT/          # Resultados generados (estimaciones .xlsx)
├── DOC/             # Documentación completa (guías en .md)
├── UTILS/           # requirements.txt y archivos temporales
└── .claude/         # Configuración de Claude Code
```

## Convenciones de Organización

| Carpeta | Propósito | Contenido |
|---------|-----------|-----------|
| **INPUT/** | Archivos fuente | Diseños técnicos (.pdf, .docx), plantillas Excel GESTIC |
| **OUTPUT/** | Resultados | Estimaciones generadas (.xlsx) |
| **AGENTS/** | Agentes LangChain | Código de agentes (.py) - un archivo por agente |
| **PROMPTS/** | Configuración | Prompts del sistema en archivos .md (reutilizables) |
| **SCRIPTS/** | Ejemplos | Scripts de prueba y procesamiento |
| **DOC/** | Documentación | Guías completas del proyecto |
| **UTILS/** | Dependencias | requirements.txt, archivos temporales |

**Reglas importantes**:
- Todos los documentos de entrada → `INPUT/`
- Todos los resultados generados → `OUTPUT/`
- Prompts separados en archivos `.md` → `PROMPTS/`
- Documentación → `DOC/` (README.md tiene detalles completos)

## Stack Tecnológico

**Core**:
- Python 3.x
- LangChain (>=0.3.0) - Framework de agentes
- Ollama (>=0.1.6) - Servidor LLM local

**Procesamiento de Documentos**:
- PyPDF2 - Lectura de PDFs
- python-docx - Lectura de Word
- pandas + openpyxl - Manipulación Excel

**Instalación**:
```bash
pip install -r UTILS/requirements.txt              # Básicas
pip install -r UTILS/requirements_estimacion.txt   # Completas
```

## Configuración del Entorno

### Ollama (Modelos Locales)

Modelo por defecto: `llama2`

Comandos esenciales:
```bash
ollama serve         # Iniciar servidor (requerido)
ollama list          # Ver modelos instalados
ollama pull [modelo] # Descargar modelo
```

### Rutas del Proyecto

El código usa rutas relativas desde `PROJECT_ROOT`:
```python
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### Windows UTF-8

Configuración incluida en el código:
```python
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

## Plantilla Excel GESTIC

**Template**: `INPUT/GESTIC-XXXXXX Proyecto - Descripción.xlsx`
**Outputs**: `OUTPUT/estimacion_*.xlsx`

Estructura: Tabla de componentes con columnas Tipo, Nombre, Complejidad, CRUD, Lógica, Integración, UI, Horas + totales por fase.

## Documentación del Proyecto

Para detalles específicos, consultar:
- `README.md` - Inicio rápido completo, ejemplos de uso
- `DOC/GUIA_AGENTES_LANGCHAIN.md` - Fundamentos de agentes
- `DOC/GUIA_AGENTE_ESTIMACION.md` - Guía del agente de estimación
- `PROMPTS/agente-estimacion-desarrollo.md` - Prompt experto

## Agentes Disponibles

**Ubicación**: `AGENTS/`

Consultar README.md para:
- Listado completo de agentes
- Herramientas disponibles por agente
- Ejemplos de uso
- Flujos de trabajo

## Git

**Branch principal**: `main`
**Estado actual**: Repositorio limpio

## Puntos Clave

1. **Sistema offline**: Ollama debe estar ejecutándose (`ollama serve`)
2. **Organización estricta**: INPUT/OUTPUT para trazabilidad
3. **Prompts externos**: Separados en `.md` para mejor mantenibilidad
4. **Plantilla Excel**: No modificar estructura GESTIC template
5. **Entorno virtual**: Recomendado para gestión de dependencias
6. **Documentación completa**: Consultar README.md y DOC/ para detalles

---

**Última actualización**: 2025-11-17
**Usuario**: jjimerod @ NTT DATA EMEAL
**Plataforma**: Windows
