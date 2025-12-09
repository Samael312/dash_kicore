import streamlit as st
import plotly.express as px

def render(df_dev):
    """
    Renderiza la vista completa de dispositivos.
    Recibe el DataFrame de dispositivos limpio.
    """
    st.header("Gestión de Dispositivos")
    
    if df_dev.empty:
        st.warning("No hay datos de dispositivos para mostrar.")
        return

    # --- FILTROS ---
    orgs = ["Todas"]
    if 'organization' in df_dev.columns:
        orgs += list(df_dev['organization'].unique())
        
    selected_org = st.selectbox("Filtrar por Organización (Tenant ID)", orgs, key="dev_org_filter")
    
    # Aplicar filtro
    df_filtered = df_dev.copy()
    if selected_org != "Todas":
        df_filtered = df_filtered[df_filtered['organization'] == selected_org]
    
    st.divider()

    # --- GRÁFICOS ---
    col1, col2 = st.columns(2)
    
    # Gráfico 1: Modelos
    with col1:
        st.subheader("Modelos (Tipo)")
        if 'model' in df_filtered.columns:
            st.plotly_chart(px.histogram(df_filtered, x='model', title="Distribución por Tipo"), use_container_width=True)
            
    # Gráfico 2: Estado Conexión
    with col2:
        st.subheader("Estado Instalaciones")
        if 'status' in df_filtered.columns:
            st.plotly_chart(px.pie(df_filtered, names='status', title="Conectados vs Desconectados"), use_container_width=True)
            
    # Gráfico Extra: Habilitados
    if 'enabled' in df_filtered.columns:
        st.subheader("Dispositivos Habilitados")
        st.plotly_chart(px.pie(df_filtered, names='enabled', title="Habilitado vs Deshabilitado"), use_container_width=True)