"""
Ejemplo de uso del Agente de Estimación
Muestra cómo usar el agente de forma programática (sin modo interactivo)
"""

from AGENTS.agente_estimacion import (
    EstimacionProyecto,
    ComponenteEstimado,
    exportar_a_excel,
    calcular_estimacion_completa,
    estimacion_actual
)
import pandas as pd
import sys

# ============================================================================
# EJEMPLO 1: Estimación Manual Completa
# ============================================================================

def ejemplo_manual():
    """Crea una estimación completamente manual"""
    print("="*80)
    print("EJEMPLO 1: Estimación Manual")
    print("="*80 + "\n")

    # Crear estimación
    global estimacion_actual
    estimacion_actual = EstimacionProyecto("Sistema CRM Empresarial")

    # Agregar componentes manualmente
    print("📦 Agregando componentes...\n")

    # Modelos de datos
    modelo_cliente = ComponenteEstimado("Modelo de datos", "Cliente")
    modelo_cliente.propiedades = 12  # id, nombre, email, teléfono, dirección, etc.
    modelo_cliente.metodos = 3  # validar, calcularScore, etc.
    modelo_cliente.reglas_negocio = 8
    estimacion_actual.agregar_componente(modelo_cliente)
    print(f"  ✓ {modelo_cliente.tipo}: {modelo_cliente.nombre}")

    modelo_contacto = ComponenteEstimado("Modelo de datos", "Contacto")
    modelo_contacto.propiedades = 10
    modelo_contacto.metodos = 2
    modelo_contacto.reglas_negocio = 5
    estimacion_actual.agregar_componente(modelo_contacto)
    print(f"  ✓ {modelo_contacto.tipo}: {modelo_contacto.nombre}")

    modelo_oportunidad = ComponenteEstimado("Modelo de datos", "Oportunidad")
    modelo_oportunidad.propiedades = 15
    modelo_oportunidad.metodos = 4
    modelo_oportunidad.reglas_negocio = 12
    estimacion_actual.agregar_componente(modelo_oportunidad)
    print(f"  ✓ {modelo_oportunidad.tipo}: {modelo_oportunidad.nombre}")

    # Servicios
    servicio_cliente = ComponenteEstimado("Servicios", "ClienteService")
    servicio_cliente.propiedades = 3
    servicio_cliente.metodos = 15  # CRUD + búsquedas + validaciones
    servicio_cliente.integraciones = 5  # Email, SMS, CRM externo
    estimacion_actual.agregar_componente(servicio_cliente)
    print(f"  ✓ {servicio_cliente.tipo}: {servicio_cliente.nombre}")

    servicio_oportunidad = ComponenteEstimado("Servicios", "OportunidadService")
    servicio_oportunidad.propiedades = 4
    servicio_oportunidad.metodos = 20
    servicio_oportunidad.integraciones = 8
    estimacion_actual.agregar_componente(servicio_oportunidad)
    print(f"  ✓ {servicio_oportunidad.tipo}: {servicio_oportunidad.nombre}")

    # Componentes frontend
    comp_dashboard = ComponenteEstimado("Componentes (TS)", "Dashboard")
    comp_dashboard.propiedades = 15  # Múltiples widgets
    comp_dashboard.metodos = 25  # Lógica de gráficos, filtros
    comp_dashboard.eventos = 20  # Interacciones
    comp_dashboard.integraciones = 10  # APIs
    comp_dashboard.reglas_negocio = 30
    estimacion_actual.agregar_componente(comp_dashboard)
    print(f"  ✓ {comp_dashboard.tipo}: {comp_dashboard.nombre}")

    comp_cliente_list = ComponenteEstimado("Componentes (TS)", "ClienteList")
    comp_cliente_list.propiedades = 8
    comp_cliente_list.metodos = 12
    comp_cliente_list.eventos = 15
    comp_cliente_list.integraciones = 5
    comp_cliente_list.reglas_negocio = 10
    estimacion_actual.agregar_componente(comp_cliente_list)
    print(f"  ✓ {comp_cliente_list.tipo}: {comp_cliente_list.nombre}")

    comp_cliente_detail = ComponenteEstimado("Componentes (TS)", "ClienteDetail")
    comp_cliente_detail.propiedades = 12
    comp_cliente_detail.metodos = 18
    comp_cliente_detail.eventos = 20
    comp_cliente_detail.integraciones = 8
    comp_cliente_detail.reglas_negocio = 25
    estimacion_actual.agregar_componente(comp_cliente_detail)
    print(f"  ✓ {comp_cliente_detail.tipo}: {comp_cliente_detail.nombre}")

    # Vistas HTML
    vista_login = ComponenteEstimado("Vista HTML", "LoginPage")
    vista_login.propiedades = 5
    vista_login.eventos = 8
    vista_login.reglas_negocio = 10
    estimacion_actual.agregar_componente(vista_login)
    print(f"  ✓ {vista_login.tipo}: {vista_login.nombre}")

    # Estilos
    estilo_theme = ComponenteEstimado("Estilos SCSS", "ThemeSystem")
    estilo_theme.propiedades = 20  # Variables de color, espaciado, etc.
    estilo_theme.metodos = 10  # Mixins
    estilo_theme.reglas_negocio = 15
    estimacion_actual.agregar_componente(estilo_theme)
    print(f"  ✓ {estilo_theme.tipo}: {estilo_theme.nombre}")

    print(f"\n📊 Total componentes agregados: {len(estimacion_actual.componentes)}\n")

    # Configurar factores
    estimacion_actual.incertidumbre = "Media"  # Requisitos medianamente claros
    estimacion_actual.acoplamiento = True  # Hay dependencias entre módulos
    estimacion_actual.seniority = "Mid"  # Equipo de nivel medio

    print("⚙️  Factores configurados:")
    print(f"  • Incertidumbre: {estimacion_actual.incertidumbre}")
    print(f"  • Acoplamiento: {'Sí' if estimacion_actual.acoplamiento else 'No'}")
    print(f"  • Seniority: {estimacion_actual.seniority}\n")

    # Calcular
    print("🧮 Calculando estimación...")
    resultado = calcular_estimacion_completa("Media|Si|Mid")
    print(resultado)

    # Exportar
    print("\n📤 Exportando a Excel...")
    nombre_salida = "estimacion_crm_empresarial.xlsx"
    resultado_export = exportar_a_excel(nombre_salida)
    print(resultado_export)

    print("\n" + "="*80)
    print("✅ EJEMPLO 1 COMPLETADO")
    print("="*80 + "\n")


