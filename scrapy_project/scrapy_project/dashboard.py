import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from datetime import timedelta

st.set_page_config(layout="wide", page_title="Race Analysis Dashboard", page_icon="🏃‍♂️")

@st.cache_data
def load_data():
    df = pd.read_json("scrapy_project/edMongo.json")
    
    temp_time = pd.to_datetime(df['finish_time'], errors='coerce')

    df['time_seconds'] = (
        temp_time.dt.hour * 3600 + 
        temp_time.dt.minute * 60 + 
        temp_time.dt.second
    ).fillna(0).astype(int)
    
    df['race_label'] = df['fecha'] + " - " + df['location'] + " (" + df['race_distance'].astype(str) + "km)"
    df = df.sort_values('time_seconds')
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"⚠️ Error al cargar el archivo: {e}")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎯 Filtros")
race_choice = st.sidebar.selectbox("Selecciona Evento", df['race_label'].unique())
gender_choice = st.sidebar.multiselect(
    "Género", 
    df['gender'].unique().tolist(), 
    default=df['gender'].unique().tolist()
)

mask = (df['race_label'] == race_choice) & (df['gender'].isin(gender_choice))
df_filtered = df[mask].copy()

# --- MAIN DASHBOARD ---
st.title("🏆 Análisis de Resultados de Carrera")
st.info(f"📍 Evento: {race_choice}")

tab1, tab2, tab3 = st.tabs(["📊 Estadísticas Generales", "👤 Buscador de Corredor", "🌟 Hall of Fame"])

# --- TAB 1: ESTADÍSTICAS GENERALES ---
with tab1:
    if df_filtered.empty:
        st.warning("No hay datos disponibles para los filtros seleccionados.")
    else:
        col1, col2, col3, col4 = st.columns(4)
        
        raw_best = pd.to_datetime(df_filtered['finish_time'].iloc[0])
        m_best = raw_best.strftime('%H:%M:%S') 
        
        m_avg_secs = df_filtered['time_seconds'].mean()
        m_avg = str(timedelta(seconds=int(m_avg_secs)))
        
        col1.metric("Mejor Tiempo", m_best)
        col2.metric("Tiempo Medio", m_avg)
        col3.metric("Total Corredores", len(df_filtered))
        col4.metric("Distancia", f"{df_filtered['race_distance'].iloc[0]} km")

        st.markdown("---")

        c_left, c_right = st.columns(2)
        with c_left:
            st.subheader("Distribución de Tiempos")
            fig_hist = px.histogram(df_filtered, x="time_seconds", color="gender", nbins=30, template="plotly_dark")
            st.plotly_chart(fig_hist, use_container_width=True)

        with c_right:
            st.subheader("Tiempos por Grupo de Edad")
            fig_age = px.box(df_filtered, x="age_group", y="time_seconds", color="gender", template="plotly_dark")
            st.plotly_chart(fig_age, use_container_width=True)

        st.markdown("---")

        st.subheader("📈 Curva de Densidad de Finalización")
        st.write("Visualización de la concentración de corredores por tiempo (minutos).")
        
        genders = df_filtered['gender'].unique()
        hist_data = [df_filtered[df_filtered['gender'] == g]['time_seconds'] / 60 for g in genders]
        
        fig_kde = ff.create_distplot(hist_data, genders, show_hist=False, show_rug=False)

        for trace in fig_kde.data:
            trace.update(fill='tozeroy') 

        min_x_min = (df_filtered['time_seconds'].min() / 60) * 0.95
        max_x_min = (df_filtered['time_seconds'].max() / 60) * 1.05
        avg_min = m_avg_secs / 60

        fig_kde.update_layout(
            template="plotly_dark",
            xaxis_title="Tiempo (Minutos)",
            yaxis_title="Densidad",
            xaxis=dict(range=[min_x_min, max_x_min]), 
            margin=dict(t=30, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        fig_kde.add_vline(
            x=avg_min, 
            line_dash="dash", 
            line_color="white", 
            annotation_text=f"Media: {m_avg}",
            annotation_position="top left"
        )
        
        st.plotly_chart(fig_kde, use_container_width=True)

# --- TAB 2: BUSCADOR INDIVIDUAL ---
with tab2:
    st.subheader("🔎 Análisis Individual")
    runner_name = st.selectbox("Escribe el nombre del corredor:", sorted(df_filtered['runner_name'].unique()))
    
    if runner_name:
        runner_row = df_filtered[df_filtered['runner_name'] == runner_name].iloc[0]
        pos_general = (df_filtered['time_seconds'] < runner_row['time_seconds']).sum() + 1
        total = len(df_filtered)
        
        res1, res2, res3 = st.columns(3)
        res1.subheader(f"⏱️ {runner_row['finish_time']}")
        res1.write("Tiempo Final")
        
        res2.subheader(f"🏁 {pos_general}º de {total}")
        res2.write("Posición General")
        
        distancia = float(runner_row['race_distance'])
        ritmo_seg = runner_row['time_seconds'] / distancia
        ritmo_min = str(timedelta(seconds=int(ritmo_seg))).split(':')[-2:]
        res3.subheader(f"⚡ {ritmo_min[0]}:{ritmo_min[1]} min/km")
        res3.write("Ritmo Medio")

        st.markdown("---")
        fig_pos = px.histogram(df_filtered, x="time_seconds", nbins=40, template="plotly_dark")
        fig_pos.add_vline(x=runner_row['time_seconds'], line_color="red", line_width=4, annotation_text="TU META")
        st.plotly_chart(fig_pos, use_container_width=True)

# --- TAB 3: HALL OF FAME ---
with tab3:
    st.subheader("🥇 Top 10 Corredores - Hall of Fame")
    
    top_10 = df_filtered.head(10).copy()
    top_10['finish_time_clean'] = pd.to_datetime(top_10['finish_time']).dt.strftime('%H:%M:%S')
    top_10.insert(0, 'Puesto', range(1, len(top_10) + 1))
    
    top_display = top_10[['Puesto', 'runner_name', 'gender', 'age_group', 'finish_time_clean']]
    top_display.columns = ['Puesto', 'Nombre del Atleta', 'Género', 'Categoría', 'Crono']
    
    st.dataframe(
        top_display, 
        hide_index=True, 
        use_container_width=True,
        column_config={
            "Puesto": st.column_config.NumberColumn("Rank", format="%d 🏆"),
            "Crono": st.column_config.TextColumn("⏱️ Tiempo Final")
        }
    )
    
    fig_top = px.bar(
        top_10, 
        x='runner_name', 
        y='time_seconds', 
        color='gender', 
        template="plotly_dark",
        labels={'runner_name': 'Atleta', 'time_seconds': 'Segundos'}
    )
    fig_top.update_yaxes(range=[top_10['time_seconds'].min() * 0.98, top_10['time_seconds'].max() * 1.02])
    st.plotly_chart(fig_top, use_container_width=True)