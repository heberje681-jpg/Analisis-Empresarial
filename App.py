"""
🏭 Industrial Intelligence OS - Dashboard Unificado de Operaciones
Diseño Avanzado en Tema Claro · Enfoque Analítico de Toma de Decisiones
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
.stApp { background-color: #f8f9fa; color: #212529; font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e9ecef; }
section[data-testid="stSidebar"] * { color: #495057 !important; }
h1, h2, h3 { color: #1a2530 !important; font-weight: 600 !important; letter-spacing: -0.02em; }
.kpi-box { background-color: #ffffff; border: 1px solid #e9ecef; border-radius: 10px; padding: 20px; text-align: left; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02); margin-bottom: 15px; }
.kpi-lbl { font-size: 11px; color: #6c757d; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600; }
.kpi-val { font-family: 'JetBrains Mono', monospace; font-size: 30px; font-weight: 600; color: #0056b3; margin-top: 4px; }
.kpi-subtext { font-size: 12px; color: #28a745; margin-top: 4px; font-weight: 500; }
.section-header { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #495057; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 2px solid #e9ecef; padding-bottom: 5px; margin-bottom: 15px; margin-top: 10px; }
</style>""", unsafe_allow_html=True)

LIGHT_THEME_COLORS = ["#0056b3", "#28a745", "#fd7e14", "#6f42c1", "#e83e8c", "#17a2b8"]

# ─── 3. FUNCIONES DE CARGA DE DATOS (CON AUTO-MAPEO) ───────────────────────
@st.cache_data(ttl=600)
def cargar_datos_inventario():
    if os.path.exists("supply_chain_data.csv"):
        return pd.read_csv("supply_chain_data.csv")
    else:
        np.random.seed(42)
        skus = [f"SKU_{i}" for i in range(100)]
        categorias = ["Cosmetics", "Skincare", "Haircare"]
        return pd.DataFrame({
            "SKU": skus, "Product type": np.random.choice(categorias, 100),
            "Price": np.random.uniform(10, 150, 100).round(2), "Availability": np.random.randint(0, 100, 100),
            "Number of products sold": np.random.randint(50, 500, 100), "Lead times": np.random.randint(1, 30, 100),
            "Shipping costs": np.random.uniform(5, 40, 100).round(2)
        })

@st.cache_data(ttl=600)
def cargar_datos_calidad():
    if os.path.exists("quality_inspection.csv"):
        df = pd.read_csv("quality_inspection.csv")
        cols = df.columns.tolist()
        cols_num = df.select_dtypes(include=np.number).columns.tolist()
        cols_cat = df.select_dtypes(exclude=np.number).columns.tolist()
        
        if "Medicion" not in cols:
            df["Medicion"] = df[cols_num[0]] if len(cols_num) > 0 else np.random.normal(50.0, 0.15, len(df))
        if "Defecto" not in cols:
            df["Defecto"] = df[cols_cat[0]] if len(cols_cat) > 0 else "Ninguno"
        if "Temperatura_Sensor" not in cols:
            df["Temperatura_Sensor"] = df[cols_num[1]] if len(cols_num) > 1 else np.random.normal(75, 5, len(df))
        if "Presion_Sensor" not in cols:
            df["Presion_Sensor"] = df[cols_num[2]] if len(cols_num) > 2 else np.random.normal(120, 10, len(df))
        if "Muestra" not in cols:
            df["Muestra"] = range(1, len(df) + 1)
            
        return df
    else:
        np.random.seed(42)
        muestras = range(1, 101)
        mediciones = np.random.normal(50.0, 0.15, 100)
        defectos = ["Ninguno" if m < 50.25 and m > 49.75 else np.random.choice(["Grieta", "Porosidad", "Acabado"]) for m in mediciones]
        return pd.DataFrame({
            "Muestra": muestras, "Medicion": mediciones, "Defecto": defectos,
            "Temperatura_Sensor": np.random.normal(75, 5, 100), "Presion_Sensor": np.random.normal(120, 10, 100)
        })

@st.cache_data(ttl=600)
def cargar_datos_mantenimiento():
    if os.path.exists("predictive_maintenance.csv"):
        df = pd.read_csv("predictive_maintenance.csv")
        if "Target" in df.columns and "Machine failure" not in df.columns:
            df.rename(columns={"Target": "Machine failure"}, inplace=True)
        return df
    else:
        np.random.seed(42)
        return pd.DataFrame({
            "UDI": range(1, 201), "Air temperature [K]": np.random.uniform(295, 305, 200).round(1),
            "Process temperature [K]": np.random.uniform(305, 315, 200).round(1), "Rotational speed [rpm]": np.random.normal(1500, 150, 200).astype(int),
            "Torque [Nm]": np.random.normal(40, 10, 200).round(1), "Tool wear [min]": np.random.randint(0, 240, 200),
            "Machine failure": np.random.choice([0, 1], 200, p=[0.96, 0.04])
        })

