"""
🏭 Industrial Intelligence OS - Dashboard Unificado de Operaciones
Diseño Avanzado en Tema Claro · Enfoque Analítico de Toma de Decisiones
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# ─── 1. CONFIGURACIÓN DE LA PÁGINA ──────────────────────────────────────────
st.set_page_config(
    page_title="Industrial Intelligence OS",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── 2. ESTILOS CSS PERSONALIZADOS (TEMA CLARO CORPORATIVO) ─────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* Fondos y contenedor principal */
.stApp {
    background-color: #f8f9fa;
    color: #212529;
    font-family: 'Inter', sans-serif;
}

/* Barra lateral */
section[data-testid="stSidebar"] {
    background-color: #ffffff !important;
    border-right: 1px solid #e9ecef;
}
section[data-testid="stSidebar"] * {
    color: #495057 !important;
}

/* Encabezados */
h1, h2, h3 {
    color: #1a2530 !important;
    font-weight: 600 !important;
    letter-spacing: -0.02em;
}

/* Tarjetas KPI Ejecutivas */
.kpi-box {
    background-color: #ffffff;
    border: 1px solid #e9ecef;
    border-radius: 10px;
    padding: 20px;
    text-align: left;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
    margin-bottom: 15px;
}
.kpi-lbl {
    font-size: 11px;
    color: #6c757d;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 30px;
    font-weight: 600;
    color: #0056b3;
    margin-top: 4px;
}
.kpi-subtext {
    font-size: 12px;
    color: #28a745;
    margin-top: 4px;
    font-weight: 500;
}

/* Contenedores de secciones internas */
.section-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #495057;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 2px solid #e9ecef;
    padding-bottom: 5px;
    margin-bottom: 15px;
    margin-top: 10px;
}
</style>""", unsafe_allow_html=True)

# Paleta de colores para gráficos en tema claro
LIGHT_THEME_COLORS = ["#0056b3", "#28a745", "#fd7e14", "#6f42c1", "#e83e8c", "#17a2b8"]

# ─── 3. FUNCIONES DE CARGA DE DATOS (CON RESPALDO AUTOMÁTICO) ───────────────
@st.cache_data(ttl=600)
def cargar_datos_inventario():
    # Intenta leer el archivo de Kaggle si existe en la carpeta
    if os.path.exists("supply_chain_data.csv"):
        return pd.read_csv("supply_chain_data.csv")
    else:
        # Datos simulados de respaldo con la misma estructura de Kaggle para que la app funcione inmediatamente
        np.random.seed(42)
        skus = [f"SKU_{i}" for i in range(100)]
        categorias = ["Cosmetics", "Skincare", "Haircare"]
        return pd.DataFrame({
            "SKU": skus,
            "Product type": np.random.choice(categorias, 100),
            "Price": np.random.uniform(10, 150, 100).round(2),
            "Availability": np.random.randint(0, 100, 100),
            "Number of products sold": np.random.randint(50, 500, 100),
            "Lead times": np.random.randint(1, 30, 100),
            "Shipping costs": np.random.uniform(5, 40, 100).round(2)
        })

@st.cache_data(ttl=600)
def cargar_datos_calidad():
    if os.path.exists("quality_inspection.csv"):
        return pd.read_csv("quality_inspection.csv")
    else:
        # Datos simulados de inspección y tolerancias
        np.random.seed(42)
        muestras = range(1, 101)
        # Simulación de mediciones de un componente (ej. diámetro o ensamble de espejo lateral en mm)
        mediciones = np.random.normal(50.0, 0.15, 100)
        defectos = ["Ninguno" if m < 50.25 and m > 49.75 else np.random.choice(["Grieta", "Porosidad", "Acabado"]) for m in mediciones]
        return pd.DataFrame({
            "Muestra": muestras,
            "Medicion": mediciones,
            "Defecto": defectos,
            "Temperatura_Sensor": np.random.normal(75, 5, 100),
            "Presion_Sensor": np.random.normal(120, 10, 100)
        })

@st.cache_data(ttl=600)
def cargar_datos_mantenimiento():
    if os.path.exists("predictive_maintenance.csv"):
        return pd.read_csv("predictive_maintenance.csv")
    else:
        # Datos simulados de salud de maquinaria CNC / Fresadora
        np.random.seed(42)
        return pd.DataFrame({
            "UDI": range(1, 201),
            "Air temperature [K]": np.random.uniform(295, 305, 200).round(1),
            "Process temperature [K]": np.random.uniform(305, 315, 200).round(1),
            "Rotational speed [rpm]": np.random.normal(1500, 150, 200).astype(int),
            "Torque [Nm]": np.random.normal(40, 10, 200).round(1),
            "Tool wear [min]": np.random.randint(0, 240, 200),
            "Machine failure": np.random.choice([0, 1], 200, p=[0.96, 0.04])
        })

