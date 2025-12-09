import streamlit as st
import plotly.express as px
import pandas as pd

def render(df_m2m):
    """
    Renderiza la vista completa de M2M.
    Recibe el DataFrame de M2M limpio.
    """
    st.header("Gestión de Comunicaciones (M2M)")
    
    if df_m2m.empty:
        st.info("No hay datos M2M disponibles.")
        return

    # --- FILTROS ---
    orgs = ["Todas"]
    if 'organization' in df_m2m.columns:
        orgs += list(df_m2m['organization'].unique())
        
    sel_org = st.selectbox("Filtrar por Grupo Comercial", orgs, key="m2m_org_filter")
    
    df_filt = df_m2m.copy()
    if sel_org != "Todas":
        df_filt = df_filt[df_filt['organization'] == sel_org]
        
    st.divider()
        
    # --- KPIs SUPERIORES ---
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("Total SIMs", len(df_filt))
    
    # Conteo de alarmas
    total_alarmas = 0
    if 'alarms' in df_filt.columns:
        # Ajustar lógica según el formato real de alarms (lista, bool o int)
        total_alarmas = df_filt['alarms'].astype(bool).sum() 
    kpi2.metric("Dispositivos con Alarmas", int(total_alarmas))
    
    st.divider()

    # --- GRÁFICOS PRINCIPALES ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Estado")
        if 'status_clean' in df_filt.columns:
            st.plotly_chart(px.pie(df_filt, names='status_clean', hole=0.4), use_container_width=True)
        
    with col2:
        st.subheader("Plan de Servicios")
        if 'rate_plan' in df_filt.columns:
            st.plotly_chart(px.pie(df_filt, names='rate_plan'), use_container_width=True)
        
    with col3:
        st.subheader("Tipo de Red")
        if 'network_type' in df_filt.columns:
            st.plotly_chart(px.pie(df_filt, names='network_type'), use_container_width=True)

    # --- ANÁLISIS DE CONSUMOS ---
    st.subheader("📊 Análisis de Consumo Diario")
    
    if 'consumptionDaily' in df_filt.columns:
        try:
            # Conversión a numérico segura
            df_filt['num_consumo'] = pd.to_numeric(df_filt['consumptionDaily'], errors='coerce').fillna(0)
            
            c_min = df_filt['num_consumo'].min()
            c_avg = df_filt['num_consumo'].mean()
            c_max = df_filt['num_consumo'].max()
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Mínimo", f"{c_min:.2f}")
            m2.metric("Medio", f"{c_avg:.2f}")
            m3.metric("Máximo", f"{c_max:.2f}")
            
            st.plotly_chart(px.histogram(df_filt, x='num_consumo', title="Histograma de Consumo"), use_container_width=True)
            
        except Exception as e:
            st.warning("No se pudieron calcular estadísticas numéricas del consumo.")
    
    with st.expander("Ver tabla completa de datos M2M"):
        st.dataframe(df_filt)