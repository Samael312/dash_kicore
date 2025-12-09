import streamlit as st
from config.settings import Settings
from backend.api_clients import CoreClient
from backend.data_service import process_devices, process_m2m

# Importamos las nuevas vistas
from frontend.views import devices_view, m2m_view

# --- CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Dashboard Flota", layout="wide", page_icon="📊")

# --- GESTIÓN DE SESIÓN ---
if 'token' not in st.session_state:
    st.session_state['token'] = None

if not st.session_state['token']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Login Core")
        if st.button("Conectar con Credenciales (.env)"):
            with st.spinner("Autenticando..."):
                client = CoreClient()
                token = client.login()
                if token:
                    st.session_state['token'] = token
                    st.rerun()
                else:
                    st.error("Error de conexión. Revisa usuario/pass en .env")
    st.stop()

# --- CARGA DE DATOS ---
client = CoreClient(st.session_state['token'])

with st.spinner("Descargando datos de la flota..."):
    # Descargamos
    raw_dev = client.get_devices()
    raw_m2m = client.get_m2m()
    
    # Procesamos (Limpieza en data_service)
    df_dev = process_devices(raw_dev)
    df_m2m = process_m2m(raw_m2m)

# --- INTERFAZ GRÁFICA ---
# Sidebar
with st.sidebar:
    st.title("Kiconex Dashboard")
    st.success("🟢 Conectado")
    if st.button("Cerrar Sesión"):
        st.session_state['token'] = None
        st.rerun()

# Pestañas principales
tab1, tab2 = st.tabs(["📡 Dispositivos", "📶 Comunicaciones M2M"])

with tab1:
    # Delegamos el pintado a la vista de dispositivos
    devices_view.render(df_dev)

with tab2:
    # Delegamos el pintado a la vista de M2M
    m2m_view.render(df_m2m)