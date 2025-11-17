# 🤖 Guía del Agente de Estimación de Desarrollo

## 📋 Tabla de Contenidos
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Arquitectura del Agente](#arquitectura-del-agente)
4. [Herramientas Disponibles](#herramientas-disponibles)
5. [Flujo de Trabajo](#flujo-de-trabajo)
6. [Ejemplos de Uso](#ejemplos-de-uso)
7. [Estructura del Excel GESTIC](#estructura-del-excel-gestic)
8. [Personalización](#personalización)
9. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este agente inteligente automatiza el proceso de estimación de proyectos de desarrollo de software:

- ✅ **Lee** diseños técnicos en PDF o Word
- ✅ **Analiza** y extrae componentes automáticamente
- ✅ **Calcula** estimaciones usando ponderaciones profesionales
- ✅ **Genera** documentos Excel GESTIC listos para usar
- ✅ **Aplica** factores de ajuste (incertidumbre, acoplamiento, seniority)

### ¿Qué es GESTIC?

GESTIC es una metodología de estimación que descompone el desarrollo en:

- **Componentes técnicos**: Modelos, Servicios, Componentes, Vistas, Estilos
- **Elementos contables**: Propiedades, Métodos, Eventos, Integraciones, Reglas de Negocio
- **Factores de ajuste**: Incertidumbre, Acoplamiento, Nivel del desarrollador
- **Fases del proyecto**: Análisis, Construcción, Pruebas, Documentación, Peer Review

---

## 🔧 Instalación

### Paso 1: Instalar Ollama

```bash
# Windows
winget install Ollama.Ollama

# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh
```

### Paso 2: Descargar Modelo

```bash
# Iniciar Ollama
ollama serve

# En otra terminal
ollama pull llama2
# o mejor aún (más preciso para análisis técnico):
ollama pull mistral
```

### Paso 3: Instalar Dependencias Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar
venv\Scripts\activate  # Windows
# o
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements_estimacion.txt
```

### Paso 4: Verificar Instalación

```bash
python -c "import PyPDF2, docx, pandas, openpyxl; print('✅ Todo OK')"
```

---

## 🏗️ Arquitectura del Agente

```
┌─────────────────────────────────────────────────────────┐
│                  USUARIO                                │
│  (Proporciona diseño técnico en PDF/Word)               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              AGENTE LANGCHAIN (Cerebro)                 │
│  - Razona sobre qué herramientas usar                   │
│  - Decide el orden de acciones                          │
│  - Aplica el conocimiento del prompt de estimación      │
└────────────────────┬────────────────────────────────────┘
                     │
         ┌───────────┼───────────┐
         │           │           │
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │ LeerPDF│  │LeerWord│  │Extraer │
    │        │  │        │  │Comps   │
    └────────┘  └────────┘  └────────┘
                     │
         ┌───────────┼───────────┐
         ▼           ▼           ▼
    ┌────────┐  ┌────────┐  ┌────────┐
    │Agregar │  │Calcular│  │Exportar│
    │ Comp   │  │Estim.  │  │ Excel  │
    └────────┘  └────────┘  └────────┘
                     │
                     ▼
         ┌────────────────────────┐
         │   EXCEL GESTIC         │
         │ (Estimación completa)  │
         └────────────────────────┘
```

### Componentes Clave

1. **LLM (Ollama)**: Motor de razonamiento del agente
2. **Herramientas**: Funciones Python que el agente puede ejecutar
3. **Prompt de Estimación**: Conocimiento experto integrado
4. **Ponderaciones GESTIC**: Tabla de tiempos por tipo de elemento
5. **Plantilla Excel**: Salida estructurada

---

## 🛠️ Herramientas Disponibles

### 1. LeerPDF
**Qué hace:** Lee archivos PDF y extrae el texto completo.

**Input:** Ruta completa al archivo PDF

**Ejemplo:**
```
C:\Users\Usuario\Desktop\diseño_sistema.pdf
```

**Output:** Texto extraído con indicación de páginas

---

### 2. LeerWord
**Qué hace:** Lee archivos Word (.docx) incluyendo texto y tablas.

**Input:** Ruta completa al archivo Word

**Ejemplo:**
```
C:\Users\Usuario\Desktop\especificacion_tecnica.docx
```

**Output:** Texto y tablas extraídas

---

### 3. ExtraerComponentes
**Qué hace:** Analiza el diseño técnico usando patrones regex para detectar automáticamente:
- Modelos de datos
- Módulos
- Servicios
- Componentes TypeScript
- Vistas HTML
- Estilos SCSS

**Input:** Texto del diseño técnico

**Output:** Lista de componentes detectados con valores estimados por defecto

---

### 4. AgregarComponente
**Qué hace:** Agrega un componente manualmente con especificación precisa.

**Input:** `tipo|nombre|propiedades|métodos|eventos|integraciones|reglas`

**Ejemplos:**
```
Servicio|AuthenticationService|3|8|0|2|5
Componentes (TS)|UserDashboard|5|10|8|3|12
Modelo de datos|Usuario|8|2|0|0|3
Vista HTML|LoginPage|2|0|5|0|8
```

**Tipos válidos:**
- `Modelo de datos`
- `Módulos`
- `Servicios`
- `Componentes (TS)`
- `Vista HTML`
- `Estilos SCSS`

---

### 5. CalcularEstimacion
**Qué hace:** Calcula la estimación completa aplicando:
- Ponderaciones por tipo de componente
- Factor de seniority del desarrollador
- Factor de incertidumbre
- Factor de acoplamiento
- Distribución en fases

**Input:** `incertidumbre|acoplamiento|seniority`

**Valores válidos:**

| Parámetro | Valores Posibles |
|-----------|------------------|
| Incertidumbre | Nula, Baja, Media, Alta |
| Acoplamiento | Si, No |
| Seniority | Senior, Mid, Junior |

**Ejemplos:**
```
Media|Si|Mid
Baja|No|Senior
Alta|Si|Junior
```

**Output:** Resumen con:
- Horas base
- Horas ajustadas por seniority
- Incremento por incertidumbre
- Incremento por acoplamiento
- Total final
- Distribución por fases

---

### 6. ExportarExcel
**Qué hace:** Genera un archivo Excel basado en la plantilla GESTIC con todos los datos de la estimación.

**Input:** Nombre del archivo de salida

**Ejemplo:**
```
estimacion_proyecto_erp.xlsx
```

**Output:**
- Archivo Excel creado en el mismo directorio
- Pestaña `Estimador_resumen` con totales por fase
- Pestaña `Estimador_desglosado` con todos los componentes
- Factores de incertidumbre y acoplamiento aplicados

---

## 📊 Flujo de Trabajo

### Flujo Completo Recomendado

```
1. Usuario → "Analiza el diseño técnico en C:\docs\diseño_api.pdf"
             ↓
2. Agente usa LeerPDF
             ↓
3. Agente usa ExtraerComponentes
             ↓
4. Usuario revisa y ajusta → "Agrega: Servicio|PaymentService|4|12|0|5|8"
             ↓
5. Agente usa AgregarComponente
             ↓
6. Usuario → "Calcula estimación con incertidumbre Media, acoplamiento Si, seniority Mid"
             ↓
7. Agente usa CalcularEstimacion
             ↓
8. Usuario → "Exporta a estimacion_payment_api.xlsx"
             ↓
9. Agente usa ExportarExcel
             ↓
10. ✅ Excel listo para entregar
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Estimación desde PDF

```
👤 Tú: Analiza el archivo C:\Users\Juan\Desktop\diseño_crm.pdf

🤖 Agente: [Lee el PDF, extrae componentes automáticamente]
📤 Respuesta: He detectado:
- 5 Modelos de datos (Cliente, Contacto, Oportunidad, Tarea, Nota)
- 3 Servicios (ClienteService, ContactoService, OportunidadService)
- 8 Componentes (TS) (Dashboard, ClienteList, ClienteDetail, ...)
- 6 Vistas HTML
Total estimado: 320 horas base

👤 Tú: Calcula con incertidumbre Media, acoplamiento Si, seniority Mid

🤖 Agente: [Aplica ponderaciones y factores]
📤 Respuesta:
Horas base: 320h
Ajustadas (Mid): 480h
+ Incertidumbre (15%): 72h
+ Acoplamiento (15%): 72h
TOTAL: 624 horas (≈ 15.6 semanas con 1 dev)

👤 Tú: Exporta a estimacion_crm_2024.xlsx

🤖 Agente: ✅ Archivo creado correctamente
```

---

### Ejemplo 2: Estimación Manual

```
👤 Tú: Voy a estimar un sistema de reservas manualmente

🤖 Agente: Perfecto, usa AgregarComponente para cada elemento

👤 Tú: Agrega Servicio|ReservaService|5|15|0|8|20

🤖 Agente: ✅ Componente agregado

👤 Tú: Agrega Componentes (TS)|CalendarioReservas|10|20|15|5|25

🤖 Agente: ✅ Componente agregado

👤 Tú: Agrega Modelo de datos|Reserva|12|3|0|0|8

🤖 Agente: ✅ Componente agregado

👤 Tú: Calcula con incertidumbre Baja, acoplamiento No, seniority Senior

🤖 Agente: [Calcula]
📤 TOTAL: 180 horas

👤 Tú: Exporta a reservas_hotel.xlsx

🤖 Agente: ✅ Listo
```

---

### Ejemplo 3: Estimación desde Word con Ajustes

```
👤 Tú: Lee el documento C:\docs\spec_ecommerce.docx y extrae los componentes

🤖 Agente: [Lee Word, detecta componentes]
📤 Detectados: 15 componentes (120h base)

👤 Tú: El ProductService tiene 20 métodos, no 2. Agrégalo correctamente:
     Servicio|ProductService|6|20|0|10|15

🤖 Agente: ✅ Actualizado

👤 Tú: También necesitamos un sistema de carrito complejo:
     Componentes (TS)|ShoppingCart|15|30|20|8|35

🤖 Agente: ✅ Agregado

👤 Tú: Calcula con Media|Si|Mid y exporta a ecommerce_estimate.xlsx

🤖 Agente: [Calcula y exporta]
📤 ✅ Total: 456 horas. Excel generado.
```

---

## 📐 Estructura del Excel GESTIC

### Pestaña: Ponderaciones

Define los **tiempos en minutos** por cada elemento según el tipo:

| Tipo | Propiedad | Método | Evento | Integración | Regla Negocio |
|------|-----------|--------|--------|-------------|---------------|
| Modelo de datos | 10 | 15 | 0 | 0 | 60 |
| Módulos | 5 | 45 | 0 | 30 | 0 |
| Servicios | 10 | 15 | 0 | 45 | 0 |
| Componentes (TS) | 10 | 30 | 30 | 45 | 60 |
| Vista HTML | 10 | 0 | 10 | 0 | 15 |
| Estilos SCSS | 15 | 30 | 15 | 75 | 30 |

**Ejemplo de cálculo:**
```
Servicio con:
- 3 propiedades: 3 × 10 = 30 min
- 8 métodos: 8 × 15 = 120 min
- 2 integraciones: 2 × 45 = 90 min
Total: 240 min = 4 horas
```

---

### Factores de Ajuste

#### Seniority
- **Senior**: ×1.0 (más rápido, experiencia)
- **Mid**: ×1.5 (nivel medio)
- **Junior**: ×2.5 (menos experiencia, más tiempo de aprendizaje)

#### Incertidumbre
- **Nula** (0%): Requisitos perfectamente claros
- **Baja** (+7%): Requisitos claros con pequeñas ambigüedades
- **Media** (+15%): Algunos requisitos poco claros
- **Alta** (+30%): Muchos requisitos ambiguos

#### Acoplamiento
- **No** (0%): Componentes independientes
- **Sí** (+15%): Múltiples dependencias entre componentes

---

### Distribución por Fases

El agente distribuye automáticamente las horas en:

- **Análisis técnico**: 10% del desarrollo
- **Construcción**: 60% del desarrollo
- **Pruebas**: 20% del desarrollo
- **Documentación**: 5% del desarrollo
- **Peer Review**: 5% del desarrollo

**Ejemplo:**
```
Total desarrollo ajustado: 400h
- Análisis: 40h
- Construcción: 240h
- Pruebas: 80h
- Documentación: 20h
- Peer Review: 20h
```

---

## 🎨 Personalización

### Modificar Ponderaciones

Edita el archivo Excel `GESTIC-XXXXXX Proyecto - Descripción.xlsx`:

1. Abre la pestaña `Ponderaciones`
2. Ajusta los valores en minutos según tu experiencia
3. Guarda el archivo
4. El agente usará automáticamente los nuevos valores

### Cambiar el Modelo LLM

En `agente_estimacion.py`, línea ~570:

```python
llm = Ollama(
    model="llama2",  # Cambia a: "mistral", "llama3.2", "codellama"
    temperature=0.3  # Aumenta para más creatividad, baja para más precisión
)
```

**Modelos recomendados:**
- `mistral`: Mejor para análisis técnico
- `llama3.2`: Más reciente, bueno para razonamiento
- `codellama`: Especializado en código

### Ajustar Patrones de Extracción

En `agente_estimacion.py`, función `extraer_componentes_tecnicos`:

```python
patrones = {
    "Modelo de datos": r"(?:modelo|entidad|entity|tabla|table)s?\s+(\w+)",
    # Agrega tus propios patrones aquí
}
```

### Modificar Distribución de Fases

En `agente_estimacion.py`, función `calcular_estimacion_completa`:

```python
estimacion_actual.horas_construccion = total_desarrollo * 0.60  # Cambia los %
estimacion_actual.horas_pruebas = total_desarrollo * 0.20
# ... etc
```

---

## 🐛 Troubleshooting

### ❌ Error: "Archivo no existe"

**Causa:** Ruta incorrecta del PDF/Word

**Solución:**
```python
# Usa rutas absolutas completas
C:\Users\TuNombre\Desktop\archivo.pdf

# Verifica que el archivo existe:
# Windows: dir "ruta\al\archivo.pdf"
# Linux/Mac: ls ruta/al/archivo.pdf
```

---

### ❌ Error: "No se detectaron componentes"

**Causa:** El diseño técnico no tiene los términos esperados

**Solución:**
1. Agrega componentes manualmente con `AgregarComponente`
2. O modifica los patrones regex en el código

---

### ❌ Error al escribir Excel: "Permission denied"

**Causa:** El archivo Excel está abierto

**Solución:**
- Cierra el archivo Excel GESTIC
- Intenta de nuevo

---

### ❌ El agente no usa las herramientas correctamente

**Causa:** Modelo demasiado básico o temperatura muy alta

**Solución:**
```bash
# Usa un modelo mejor
ollama pull mistral

# En el código, reduce la temperatura
llm = Ollama(model="mistral", temperature=0.1)
```

---

### ❌ Estimaciones muy altas/bajas

**Causa:** Ponderaciones no ajustadas a tu contexto

**Solución:**
1. Revisa estimaciones anteriores reales
2. Ajusta las ponderaciones en el Excel
3. Calibra con proyectos históricos

---

## 📚 Mejores Prácticas

### 1. Preparación del Diseño Técnico

✅ **Bueno:**
```
Sistema de Gestión de Biblioteca

Modelos:
- Libro (ISBN, título, autor, categoría, disponible)
- Usuario (DNI, nombre, email, teléfono)
- Préstamo (fecha_inicio, fecha_fin, estado)

Servicios:
- LibroService: buscarPorISBN(), listarDisponibles(), reservar()
- PrestamoService: crearPrestamo(), devolverLibro(), calcularMulta()

Componentes:
- CatalogoBiblioteca: búsqueda avanzada, filtros, paginación
- DetalleLil: información completa, disponibilidad, reserva

Integraciones:
- API email para notificaciones
- Sistema de pagos para multas
```

❌ **Malo:**
```
Hacer un sistema de biblioteca con libros y usuarios.
```

### 2. Revisión Manual

Siempre revisa los componentes auto-detectados:
```
1. Extrae automáticamente
2. Revisa la lista
3. Agrega/corrige manualmente los incorrectos
4. Calcula estimación
```

### 3. Iteración

No esperes perfección en el primer intento:
```
Primera pasada: Detección automática (70% precisión)
Segunda pasada: Ajustes manuales (+20%)
Tercera pasada: Validación con experto (+10%)
```

### 4. Documentación de Supuestos

Agrega notas en el Excel sobre:
- Tecnologías asumidas
- Complejidades consideradas
- Áreas con mayor incertidumbre

---

## 🚀 Casos de Uso Avanzados

### Integración con CI/CD

```python
# Script automatizado
import subprocess

# 1. Generar estimación
subprocess.run(["python", "agente_estimacion.py", "--input", "diseño.pdf", "--output", "est.xlsx"])

# 2. Validar que está dentro del presupuesto
# ... lógica de validación ...

# 3. Adjuntar a PR automáticamente
```

### API REST del Agente

Envuelve el agente en una API Flask:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/estimar', methods=['POST'])
def estimar():
    archivo = request.files['diseño']
    # Procesar con el agente
    # Retornar JSON con estimación
    return jsonify({...})
```

---

## 📞 Soporte y Contacto

Si necesitas ayuda:

1. Revisa esta guía completa
2. Consulta los ejemplos de uso
3. Verifica que Ollama esté corriendo: `ollama list`
4. Prueba con `verbose=True` para depurar

---

**¡Buena suerte con tus estimaciones! 📊✨**