# ─── 4. ESTRUCTURA DE LA BARRA LATERAL (MENÚ PRINCIPAL) ─────────────────────
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0056b3 !important;'>Industrial OS</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size:12px; margin-top:-10px;'>Planta Central Gerencial</p>", unsafe_allow_html=True)
    st.divider()
    
    modulo = st.radio(
        "ÁREA DE OPERACIONES",
        ["📦 Cadena de Suministro e Inventario", "🔬 Analítica de Calidad", "⚙️ Mantenimiento Predictivo"]
    )
    st.divider()
    st.markdown("<div style='font-size: 11px; font-weight: 500;'>ESTADO DE CONEXIÓN:</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 1: CADENA DE SUMINISTRO E INVENTARIOS (Pareto Corregido)
# ══════════════════════════════════════════════════════════════════════════════
if modulo == "📦 Cadena de Suministro e Inventario":
    st.title("📦 Business Intelligence: Inventario y Logística")
    
    df_inv = cargar_datos_inventario()
    
    with st.sidebar:
        if "supply_chain_data.csv" in os.listdir("."):
            st.success("Conectado a dataset real de Kaggle")
        else:
            st.caption("Usando simulación avanzada")

    # Mapeo dinámico de nombres de columnas de Kaggle (Manejo de errores seguro)
    sales_col = "Number of products sold" if "Number of products sold" in df_inv.columns else (df_inv.columns[4] if len(df_inv.columns) > 4 else "Sales")
    price_col = "Price" if "Price" in df_inv.columns else "Price"
    sku_col = "SKU" if "SKU" in df_inv.columns else df_inv.columns[0]
    avail_col = "Availability" if "Availability" in df_inv.columns else "Availability"
    lead_col = "Lead times" if "Lead times" in df_inv.columns else "Lead times"
    ship_col = "Shipping costs" if "Shipping costs" in df_inv.columns else "Shipping costs"
    type_col = "Product type" if "Product type" in df_inv.columns else "Product type"

    df_inv["Valor_Ventas"] = df_inv[price_col] * df_inv[sales_col]
    df_inv = df_inv.sort_values(by="Valor_Ventas", ascending=False).reset_index(drop=True)
    df_inv["Acumulado"] = df_inv["Valor_Ventas"].cumsum()
    total_valor = df_inv["Valor_Ventas"].sum()
    df_inv["Porcentaje_Acumulado"] = (df_inv["Acumulado"] / total_valor) * 100
    
    df_inv["Clasificacion_ABC"] = df_inv["Porcentaje_Acumulado"].apply(
        lambda x: "Clase A (Crítico)" if x <= 80 else ("Clase B (Medio)" if x <= 95 else "Clase C (Bajo)")
    )

    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    with kpi_col1:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Productos Totales</div><div class='kpi-val'>{len(df_inv)}</div><div class='kpi-subtext' style='color:#0056b3;'>SKUs en Catálogo</div></div>", unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Valor de Movimiento</div><div class='kpi-val'>${total_valor:,.2f}</div><div class='kpi-subtext'>Cálculo de Demanda</div></div>", unsafe_allow_html=True)
    with kpi_col3:
        bajo_stock = len(df_inv[df_inv[avail_col] < 15]) if avail_col in df_inv.columns else 0
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Riesgo de Quiebre</div><div class='kpi-val' style='color:#fd7e14;'>{bajo_stock}</div><div class='kpi-subtext' style='color:#fd7e14;'>Stock Menor a 15 u.</div></div>", unsafe_allow_html=True)
    with kpi_col4:
        lead_time_prom = df_inv[lead_col].mean() if lead_col in df_inv.columns else 0
        st.markdown(f"<div class='kpi-box'><div class='kpi-lbl'>Lead Time Promedio</div><div class='kpi-val'>{lead_time_prom:.1f} d</div><div class='kpi-subtext'>Tiempo de Respuesta</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Análisis de Distribución y Pareto de Inventarios</div>", unsafe_allow_html=True)
    
    layout_graficos_inv = st.columns([1.6, 1])
    with layout_graficos_inv[0]:
        st.subheader("Análisis de Pareto Dinámico (Doble Eje con Curva Acumulada)")
        
        # 🌟 CONSTRUCCIÓN DEL DIAGRAMA DE PARETO COMPLETO (DOBLE EJE) 🌟
        fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Asignar colores a las barras según clasificación ABC
        color_map = {"Clase A (Crítico)": "#0056b3", "Clase B (Medio)": "#fd7e14", "Clase C (Bajo)": "#28a745"}
        bar_colors = df_inv["Clasificacion_ABC"].map(color_map).tolist()
        
        # Eje Y Izquierdo: Barras de Ventas Individuales
        fig_pareto.add_trace(
            go.Bar(
                x=df_inv[sku_col], y=df_inv["Valor_Ventas"],
                name="Ventas Individuales ($)", marker_color=bar_colors,
                hovertemplate="<b>SKU: %{x}</b><br>Ventas: $%{y:,.2f}<extra></extra>"
            ), secondary_y=False
        )
        
        # Eje Y Derecho: Línea de Porcentaje Acumulado (Curva de Pareto)
        fig_pareto.add_trace(
            go.Scatter(
                x=df_inv[sku_col], y=df_inv["Porcentaje_Acumulado"],
                name="% Acumulado", mode="lines+markers",
                line=dict(color="#dc3545", width=2.5), marker=dict(size=4),
                hovertemplate="<b>Porcentaje Acumulado:</b> %{y:.1f}%<extra></extra>"
            ), secondary_y=True
        )
        
        # Línea guía de corte del 80% analítico
        fig_pareto.add_hline(y=80, line_dash="dash", line_color="#dc3545", opacity=0.7, secondary_y=True)

        fig_pareto.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=20, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, x
