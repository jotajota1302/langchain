"""
Análisis inteligente del diseño técnico GESTIC usando Qwen2.5
Usa LangChain + Ollama para extraer componentes de forma más precisa
"""

import os
import sys
import re
import math
from docx import Document
import pandas as pd
from openpyxl import load_workbook
from langchain_community.llms import Ollama

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_WORD = r"C:\Users\Nitropc\Desktop\LANGCHAIN\GESTIC-833509_Diseno_Tecnico_Detalle_RD_v2.docx"
EXCEL_TEMPLATE = r"C:\Users\Nitropc\Desktop\LANGCHAIN\GESTIC-XXXXXX Proyecto - Descripción.xlsx"
ARCHIVO_SALIDA = "estimacion_gestic_833509_RD_IA.xlsx"

print("="*80)
print("🤖 ANÁLISIS INTELIGENTE CON QWEN2.5")
print("="*80 + "\n")

# ============================================================================
# PASO 1: INICIALIZAR MODELO
# ============================================================================

print("🔧 Inicializando modelo Qwen2.5...")
llm = Ollama(
    model="qwen2.5",
    temperature=0.1  # Baja temperatura para ser más preciso
)
print("✅ Modelo cargado\n")

# ============================================================================
# PASO 2: LEER DOCUMENTO
# ============================================================================

print("📄 Leyendo documento Word...")
doc = Document(ARCHIVO_WORD)

# Extraer texto completo
texto_completo = []
for parrafo in doc.paragraphs:
    if parrafo.text.strip():
        texto_completo.append(parrafo.text)

texto_completo_str = "\n".join(texto_completo)
print(f"✅ Documento leído: {len(texto_completo_str)} caracteres\n")

# Limitar el texto a los primeros 15000 caracteres para el análisis (límite del modelo)
texto_para_analisis = texto_completo_str[:15000]

# ============================================================================
# PASO 3: ANÁLISIS INTELIGENTE CON IA
# ============================================================================

print("="*80)
print("🧠 ANALIZANDO DISEÑO TÉCNICO CON IA")
print("="*80 + "\n")

# Prompt 1: Extraer servicios
print("🔍 Paso 1/3: Extrayendo servicios...")

prompt_servicios = f"""Eres un experto en análisis de diseños técnicos de Angular.

Analiza el siguiente diseño técnico y extrae ÚNICAMENTE los servicios (Services) mencionados.

Un servicio TypeScript/Angular típicamente:
- Tiene el sufijo "Service" en su nombre
- Se usa para lógica de negocio, llamadas API, gestión de estado
- Ejemplos: UserService, AuthService, DataService

IMPORTANTE:
- Lista SOLO los servicios que encuentres explícitamente mencionados
- NO inventes servicios que no estén en el texto
- Un servicio por línea
- Solo el nombre, sin explicaciones

Texto del diseño:
{texto_para_analisis}

Lista de servicios encontrados:"""

resultado_servicios = llm.invoke(prompt_servicios)

servicios = [s.strip() for s in resultado_servicios.strip().split('\n') if s.strip() and len(s.strip()) > 3]
# Limpiar numeración si existe
servicios = [re.sub(r'^\d+[\.\)]\s*', '', s) for s in servicios]
# Filtrar líneas que no son nombres de servicios
servicios = [s for s in servicios if 'Service' in s and len(s) < 50]

print(f"   ✅ Encontrados {len(servicios)} servicios")
for servicio in servicios[:10]:
    print(f"      - {servicio}")
if len(servicios) > 10:
    print(f"      ... y {len(servicios)-10} más")

# Prompt 2: Extraer componentes
print("\n🔍 Paso 2/3: Extrayendo componentes...")

prompt_componentes = f"""Eres un experto en análisis de diseños técnicos de Angular.

Analiza el siguiente diseño técnico y extrae ÚNICAMENTE los componentes (Components) de Angular mencionados.

Un componente Angular típicamente:
- Tiene el sufijo "Component" en su nombre
- Representa una vista/interfaz de usuario
- Ejemplos: HeaderComponent, UserListComponent, DashboardComponent

IMPORTANTE:
- Lista SOLO los componentes que encuentres explícitamente mencionados
- NO inventes componentes que no estén en el texto
- Un componente por línea
- Solo el nombre, sin explicaciones

Texto del diseño:
{texto_para_analisis}

Lista de componentes encontrados:"""

resultado_componentes = llm.invoke(prompt_componentes)

componentes = [c.strip() for c in resultado_componentes.strip().split('\n') if c.strip() and len(c.strip()) > 3]
# Limpiar numeración
componentes = [re.sub(r'^\d+[\.\)]\s*', '', c) for c in componentes]
# Filtrar líneas que no son nombres de componentes
componentes = [c for c in componentes if 'Component' in c and len(c) < 60]

