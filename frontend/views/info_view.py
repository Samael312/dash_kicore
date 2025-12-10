import streamlit as st
import plotly.express as px
import pandas as pd

# =====================================================
#  1. ESTILOS CSS (TU CSS PROPORCIONADO)
# =====================================================
def load_custom_css():
    st.markdown("""
        <style>
        /* Tipografía y Fondo */
        .stApp {
            background-color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #002b5c !important; /* Azul Oscuro Corporativo */
            font-weight: 700;
        }
        
        /* Contenedor de la Leyenda Personalizada */
        .custom-legend-box {
            background-color: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 15px;
            max-height: 400px; /* Altura fija */
            overflow-y: auto;  /* Scroll vertical */
            box-shadow: inset 0 0 5px rgba(0,0,0,0.05);
        }

        /* Items de la Leyenda */
        .legend-row {
            display: flex;
            align-items: center;
            padding: 8px 0;
            border-bottom: 1px solid #eee;
            font-size: 13px;
            transition: background 0.2s;
        }
        .legend-row:hover {
            background-color: #eaeef3; /* Efecto hover sutil */
            border-radius: 4px;
        }

        /* Indicador de Color (Puntito) */
        .color-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%; /* Círculo perfecto */
            margin-right: 12px;
            flex-shrink: 0;
            border: 1px solid rgba(0,0,0,0.1);
        }

        /* Texto de la etiqueta */
        .label-text {
            flex-grow: 1;
            color: #333;
            font-weight: 500;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis; /* Puntos suspensivos si es muy largo */
            margin-right: 10px;
        }

        /* Valor numérico */
        .value-text {
            color: #002b5c;
            font-weight: 700;
            font-size: 12px;
        }

        /* Scrollbar Personalizada */
        .custom-legend-box::-webkit-scrollbar {
            width: 6px;
        }
        .custom-legend-box::-webkit-scrollbar-track {
            background: transparent; 
        }
        .custom-legend-box::-webkit-scrollbar-thumb {
            background: #cbd5e1; 
            border-radius: 10px;
        }
        .custom-legend-box::-webkit-scrollbar-thumb:hover {
            background: #94a3b8; 
        }
        </style>
    """, unsafe_allow_html=True)

# =====================================================
#  3. RENDERIZADO PRINCIPAL
# =====================================================
def render(df_info):
    load_custom_css()
    
    st.markdown("## 📡 Gestión de Comunicaciones (M2M) y Software")

    if df_m2m.empty:
        st.info("No hay datos disponibles.")
        return

    # --- FILTROS (Mantenemos tu lógica existente) ---
    with st.container():
        orgs = ["Todas"]
        if "organization" in df_processed.columns:
            orgs += sorted(df_processed["organization"].astype(str).unique())
        sel_org = st.selectbox("🏢 Organización", orgs, key="m2m_org_filter")

    df_filt = df_processed.copy()
    if sel_org != "Todas":
        df_filt = df_filt[df_filt["organization"] == sel_org]

    st.markdown("---")

    # --- KPIs Generales ---
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Dispositivos", len(df_filt))
    
    # Contamos actualizados usando la nueva columna
    updated_count = len(df_filt[df_filt['status_update'] == "Actualizado"]) if 'status_update' in df_filt.columns else 0
    k2.metric("Dispositivos Actualizados", updated_count)
    
    # Calculamos porcentaje
    pct_updated = (updated_count / len(df_filt) * 100) if len(df_filt) > 0 else 0
    k3.metric("% Flota Actualizada", f"{pct_updated:.1f}%")

    st.markdown("---")

    # =====================================================
    #  NUEVA SECCIÓN: ANÁLISIS DE SOFTWARE
    # =====================================================
    
    st.markdown("### 💿 Análisis de Versiones Quiiotd")

    col_hist, col_pie = st.columns([2, 1])

    # --- GRÁFICO 1: HISTOGRAMA DE VERSIONES ---
    with col_hist:
        st.markdown("#### Distribución de Versiones")
        if 'quiiotd_version' in df_filt.columns:
            # Agrupamos para tener un conteo limpio
            version_counts = df_filt['quiiotd_version'].value_counts().reset_index()
            version_counts.columns = ['Versión', 'Cantidad']
            
            fig_ver = px.bar(
                version_counts, 
                x='Versión', 
                y='Cantidad',
                text_auto=True,
                color='Cantidad',
                color_continuous_scale=px.colors.sequential.Blues
            )
            fig_ver.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Versión Quiiotd",
                yaxis_title="Nº Dispositivos",
                height=400,
                showlegend=False
            )
            st.plotly_chart(fig_ver, use_container_width=True)
        else:
            st.warning("No se encontró la columna 'quiiotd_version'.")

    # --- GRÁFICO 2: TARTA DE ACTUALIZACIÓN ---
    with col_pie:
        st.markdown("#### Estado de Actualización")
        st.caption("Considerado actualizado si fecha >= Jun 2025")
        
        if 'status_update' in df_filt.columns:
            # Definimos colores: Verde para actualizado, Rojo/Gris para desactualizado
            color_map_update = {
                "Actualizado": "#002b5c",      # Azul Corporativo (Positivo)
                "Desactualizado": "#cbd5e1"    # Gris (Negativo/Pendiente)
            }
            
            fig_upd = px.pie(
                df_filt, 
                names='status_update', 
                hole=0.5,
                color='status_update',
                color_discrete_map=color_map_update
            )
            fig_upd.update_traces(textinfo='percent+label')
            fig_upd.update_layout(
                showlegend=True, 
                legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                margin=dict(t=20, b=50, l=20, r=20),
                height=350
            )
            st.plotly_chart(fig_upd, use_container_width=True)
        else:
            st.warning("No se pudieron calcular las fechas de compilación.")

    st.markdown("---")

    # (Aquí puedes mantener el resto de tus gráficos de consumo, país, etc. si los tienes en este archivo)
    
    # --- TABLA DE DATOS ---
    with st.expander("📂 Ver datos detallados (Incluye info de versiones)"):
        # Seleccionamos columnas relevantes para mostrar primero
        cols_to_show = [c for c in ['organization', 'model', 'quiiotd_version', 'compilation_date', 'status_update'] if c in df_filt.columns]
        # Añadimos el resto de columnas
        cols_to_show += [c for c in df_filt.columns if c not in cols_to_show]
        
        st.dataframe(df_filt[cols_to_show], use_container_width=True)