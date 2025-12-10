import streamlit as st
import plotly.express as px
import pandas as pd

# =====================================================
#  1. ESTILOS CSS
# =====================================================
def load_custom_css():
    st.markdown("""
        <style>
        .stApp { background-color: #ffffff; font-family: 'Segoe UI', sans-serif; }

        /* Contenedores de Métricas */
        div[data-testid="stMetric"] {
            background-color: #f8f9fa; 
            border: 1px solid #e9ecef;
            border-left: 5px solid #002b5c; 
            padding: 10px; 
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Títulos */
        h3 { color: #002b5c !important; font-weight: 700; border-bottom: 2px solid #eee; padding-bottom: 10px; }
        h4 { color: #004b8d !important; font-weight: 600; }
        </style>
    """, unsafe_allow_html=True)

# =====================================================
#  2. DETECCIÓN DE TIPO DE DISPOSITIVO
# =====================================================
def detect_device_type(df):
    if df is None or df.empty:
        return "Dispositivos"
    cols = df.columns
    if "physical_id" in cols or "ki_id" in cols:
        return "🛠️ Boards"
    elif "ssid" in cols or "mac" in cols:
        return "Kiwi"
    return "📟 Dispositivos"

# =====================================================
#  3. FUNCIÓN DE RENDERIZADO (ÚNICA)
# =====================================================
def render(df):
    load_custom_css()

    if df is None or df.empty:
        st.warning("⚠️ No hay datos disponibles para mostrar en esta sección.")
        st.divider()
        return

    title_prefix = detect_device_type(df)
    st.markdown(f"### {title_prefix}")

    # Columnas requeridas para procesado
    required_cols = ["organization", "model", "status_clean", "enabled_clean"]
    if not all(col in df.columns for col in required_cols):
        st.error(f"Error: El DataFrame de {title_prefix} no tiene las columnas procesadas requeridas.")
        st.dataframe(df.head())
        st.divider()
        return

    # --- FILTROS ---
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            orgs = ["Todas"] + sorted(df["organization"].fillna("Sin Asignar").astype(str).unique())
            sel_org = st.selectbox(f"🏢 Organización - {title_prefix}", orgs, key=f"org_{title_prefix}")
        df_temp = df if sel_org == "Todas" else df[df["organization"] == sel_org]
        with c2:
            models = ["Todos"] + sorted(df_temp["model"].fillna("Genérico").astype(str).unique())
            sel_model = st.selectbox(f"📦 Modelo - {title_prefix}", models, key=f"mod_{title_prefix}")

    # Aplicar filtros
    df_filt = df_temp if sel_model == "Todos" else df_temp[df_temp["model"] == sel_model]

    st.markdown("<br>", unsafe_allow_html=True)

    # --- KPIs ---
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Dispositivos", len(df_filt))
    k2.metric("Conectados", len(df_filt[df_filt["status_clean"] == "Conectado"]))
    k3.metric("Habilitados", len(df_filt[df_filt["enabled_clean"] == "Habilitado"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- GRÁFICOS ---
    st.markdown(f"#### 📊 Distribución por Modelo ({title_prefix})")
    df_chart = df_filt["model"].value_counts().reset_index()
    df_chart.columns = ["Modelo", "Cantidad"]
    if not df_chart.empty:
        fig_hist = px.bar(
            df_chart, x="Modelo", y="Cantidad", text_auto=True,
            color="Cantidad", color_continuous_scale=px.colors.sequential.Blues
        )
        fig_hist.update_layout(plot_bgcolor='rgba(0,0,0,0)', height=300, showlegend=False, xaxis_title=None)
        st.plotly_chart(fig_hist, use_container_width=True)

    # Tartas de Estado
    col_pie1, col_pie2 = st.columns(2)
    color_map_conn = {"Conectado": "#002b5c", "Desconectado": "#cbd5e1"}
    color_map_enb = {"Habilitado": "#0074d9", "Deshabilitado": "#e1e1e1"}

    with col_pie1:
        st.caption("Estado de Conectividad")
        if not df_filt.empty:
            fig1 = px.pie(df_filt, names="status_clean", hole=0.5, color="status_clean", color_discrete_map=color_map_conn)
            fig1.update_traces(textinfo='percent+label')
            fig1.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)

    with col_pie2:
        st.caption("Estado de Habilitación")
        if not df_filt.empty:
            fig2 = px.pie(df_filt, names="enabled_clean", hole=0.5, color="enabled_clean", color_discrete_map=color_map_enb)
            fig2.update_traces(textinfo='percent+label')
            fig2.update_layout(height=250, margin=dict(t=10,b=10,l=10,r=10), showlegend=False)
            st.plotly_chart(fig2, use_container_width=True)

    # Tabla completa
    with st.expander(f"📂 Ver listado completo de {title_prefix}", expanded=False):
        st.dataframe(df_filt, use_container_width=True)

    st.divider()