# ============================================================================
# EJEMPLO 2: Estimación Rápida
# ============================================================================

def ejemplo_rapido():
    """Estimación rápida con menos componentes"""
    print("="*80)
    print("EJEMPLO 2: Estimación Rápida (API REST)")
    print("="*80 + "\n")

    global estimacion_actual
    estimacion_actual = EstimacionProyecto("API REST de Productos")

    # Solo componentes backend
    modelo_producto = ComponenteEstimado("Modelo de datos", "Producto")
    modelo_producto.propiedades = 8
    modelo_producto.metodos = 2
    modelo_producto.reglas_negocio = 5
    estimacion_actual.agregar_componente(modelo_producto)

    servicio_producto = ComponenteEstimado("Servicios", "ProductoService")
    servicio_producto.propiedades = 2
    servicio_producto.metodos = 10
    servicio_producto.integraciones = 3
    estimacion_actual.agregar_componente(servicio_producto)

    print(f"📦 Componentes: {len(estimacion_actual.componentes)}")

    # Configurar (API sencilla, equipo senior)
    estimacion_actual.incertidumbre = "Baja"
    estimacion_actual.acoplamiento = False
    estimacion_actual.seniority = "Senior"

    resultado = calcular_estimacion_completa("Baja|No|Senior")
    print(resultado)

    exportar_a_excel("estimacion_api_productos.xlsx")

    print("\n✅ EJEMPLO 2 COMPLETADO\n")


# ============================================================================
# EJEMPLO 3: Comparación de Escenarios
# ============================================================================

