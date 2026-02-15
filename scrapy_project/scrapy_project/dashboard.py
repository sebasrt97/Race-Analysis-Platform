import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(layout="wide", page_title="Race Analysis Dashboard")

# 1. Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("tus_datos_scrapeados.csv")
    # Asegúrate de convertir tiempos a segundos para cálculos
    return df

df = load_data()

# SIDEBAR - Filtros Globales
st.sidebar.header("Filtros")
race_choice = st.sidebar.selectbox("Selecciona Carrera", df['race'].unique())
gender_choice = st.sidebar.multiselect("Género", df['gender'].unique(), default=df['gender'].unique())

# Filtrado de datos
mask = (df['race'] == race_choice) & (df['gender'].isin(gender_choice))
df_filtered = df[mask]

# DASHBOARD PRINCIPAL
st.title("🏆 Análisis de Carreras")

tab1, tab2 = st.tabs(["Análisis de Carrera", "Análisis de Corredor"])

with tab1:
    st.subheader(f"Resultados: {race_choice}")
    # Métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Mínimo", df_filtered['time'].min())
    col2.metric("Media", df_filtered['time'].mean())
    # ... etc
    
    # Gráfico
    fig = px.histogram(df_filtered, x="time", nbins=30, title="Distribución de Tiempos")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader("Búsqueda de Corredor")
    runner_name = st.selectbox("Nombre del Corredor", df['runner_name'].unique())
    # Lógica para mostrar historial y posición en la distribución