print(f"   ✅ Encontrados {len(componentes)} componentes")
for comp in componentes[:15]:
    print(f"      - {comp}")
if len(componentes) > 15:
    print(f"      ... y {len(componentes)-15} más")

# Prompt 3: Estimar complejidad
print("\n🔍 Paso 3/3: Analizando complejidad del proyecto...")

prompt_complejidad = f"""Eres un experto en estimación de proyectos de desarrollo.

Analiza el siguiente diseño técnico y responde ÚNICAMENTE con un número del 1 al 10:

1-3: Proyecto simple (CRUD básico, pocas integraciones)
4-6: Proyecto medio (múltiples entidades, algunas integraciones)
7-10: Proyecto complejo (muchas integraciones, lógica de negocio compleja, workflows)

Considera:
- Número de componentes y servicios
- Integraciones con sistemas externos
- Complejidad de la lógica de negocio
- Workflows y permisos

Texto del diseño:
{texto_para_analisis}

Responde SOLO con el número (1-10):"""

resultado_complejidad = llm.invoke(prompt_complejidad)

try:
    complejidad = int(re.search(r'\d+', resultado_complejidad).group())
    complejidad = max(1, min(10, complejidad))  # Asegurar rango 1-10
except:
    complejidad = 6  # Valor por defecto medio

print(f"   ✅ Complejidad estimada: {complejidad}/10")

# ============================================================================
# PASO 4: CALCULAR ESTIMACIÓN
# ============================================================================

print("\n" + "="*80)
print("🧮 CALCULANDO ESTIMACIÓN")
print("="*80 + "\n")

class ComponenteEstimado:
    def __init__(self, tipo, nombre):
        self.tipo = tipo
        self.nombre = nombre
        self.propiedades = 0
        self.metodos = 0
        self.eventos = 0
        self.integraciones = 0
        self.reglas_negocio = 0
        self.horas = 0

componentes_estimados = []

# Ajustar estimaciones según complejidad detectada
# Complejidad baja (1-3): valores conservadores
# Complejidad media (4-6): valores estándar
# Complejidad alta (7-10): valores altos

factor_complejidad = complejidad / 6  # Factor relativo a complejidad media

# Servicios
for servicio in servicios[:20]:
    comp = ComponenteEstimado("Servicios", servicio)
    comp.propiedades = math.ceil(3 * factor_complejidad)
    comp.metodos = math.ceil(12 * factor_complejidad)
    comp.integraciones = math.ceil(3 * factor_complejidad)
    comp.horas = math.ceil((comp.propiedades * 10 + comp.metodos * 15 + comp.integraciones * 45) / 60)
    componentes_estimados.append(comp)

# Componentes
for componente in componentes[:25]:
    comp = ComponenteEstimado("Componentes (TS)", componente)
    comp.propiedades = math.ceil(8 * factor_complejidad)
    comp.metodos = math.ceil(15 * factor_complejidad)
    comp.eventos = math.ceil(10 * factor_complejidad)
    comp.integraciones = math.ceil(5 * factor_complejidad)
    comp.reglas_negocio = math.ceil(12 * factor_complejidad)
    comp.horas = math.ceil((comp.propiedades * 10 + comp.metodos * 30 + comp.eventos * 30 +
                  comp.integraciones * 45 + comp.reglas_negocio * 60) / 60)
    componentes_estimados.append(comp)

# Calcular totales
total_horas_base = sum(c.horas for c in componentes_estimados)

# Aplicar factores
factor_seniority = 1.5  # Mid
horas_ajustadas = math.ceil(total_horas_base * factor_seniority)

factor_incertidumbre = 0.15  # Media
horas_incertidumbre = math.ceil(horas_ajustadas * factor_incertidumbre)

factor_acoplamiento = 0.15  # Sí
horas_acoplamiento = math.ceil(horas_ajustadas * factor_acoplamiento)

total_final = math.ceil(horas_ajustadas + horas_incertidumbre + horas_acoplamiento)

# Distribución por fases
horas_analisis = math.ceil(horas_ajustadas * 0.10)
horas_construccion = math.ceil(horas_ajustadas * 0.60)
horas_pruebas = math.ceil(horas_ajustadas * 0.20)
horas_documentacion = math.ceil(horas_ajustadas * 0.05)
horas_peer_review = math.ceil(horas_ajustadas * 0.05)