# ─── 4. ESTRUCTURA DE LA BARRA LATERAL (MENÚ PRINCIPAL) ─────────────────────
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0056b3 !important;'>Industrial OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:12px; margin-top:-10px;'>Planta Central Gerencial</p>", unsafe_allow_html=True)
    st.divider()
    
    # Selector del área analítica de la empresa
    modulo = st.radio(
        "ÁREA DE OPERACIONES",
        ["📦 Cadena de Suministro e Inventario", "🔬 Analítica de Calidad", "⚙️ Mantenimiento Predictivo"]
    )
    st.divider()
    
    # Indicador dinámico del origen de datos
    st.markdown("<div style='font-size: 11px; font-weight: 500;'>ESTADO DE CONEXIÓN:</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: CADENA DE SUMINISTRO E INVENTARIOS
# ══════════════════════════════════════════════════════════════════════════════
if modulo == "📦 Cadena de Suministro e Inventario":
    st.title("📦 Business Intelligence: Inventario y Logística")
    
    df_inv = cargar_datos_inventario()
    
    # Verificación visual de fuente de datos en el sidebar
    with st.sidebar:
        if "supply_chain_data.csv" in os.listdir("."):
            st.success("Conectado a dataset real de Kaggle")
        else:
            st.caption("Usando simulación avanzada (Suministra tu archivo 'supply_chain_data.csv')")

    # Cálculos analíticos clave para ingeniería industrial (Clasificación ABC Dinámica)
    df_inv["Valor_Ventas"] = df_inv["Price"] * df_inv["Number of products sold"]
    df_inv = df_inv.sort_values(by="Valor_Ventas", ascending=False).reset_index(drop=True)
    df_inv["Acumulado"] = df_inv["Valor_Ventas"].cumsum()
    total_valor = df_inv["Valor_Ventas"].sum()
    df_inv["Porcentaje_Acumulado"] = (df_inv["Acumulado"] / total_valor) * 100
    
    # Asignación de zonas ABC basadas en Pareto
    df_inv["Clasificacion_ABC"] = df_inv["Porcentaje_Acumulado"].apply(
        lambda x: "Clase A (Crítico)" if x <= 80 else ("Clase B (Medio)" if x <= 95 else "Clase C (Bajo)")
    )

    # Fila superior de Indicadores (KPIs)
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Productos Totales</div><div class='kpi-val'>{len(df_inv)}</div><div class='kpi-subtext' style='color:#0056b3;'>SKUs en Catálogo</div></div>", unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Valor de Movimiento</div><div class='kpi-val'>${total_valor:,.2f}</div><div class='kpi-subtext'>Cálculo de Demanda</div></div>", unsafe_allow_html=True)
    with kpi_col3:
        # Contar artículos que requieren atención por bajo inventario
        bajo_stock = len(df_inv[df_inv["Availability"] < 15])
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Riesgo de Quiebre</div><div class='kpi-val' style='color:#fd7e14;'>{bajo_stock}</div><div class='kpi-subtext' style='color:#fd7e14;'>Stock Menor a 15 u.</div></div>", unsafe_allow_html=True)
    with kpi_col4:
        lead_time_prom = df_inv["Lead times"].mean()
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Lead Time Promedio</div><div class='kpi-val'>{lead_time_prom:.1f} d</div><div class='kpi-subtext'>Tiempo de Respuesta</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Análisis de Distribución y Pareto de Inventarios</div>", unsafe_allow_html=True)
    
    layout_graficos_inv = st.columns([1.5, 1])
    with layout_graficos_inv[0]:
        st.subheader("Análisis de Pareto Dinámico (Clasificación ABC)")
        fig_abc = px.bar(
            df_inv, x=df_inv.index, y="Valor_Ventas", color="Clasificacion_ABC",
            labels={"x": "Productos ordenados por valor", "Valor_Ventas": "Ingresos por Ventas ($)"},
            color_discrete_sequence=["#0056b3", "#fd7e14", "#28a745"]
        )
        fig_abc.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=10, r=10, t=20, b=10))
        st.plotly_chart(fig_abc, use_container_width=True)
        
    with layout_graficos_inv[1]:
        st.subheader("Costos Logísticos por Tipo de Producto")
        fig_costos = px.box(
            df_inv, x="Product type", y="Shipping costs", 
            points="all", color="Product type", color_discrete_sequence=LIGHT_THETheme_COLORS if 'LIGHT_THETheme_COLORS' in locals() else LIGHT_THEME_COLORS
        )
        fig_costos.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", showlegend=False)
        st.plotly_chart(fig_costos, use_container_width=True)

    st.subheader("📋 Matriz de Control de Inventario General")
    st.dataframe(df_inv[["SKU", "Product type", "Price", "Availability", "Number of products sold", "Clasificacion_ABC", "Valor_Ventas"]], use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: ANALÍTICA DE CALIDAD (CONTROL DE PROCESOS)
# ══════════════════════════════════════════════════════════════════════════════
elif modulo == "🔬 Analítica de Calidad":
    st.title("🔬 Quality Analytics: Control Estadístico de Procesos")
    
    df_cal = cargar_datos_calidad()
    
    with st.sidebar:
        if "quality_inspection.csv" in os.listdir("."):
            st.success("Conectado a dataset de Inspección real")
        else:
            st.caption("Usando simulación avanzada (Suministra tu archivo 'quality_inspection.csv')")

    # Algoritmia avanzada para Control de Calidad: Límites Estadísticos Reales (±3 Sigma)
    promedio_proceso = df_cal["Medicion"].mean()
    desviacion_proceso = df_cal["Medicion"].std()
    
    lcs = promedio_proceso + (3 * desviacion_proceso) # Límite de Control Superior
    lci = promedio_proceso - (3 * desviacion_proceso) # Límite de Control Inferior
    
    # Simulación de límites de especificación de diseño para el Cp/Cpk (Tolerancias de ingeniería)
    les = promedio_proceso + 0.40 
    lei = promedio_proceso - 0.40
    
    # Índices de capacidad del proceso (Métricas cruciales para auditorías PPAP/APQP)
    cp = (les - lei) / (6 * desviacion_proceso)
    cpk = min((les - promedio_proceso)/(3 * desviacion_proceso), (promedio_proceso - lei)/(3 * desviacion_proceso))

    # Fila superior de Indicadores de Calidad
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Media del Proceso</div><div class='kpi-val'>{promedio_proceso:.3f} mm</div><div class='kpi-subtext' style='color:#0056b3;'>Dimensión Promedio</div></div>", unsafe_allow_html=True)
    with kpi_col2:
        Tasa_defectos = (len(df_cal[df_cal["Defecto"] != "Ninguno"]) / len(df_cal)) * 100
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Tasa de Defectos</div><div class='kpi-val' style='color:#dc3545;'>{tasa_defectos:.1f}%</div><div class='kpi-subtext' style='color:#dc3545;'>Unidades Rechazadas</div></div>", unsafe_allow_html=True)
    with kpi_col3:
        color_cp = "#28a745" if cp >= 1.33 else "#fd7e14"
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Índice de Capacidad (Cp)</div><div class='kpi-val' style='color:{color_cp};'>{cp:.2f}</div><div class='kpi-subtext'>Potencial del Proceso</div></div>", unsafe_allow_html=True)
    with kpi_col4:
        color_cpk = "#28a745" if cpk >= 1.33 else "#dc3545"
        status_cpk = "Proceso Capable" if cpk >= 1.33 else "Proceso No Centrado"
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Capacidad Real (Cpk)</div><div class='kpi-val' style='color:{color_cpk};'>{cpk:.2f}</div><div class='kpi-subtext' style='color:{color_cpk};'>{status_cpk}</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Gráficos de Control Estadístico en Tiempo Real</div>", unsafe_allow_html=True)
    
    # Construcción de Gráfico de Control Tipo Shewhart (X-bar) con Plotly
    fig_control = go.Figure()
    fig_control.add_trace(go.Scatter(x=df_cal["Muestra"], y=df_cal["Medicion"], mode="lines+markers", name="Medición Pieza", line=dict(color="#0056b3", width=2)))
    fig_control.add_hline(y=promedio_proceso, line_dash="dash", line_color="#28a745", annotation_text="Línea Central (Media)")
    fig_control.add_hline(y=lcs, line_dash="dot", line_color="#dc3545", annotation_text="LCS (+3σ)")
    fig_control.add_hline(y=lci, line_dash="dot", line_color="#dc3545", annotation_text="LCI (-3σ)")
    
    fig_control.update_layout(
        title="Carta de Control de Variabilidad Estadístico (Muestreo Secuencial)",
        plot_bgcolor="#ffffff", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(gridcolor="#f1f3f5", title="Número de Muestra"), yaxis=dict(gridcolor="#f1f3f5", title="Dimensión Analizada")
    )
    st.plotly_chart(fig_control, use_container_width=True)

    layout_inferior_cal = st.columns(2)
    with layout_inferior_cal[0]:
        st.subheader("Análisis de Pareto: Modos de Falla Frecuentes")
        df_defectos = df_cal[df_cal["Defecto"] != "Ninguno"]["Defecto"].value_counts().reset_index()
        if not df_defectos.empty:
            fig_pareto_defectos = px.bar(df_defectos, x="index", y="Defecto", labels={"index": "Tipo de Defecto", "Defecto": "Frecuencia de Ocurrencia"}, color_discrete_sequence=["#fd7e14"])
            fig_pareto_defectos.update_layout(plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pareto_defectos, use_container_width=True)
        else:
            st.info("No se registran defectos en la corrida actual. Excelente estabilidad.")
            
    with layout_inferior_cal[1]:
        st.subheader("Correlación: Temperatura del Proceso vs Variación Física")
        fig_corr = px.scatter(df_cal, x="Temperatura_Sensor", y="Medicion", color="Defecto", color_discrete_sequence=["#28a745", "#dc3545", "#fd7e14", "#6f42c1"])
        fig_corr.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_corr, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 3: MANTENIMIENTO PREDICTIVO
# ══════════════════════════════════════════════════════════════════════════════
else:
    st.title("⚙️ Mantenimiento Predictivo & Monitoreo de Maquinaria")
    
    df_maint = cargar_datos_mantenimiento()
    
    with st.sidebar:
        if "predictive_maintenance.csv" in os.listdir("."):
            st.success("Conectado a dataset de Sensores real")
        else:
            st.caption("Usando simulación avanzada (Suministra tu archivo 'predictive_maintenance.csv')")

    # KPIs de la Salud General del Taller / Célula de Manufactura
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Total Registros Monitoreados</div><div class='kpi-val'>{len(df_maint)}</div><div class='kpi-subtext' style='color:#0056b3;'>Horas de Operación</div></div>", unsafe_allow_html=True)
    with kpi_col2:
        fallas_reales = df_maint["Machine failure"].sum()
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Anomalías / Fallas</div><div class='kpi-val' style='color:#dc3545;'>{fallas_reales}</div><div class='kpi-subtext' style='color:#dc3545;'>Paros Críticos del Sistema</div></div>", unsafe_allow_html=True)
    with kpi_col3:
        max_tool_wear = df_maint["Tool wear [min]"].max()
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Desgaste Máx. Herramienta</div><div class='kpi-val'>{max_tool_wear} min</div><div class='kpi-subtext' style='color:#fd7e14;'>Vida Útil Remanente</div></div>", unsafe_allow_html=True)
    with kpi_col4:
        Oee_estimado = ((len(df_maint) - fallas_reales) / len(df_maint)) * 100
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Disponibilidad (Proxy OEE)</div><div class='kpi-val' style='color:#28a745;'>{oee_estimado:.1f}%</div><div class='kpi-subtext'>Eficiencia de Equipos</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Análisis de Telemetría Industrial para Prevención de Paros</div>", unsafe_allow_html=True)
    
    layout_graficos_maint = st.columns(2)
    with layout_graficos_maint[0]:
        st.subheader("Distribución Operativa: Torque vs Velocidad Rotación (RPM)")
        # Gráfico que identifica en qué áreas de trabajo se producen las fallas mecánicas de la máquina
        fig_scatter_maint = px.scatter(
            df_maint, x="Rotational speed [rpm]", y="Torque [Nm]",
            color=df_maint["Machine failure"].astype(str),
            color_discrete_map={"0": "#0056b3", "1": "#dc3545"},
            labels={"0": "Operación Normal", "1": "Falla del Equipo"}
        )
        fig_scatter_maint.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_scatter_maint, use_container_width=True)
        
    with layout_graficos_maint[1]:
        st.subheader("Curva de Degradación: Desgaste de Herramienta")
        # Histograma industrial para planear cuándo programar un cambio rápido (SMED) antes de romper la herramienta
        fig_hist_wear = px.histogram(
            df_maint, x="Tool wear [min]", color="Machine failure",
            color_discrete_map={0: "#28a745", 1: "#dc3545"},
            nbins=30
        )
        fig_hist_wear.update_layout(plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_hist_wear, use_container_width=True)

    st.subheader("🚨 Registro de Telemetría para Inspección en Planta")
    st.dataframe(df_maint.sort_values(by="Machine failure", ascending=False), use_container_width=True, hide_index=True)

# ─── 5. PIE DE PÁGINA CORPORATIVO ───────────────────────────────────────────
st.divider()
st.caption("🏭 Industrial Intelligence OS · Sistema Unificado de Gestión de Operaciones · Portafolio Avanzado de Ingeniería Industrial.")