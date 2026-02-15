import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import timedelta

# Configuración de la página
st.set_page_config(layout="wide", page_title="Race Analysis Dashboard", page_icon="🏃‍♂️")

# --- FUNCIONES DE UTILIDAD ---
def hhmmss_to_seconds(hhmmss):
    """Convierte formato HH:MM:SS a segundos totales."""
    try:
        if pd.isna(hhmmss) or hhmmss == "":
            return 0
        parts = str(hhmmss).split(':')
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        return 0
    except:
        return 0

def seconds_to_hhmmss(seconds):
    """Convierte segundos a formato HH:MM:SS."""
    if pd.isna(seconds) or seconds <= 0:
        return "00:00:00"
    return str(timedelta(seconds=int(seconds)))

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # Carga el archivo JSON
    df = pd.read_json("scrapy_project/edMongo.json")
    
    # Adaptación a tus columnas específicas
    df['time_seconds'] = df['finish_time'].apply(hhmmss_to_seconds)
    
    # Crear un identificador de carrera si no existe uno único
    # Combinamos fecha, distancia y localización para el selector
    df['race_label'] = df['fecha'] + " - " + df['location'] + " (" + df['race_distance'].astype(str) + "km)"
    
    # Ordenar por tiempo
    df = df.sort_values('time_seconds')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Error al cargar el archivo: {e}")
    st.stop()

# --- SIDEBAR ---
st.sidebar.header("🎯 Filtros")

# Seleccionar Carrera
race_choice = st.sidebar.selectbox("Selecciona Evento", df['race_label'].unique())

# Seleccionar Género
gender_choice = st.sidebar.multiselect(
    "Género", 
    df['gender'].unique(), 
    default=df['gender'].unique()
)

# Filtrado
mask = (df['race_label'] == race_choice) & (df['gender'].isin(gender_choice))
df_filtered = df[mask].copy()

# --- DASHBOARD PRINCIPAL ---
st.title("🏆 Análisis de Resultados de Carrera")
st.info(f"📍 Evento: {race_choice}")

tab1, tab2 = st.tabs(["📊 Estadísticas Generales", "👤 Buscador de Corredor"])

# --- TAB 1: GENERAL ---
with tab1:
    if df_filtered.empty:
        st.warning("No hay datos disponibles.")
    else:
        # Métricas de la carrera
        col1, col2, col3, col4 = st.columns(4)
        
        m_best = df_filtered['time_seconds'].min()
        m_avg = df_filtered['time_seconds'].mean()
        
        col1.metric("Mejor Tiempo", seconds_to_hhmmss(m_best))
        col2.metric("Tiempo Medio", seconds_to_hhmmss(m_avg))
        col3.metric("Total Corredores", len(df_filtered))
        col4.metric("Distancia", f"{df_filtered['race_distance'].iloc[0]} km")

        st.divider()

        c_left, c_right = st.columns(2)

        with c_left:
            st.subheader("Distribución de Tiempos")
            fig_hist = px.histogram(
                df_filtered, 
                x="time_seconds", 
                color="gender",
                nbins=30,
                labels={'time_seconds': 'Segundos', 'count': 'Frecuencia'},
                template="plotly_dark"
            )
            st.plotly_chart(fig_hist, use_container_width=True)

        with c_right:
            st.subheader("Tiempos por Grupo de Edad")
            fig_age = px.box(
                df_filtered, 
                x="age_group", 
                y="time_seconds", 
                color="gender",
                labels={'age_group': 'Categoría/Edad', 'time_seconds': 'Segundos'}
            )
            st.plotly_chart(fig_age, use_container_width=True)

# --- TAB 2: CORREDOR ---
with tab2:
    st.subheader("🔎 Análisis Individual")
    
    runner_name = st.selectbox("Escribe el nombre del corredor:", sorted(df_filtered['runner_name'].unique()))
    
    if runner_name:
        runner_row = df_filtered[df_filtered['runner_name'] == runner_name].iloc[0]
        
        # Cálculos de posición
        pos_general = (df_filtered['time_seconds'] < runner_row['time_seconds']).sum() + 1
        total = len(df_filtered)
        
        res1, res2, res3 = st.columns(3)
        res1.subheader(f"⏱️ {runner_row['finish_time']}")
        res1.write("Tiempo Final")
        
        res2.subheader(f"🏁 {pos_general}º de {total}")
        res2.write("Posición General")
        
        # Ritmo estimado (min/km)
        distancia = float(runner_row['race_distance'])
        ritmo_seg = runner_row['time_seconds'] / distancia
        ritmo_min = str(timedelta(seconds=int(ritmo_seg))).split(':')[-2:]
        res3.subheader(f"⚡ {ritmo_min[0]}:{ritmo_min[1]} min/km")
        res3.write("Ritmo Medio")

        st.markdown("---")
        
        # Gráfico de posición
        st.write(f"**{runner_name}** comparado con el resto de corredores:")
        fig_pos = px.histogram(df_filtered, x="time_seconds", nbins=40)
        fig_pos.add_vline(x=runner_row['time_seconds'], line_color="red", line_width=4, annotation_text="TU META")
        st.plotly_chart(fig_pos, use_container_width=True)