print("📊 RESUMEN DE ESTIMACIÓN (CON IA):\n")
print(f"   Componentes analizados: {len(componentes_estimados)}")
print(f"      - Servicios: {len([c for c in componentes_estimados if c.tipo == 'Servicios'])}")
print(f"      - Componentes TS: {len([c for c in componentes_estimados if c.tipo == 'Componentes (TS)'])}")
print(f"   Complejidad del proyecto: {complejidad}/10")
print(f"   Factor de ajuste por complejidad: {factor_complejidad:.2f}x")
print(f"\n   Horas base: {total_horas_base}h")
print(f"   Horas ajustadas (Mid): {horas_ajustadas}h")
print(f"   + Incertidumbre (Media 15%): {horas_incertidumbre}h")
print(f"   + Acoplamiento (15%): {horas_acoplamiento}h")
print(f"   {'─'*40}")
print(f"   TOTAL FINAL: {total_final} horas")
print(f"\n   📅 Duración estimada:")
print(f"      - Con 1 desarrollador: {math.ceil(total_final/40)} semanas")
print(f"      - Con 2 desarrolladores: {math.ceil(total_final/80)} semanas")
print(f"      - Con 3 desarrolladores: {math.ceil(total_final/120)} semanas")
print(f"\n   📋 Distribución por fases:")
print(f"      - Análisis técnico: {horas_analisis}h")
print(f"      - Construcción: {horas_construccion}h")
print(f"      - Pruebas: {horas_pruebas}h")
print(f"      - Documentación: {horas_documentacion}h")
print(f"      - Peer Review: {horas_peer_review}h")

# ============================================================================
# PASO 5: EXPORTAR A EXCEL
# ============================================================================

print("\n" + "="*80)
print("📤 EXPORTANDO A EXCEL GESTIC")
print("="*80 + "\n")

try:
    wb = load_workbook(EXCEL_TEMPLATE)

    # Escribir en Estimador_resumen
    ws_resumen = wb['Estimador_resumen']
    fila_inicio = 4

    ws_resumen[f'D{fila_inicio+1}'] = 0  # Gestión
    ws_resumen[f'D{fila_inicio+2}'] = horas_analisis
    ws_resumen[f'D{fila_inicio+3}'] = horas_construccion
    ws_resumen[f'D{fila_inicio+4}'] = horas_pruebas
    ws_resumen[f'D{fila_inicio+5}'] = horas_documentacion
    ws_resumen[f'D{fila_inicio+6}'] = horas_peer_review

    ws_resumen['C1'] = "Media"
    ws_resumen['C2'] = "Sí"

    # Escribir en Estimador_desglosado
    ws_desglosado = wb['Estimador_desglosado']
    fila_actual = 6

    for comp in componentes_estimados[:50]:
        ws_desglosado[f'A{fila_actual}'] = comp.tipo
        ws_desglosado[f'B{fila_actual}'] = "SÍ"
        ws_desglosado[f'C{fila_actual}'] = comp.nombre
        ws_desglosado[f'D{fila_actual}'] = comp.propiedades
        ws_desglosado[f'E{fila_actual}'] = comp.metodos
        ws_desglosado[f'F{fila_actual}'] = comp.eventos
        ws_desglosado[f'G{fila_actual}'] = comp.integraciones
        ws_desglosado[f'H{fila_actual}'] = comp.reglas_negocio
        ws_desglosado[f'I{fila_actual}'] = comp.horas
        fila_actual += 1

    wb.save(ARCHIVO_SALIDA)

    print(f"✅ Estimación exportada a: {ARCHIVO_SALIDA}")
    print(f"   Total componentes: {len(componentes_estimados)}")
    print(f"   Total horas: {total_final}h")

except Exception as e:
    print(f"❌ Error al exportar: {e}")
    import traceback
    traceback.print_exc()

# ============================================================================
# PASO 6: COMPARACIÓN CON ANÁLISIS MANUAL
# ============================================================================

print("\n" + "="*80)
print("📊 COMPARACIÓN: IA vs REGEX")
print("="*80 + "\n")

# Leer resultados del análisis manual anterior
print("Análisis con REGEX (procesar_gestic_rd.py):")
print("  - Servicios detectados: 5")
print("  - Componentes detectados: 24 (15 usados)")
print("  - Total horas: 936h")
print()
print(f"Análisis con IA (Qwen2.5):")
print(f"  - Servicios detectados: {len(servicios)}")
print(f"  - Componentes detectados: {len(componentes)}")
print(f"  - Total horas: {total_final}h")
print(f"  - Complejidad analizada: {complejidad}/10")
print()

diferencia_horas = total_final - 936
porcentaje = (diferencia_horas / 936) * 100
print(f"Diferencia: {diferencia_horas:+d}h ({porcentaje:+.1f}%)")

print("\n" + "="*80)
print("✅ PROCESO COMPLETADO")
print("="*80)
print(f"\nArchivos generados:")
print(f"   - {ARCHIVO_SALIDA} (estimación con IA)")
print()