def ejemplo_comparacion():
    """Compara diferentes escenarios de un mismo proyecto"""
    print("="*80)
    print("EJEMPLO 3: Comparación de Escenarios")
    print("="*80 + "\n")

    global estimacion_actual

    # Definir componentes base
    def crear_componentes_base():
        global estimacion_actual
        estimacion_actual = EstimacionProyecto("Sistema de Reservas")

        modelo_reserva = ComponenteEstimado("Modelo de datos", "Reserva")
        modelo_reserva.propiedades = 10
        modelo_reserva.metodos = 3
        modelo_reserva.reglas_negocio = 8
        estimacion_actual.agregar_componente(modelo_reserva)

        servicio_reserva = ComponenteEstimado("Servicios", "ReservaService")
        servicio_reserva.propiedades = 3
        servicio_reserva.metodos = 12
        servicio_reserva.integraciones = 5
        estimacion_actual.agregar_componente(servicio_reserva)

        comp_calendario = ComponenteEstimado("Componentes (TS)", "CalendarioReservas")
        comp_calendario.propiedades = 12
        comp_calendario.metodos = 20
        comp_calendario.eventos = 25
        comp_calendario.integraciones = 8
        comp_calendario.reglas_negocio = 30
        estimacion_actual.agregar_componente(comp_calendario)

    # Escenario 1: Equipo Junior, alta incertidumbre
    print("📊 ESCENARIO 1: Equipo Junior + Alta Incertidumbre")
    crear_componentes_base()
    estimacion_actual.incertidumbre = "Alta"
    estimacion_actual.acoplamiento = True
    estimacion_actual.seniority = "Junior"
    resultado1 = calcular_estimacion_completa("Alta|Si|Junior")
    print(resultado1)

    # Escenario 2: Equipo Mid, incertidumbre media
    print("\n📊 ESCENARIO 2: Equipo Mid + Incertidumbre Media")
    crear_componentes_base()
    estimacion_actual.incertidumbre = "Media"
    estimacion_actual.acoplamiento = True
    estimacion_actual.seniority = "Mid"
    resultado2 = calcular_estimacion_completa("Media|Si|Mid")
    print(resultado2)

    # Escenario 3: Equipo Senior, baja incertidumbre
    print("\n📊 ESCENARIO 3: Equipo Senior + Baja Incertidumbre")
    crear_componentes_base()
    estimacion_actual.incertidumbre = "Baja"
    estimacion_actual.acoplamiento = False
    estimacion_actual.seniority = "Senior"
    resultado3 = calcular_estimacion_completa("Baja|No|Senior")
    print(resultado3)

    print("\n" + "="*80)
    print("✅ EJEMPLO 3 COMPLETADO - Revisa las diferencias entre escenarios")
    print("="*80 + "\n")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🤖 EJEMPLOS DE USO DEL AGENTE DE ESTIMACIÓN")
    print("="*80 + "\n")

    if len(sys.argv) > 1:
        ejemplo = sys.argv[1]
        if ejemplo == "1":
            ejemplo_manual()
        elif ejemplo == "2":
            ejemplo_rapido()
        elif ejemplo == "3":
            ejemplo_comparacion()
        else:
            print("Uso: python ejemplo_estimacion.py [1|2|3]")
    else:
        print("Selecciona un ejemplo:")
        print("  1 - Estimación Manual Completa (CRM)")
        print("  2 - Estimación Rápida (API REST)")
        print("  3 - Comparación de Escenarios")
        print("\nEjecuta: python ejemplo_estimacion.py [número]\n")

        # Por defecto, ejecutar todos
        respuesta = input("¿Ejecutar todos los ejemplos? (s/n): ").strip().lower()
        if respuesta == 's':
            ejemplo_manual()
            input("\nPresiona ENTER para continuar al siguiente ejemplo...")
            ejemplo_rapido()
            input("\nPresiona ENTER para continuar al siguiente ejemplo...")
            ejemplo_comparacion()
        else:
            print("\n👋 ¡Hasta luego!")
