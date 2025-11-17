import streamlit as st
import pandas as pd
import altair as alt

# Configuración de página con tema oscuro
st.set_page_config(
    page_title="Messi vs Ronaldo Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado con diseño tipo dashboard profesional
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    /* Fondo principal */
    .stApp {
        background: #0a0d1f;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Container principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 1600px;
    }
    
    /* Títulos */
    h1 {
        color: #ffffff;
        font-weight: 800;
        font-size: 2.8rem !important;
        margin-bottom: 0.3rem;
        letter-spacing: 0.02em;
        text-align: center;
        text-transform: uppercase;
    }
    
    .subtitle {
        color: #60a5fa;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
        text-align: center;
        letter-spacing: 0.03em;
    }
    
    /* Contenedor centrado para KPIs */
    .kpi-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem auto;
        max-width: 1400px;
    }
    
    /* Tabs personalizados - SIN EMOJIS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(15, 20, 40, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
        border: 1px solid rgba(6, 182, 212, 0.25);
        justify-content: center;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: #60a5fa;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 1px solid transparent;
        transition: all 0.3s ease;
        font-family: 'Poppins', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(6, 182, 212, 0.1);
        border-color: rgba(6, 182, 212, 0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(6, 182, 212, 0.2) 0%, rgba(168, 85, 247, 0.2) 100%);
        border-color: #06b6d4;
        color: #06b6d4;
    }
    
    /* Sección headers */
    .section-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(6, 182, 212, 0.3);
    }
    
    .section-title {
        color: #06b6d4;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 0.1em;
        text-align: center;
        text-transform: uppercase;
    }
    
    /* Tarjetas de métricas mejoradas y centralizadas */
    div[data-testid="metric-container"] {
        background: rgba(15, 20, 40, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(6, 182, 212, 0.4);
        border-radius: 16px;
        padding: 1.5rem 1.2rem;
        box-shadow: 
            0 4px 12px rgba(0, 0, 0, 0.5),
            0 0 25px rgba(6, 182, 212, 0.15);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
        text-align: center;
    }
    
    div[data-testid="metric-container"]::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #06b6d4 0%, #a855f7 100%);
        opacity: 0.9;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 
            0 12px 24px rgba(0, 0, 0, 0.6),
            0 0 40px rgba(6, 182, 212, 0.35);
        border-color: rgba(6, 182, 212, 0.7);
    }
    
    [data-testid="stMetricLabel"] {
        color: #60a5fa;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.5rem;
        font-family: 'Poppins', sans-serif;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2.4rem;
        font-weight: 800;
        color: #06b6d4;
        line-height: 1.2;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Gráficas - Contenedor mejorado */
    .chart-container {
        background: rgba(15, 20, 40, 0.6);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(6, 182, 212, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 0.5rem;
        box-shadow: 
            0 4px 6px rgba(0, 0, 0, 0.4),
            0 0 20px rgba(6, 182, 212, 0.08);
        height: 100%;
    }
    
    .chart-title {
        color: #06b6d4;
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        font-family: 'Poppins', sans-serif;
    }
    
    .chart-subtitle {
        color: #60a5fa;
        font-size: 0.85rem;
        margin-bottom: 1rem;
        font-weight: 400;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {
        background: #0f1428;
        border-right: 1px solid rgba(6, 182, 212, 0.2);
    }
    
    section[data-testid="stSidebar"] > div {
        background: transparent;
    }
    
    /* Tabla mejorada */
    .dataframe {
        font-family: 'Poppins', sans-serif !important;
    }
</style>
""", unsafe_allow_html=True)

# Cargar datos desde el archivo Excel
try:
    df_raw = pd.read_excel("MessiRonaldo.xlsx")
    
    df_raw.columns = ['Season', 'Player', 'Liga_Goals', 'Liga_Asts', 'Liga_Aps', 
                      'Liga_Minutes', 'CL_Goals', 'CL_Asts', 'CL_Aps', 'CL_Minutes']
    
    df_liga = df_raw[['Season', 'Player', 'Liga_Goals', 'Liga_Asts', 'Liga_Aps', 'Liga_Minutes']].copy()
    df_liga.columns = ['Season', 'Player', 'Goals', 'Assists', 'Matches', 'Minutes']
    df_liga['Competition'] = 'Liga'
    
    df_cl = df_raw[['Season', 'Player', 'CL_Goals', 'CL_Asts', 'CL_Aps', 'CL_Minutes']].copy()
    df_cl.columns = ['Season', 'Player', 'Goals', 'Assists', 'Matches', 'Minutes']
    df_cl['Competition'] = 'Champions League'
    
    df = pd.concat([df_liga, df_cl], ignore_index=True)
    
    numeric_cols = ['Goals', 'Assists', 'Matches', 'Minutes']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
except FileNotFoundError:
    st.error("No se encontró el archivo 'MessiRonaldo.xlsx'")
    st.stop()
except Exception as e:
    st.error(f"Error: {str(e)}")
    st.stop()

# Crear métricas calculadas
df["GA"] = df["Goals"] + df["Assists"]
df["GA_per_match"] = df["GA"] / df["Matches"].replace(0, float("nan"))
df["Min_per_Goal"] = df["Minutes"] / df["Goals"].replace(0, float("nan"))
df["Min_per_GA"] = df["Minutes"] / df["GA"].replace(0, float("nan"))

# Header principal centralizado
st.markdown("# MESSI VS CRISTIANO RONALDO")
st.markdown('<p class="subtitle">Análisis comparativo de eficiencia, consistencia y rendimiento profesional</p>', unsafe_allow_html=True)

# Filtros en sidebar
with st.sidebar:
    st.markdown("### Filtros de Análisis")
    
    selected_competition = st.multiselect(
        "Competición",
        options=df['Competition'].unique(),
        default=df['Competition'].unique()
    )
    
    selected_seasons = st.slider(
        "Rango de temporadas",
        min_value=int(df['Season'].str[:4].astype(int).min()),
        max_value=int(df['Season'].str[:4].astype(int).max()),
        value=(int(df['Season'].str[:4].astype(int).min()), 
               int(df['Season'].str[:4].astype(int).max()))
    )

# Aplicar filtros
df_filtered = df[df['Competition'].isin(selected_competition)]
df_filtered = df_filtered[
    df_filtered['Season'].str[:4].astype(int).between(selected_seasons[0], selected_seasons[1])
]

# Agrupar datos
df_grouped = df_filtered.groupby(['Season', 'Player']).agg({
    'Goals': 'sum',
    'Assists': 'sum',
    'Matches': 'sum',
    'Minutes': 'sum'
}).reset_index()

df_grouped['GA'] = df_grouped['Goals'] + df_grouped['Assists']
df_grouped['GA_per_match'] = df_grouped['GA'] / df_grouped['Matches']
df_grouped['Min_per_Goal'] = df_grouped['Minutes'] / df_grouped['Goals'].replace(0, float("nan"))

# KPIs principales centralizados
st.markdown("""
<div class="section-header">
    <h2 class="section-title">RESUMEN GENERAL</h2>
</div>
""", unsafe_allow_html=True)

# Crear columnas vacías para centrar las KPIs
col_empty1, kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6, col_empty2 = st.columns([0.5, 1, 1, 1, 1, 1, 1, 0.5])

with kpi_col1:
    messi_ga = int(df_filtered[df_filtered.Player=="Messi"]["GA"].sum())
    st.metric("MESSI G+A", f"{messi_ga:,}")

with kpi_col2:
    cr7_ga = int(df_filtered[df_filtered.Player=="Ronaldo"]["GA"].sum())
    st.metric("RONALDO G+A", f"{cr7_ga:,}")

with kpi_col3:
    messi_goals = int(df_filtered[df_filtered.Player=="Messi"]["Goals"].sum())
    st.metric("MESSI GOLES", f"{messi_goals:,}")

with kpi_col4:
    cr7_goals = int(df_filtered[df_filtered.Player=="Ronaldo"]["Goals"].sum())
    st.metric("RONALDO GOLES", f"{cr7_goals:,}")

with kpi_col5:
    messi_assists = int(df_filtered[df_filtered.Player=="Messi"]["Assists"].sum())
    st.metric("MESSI ASTS", f"{messi_assists:,}")

with kpi_col6:
    cr7_assists = int(df_filtered[df_filtered.Player=="Ronaldo"]["Assists"].sum())
    st.metric("RONALDO ASTS", f"{cr7_assists:,}")

# Sistema de Tabs SIN EMOJIS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "EVOLUCIÓN TEMPORAL", 
    "POR COMPETICIÓN", 
    "EFICIENCIA", 
    "ANÁLISIS DETALLADO",
    "COMPARATIVA DIRECTA"
])

# TAB 1: Evolución Temporal
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">G+A por Partido</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Tendencia histórica</p>', unsafe_allow_html=True)
        
        line_chart = alt.Chart(df_grouped).mark_line(
            strokeWidth=3,
            point=alt.OverlayMarkDef(size=80, filled=True)
        ).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("GA_per_match:Q", title="G+A por Partido", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", 
                            scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]),
                            legend=alt.Legend(title=None, orient="top", labelColor="#e2e8f0")),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("GA_per_match:Q", title="G+A/Partido", format=".2f")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(line_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Goles por Temporada</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Producción goleadora</p>', unsafe_allow_html=True)
        
        goals_chart = alt.Chart(df_grouped).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("Goals:Q", title="Goles", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("Goals:Q", title="Goles")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(goals_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Asistencias por Temporada</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Creación de juego</p>', unsafe_allow_html=True)
        
        assists_chart = alt.Chart(df_grouped).mark_area(
            line={'strokeWidth': 2},
            opacity=0.6
        ).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("Assists:Q", title="Asistencias", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("Assists:Q", title="Asistencias")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(assists_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Minutos Jugados</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Carga de partidos</p>', unsafe_allow_html=True)
        
        minutes_chart = alt.Chart(df_grouped).mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("Minutes:Q", title="Minutos", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("Minutes:Q", title="Minutos", format=",")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(minutes_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 2: Por Competición
with tab2:
    col1, col2 = st.columns(2)
    
    comp_data = df_filtered.groupby(['Competition', 'Player']).agg({
        'GA': 'sum',
        'Goals': 'sum',
        'Assists': 'sum',
        'Matches': 'sum'
    }).reset_index()
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Contribuciones Totales</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">G+A por competición</p>', unsafe_allow_html=True)
        
        comp_chart = alt.Chart(comp_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x=alt.X("Competition:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("GA:Q", title="G+A", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=alt.Legend(title=None, orient="top", labelColor="#e2e8f0")),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Competition:N", title="Competición"),
                alt.Tooltip("GA:Q", title="G+A")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(comp_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Goles por Competición</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Distribución goleadora</p>', unsafe_allow_html=True)
        
        goals_comp = alt.Chart(comp_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x=alt.X("Competition:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("Goals:Q", title="Goles", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Competition:N", title="Competición"),
                alt.Tooltip("Goals:Q", title="Goles")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(goals_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Asistencias por Competición</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Capacidad de asociación</p>', unsafe_allow_html=True)
        
        assists_comp = alt.Chart(comp_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x=alt.X("Competition:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("Assists:Q", title="Asistencias", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Competition:N", title="Competición"),
                alt.Tooltip("Assists:Q", title="Asistencias")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(assists_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        comp_data['GA_per_match'] = comp_data['GA'] / comp_data['Matches']
        
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Promedio por Partido</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Eficiencia según competición</p>', unsafe_allow_html=True)
        
        avg_comp = alt.Chart(comp_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10
        ).encode(
            x=alt.X("Competition:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("GA_per_match:Q", title="G+A por Partido", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            xOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Competition:N", title="Competición"),
                alt.Tooltip("GA_per_match:Q", title="G+A/Partido", format=".2f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(avg_comp, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 3: Eficiencia
with tab3:
    col1, col2 = st.columns(2)
    
    efficiency_data = df_grouped.groupby('Player').agg({
        'Min_per_Goal': 'mean',
        'Goals': 'sum',
        'Minutes': 'sum',
        'GA': 'sum'
    }).reset_index()
    efficiency_data['Min_per_GA'] = efficiency_data['Minutes'] / efficiency_data['GA']
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Minutos por Gol</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Eficiencia de conversión</p>', unsafe_allow_html=True)
        
        mpg_chart = alt.Chart(efficiency_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10,
            width=120
        ).encode(
            x=alt.X("Player:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("Min_per_Goal:Q", title="Minutos/Gol", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Min_per_Goal:Q", title="Min/Gol", format=".1f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(mpg_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Minutos por G+A</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Eficiencia total</p>', unsafe_allow_html=True)
        
        mpga_chart = alt.Chart(efficiency_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10,
            width=120
        ).encode(
            x=alt.X("Player:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("Min_per_GA:Q", title="Minutos/G+A", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Min_per_GA:Q", title="Min/G+A", format=".1f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(mpga_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Evolución Eficiencia</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Minutos por gol a lo largo del tiempo</p>', unsafe_allow_html=True)
        
        eff_evolution = alt.Chart(df_grouped).mark_line(
            strokeWidth=3,
            point=alt.OverlayMarkDef(size=80, filled=True)
        ).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("Min_per_Goal:Q", title="Min/Gol", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("Min_per_Goal:Q", title="Min/Gol", format=".1f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(eff_evolution, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Partidos Jugados</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Total de apariciones</p>', unsafe_allow_html=True)
        
        matches_data = df_grouped.groupby('Player')['Matches'].sum().reset_index()
        
        matches_chart = alt.Chart(matches_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10,
            width=120
        ).encode(
            x=alt.X("Player:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("Matches:Q", title="Partidos", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Matches:Q", title="Partidos")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(matches_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 4: Análisis Detallado
with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Top 10 Mejores Temporadas</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Por total de G+A</p>', unsafe_allow_html=True)
        
        top_seasons = df_grouped.nlargest(10, 'GA')[['Player', 'Season', 'GA']].sort_values('GA', ascending=True)
        
        top_chart = alt.Chart(top_seasons).mark_bar(
            cornerRadiusTopRight=8,
            cornerRadiusBottomRight=8
        ).encode(
            y=alt.Y("Season:N", title=None, sort='-x', axis=alt.Axis(labelColor="#60a5fa")),
            x=alt.X("GA:Q", title="G+A", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=alt.Legend(title=None, orient="top", labelColor="#e2e8f0")),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("GA:Q", title="G+A")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(top_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Distribución Goles vs Asistencias</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Proporción de contribuciones</p>', unsafe_allow_html=True)
        
        contribution_data = df_filtered.groupby('Player').agg({
            'Goals': 'sum',
            'Assists': 'sum'
        }).reset_index()
        
        contribution_data_melted = contribution_data.melt(
            id_vars=['Player'],
            value_vars=['Goals', 'Assists'],
            var_name='Tipo',
            value_name='Total'
        )
        
        donut_chart = alt.Chart(contribution_data_melted).mark_arc(innerRadius=60, outerRadius=110).encode(
            theta=alt.Theta("Total:Q"),
            color=alt.Color(
                "Tipo:N",
                scale=alt.Scale(domain=['Goals', 'Assists'], range=['#06b6d4', '#a855f7']),
                legend=alt.Legend(title=None, orient="bottom", labelColor="#e2e8f0")
            ),
            column=alt.Column("Player:N", header=alt.Header(labelColor="#e2e8f0", labelFontSize=14)),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Tipo:N", title="Tipo"),
                alt.Tooltip("Total:Q", title="Total")
            ]
        ).properties(
            height=350,
            width=160
        ).configure_view(
            strokeWidth=0,
            fill="#0a0d1f"
        )
        
        st.altair_chart(donut_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Segunda fila
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Ratio Goles/Asistencias</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Por temporada</p>', unsafe_allow_html=True)
        
        df_grouped['Goals_Assists_Ratio'] = df_grouped['Goals'] / df_grouped['Assists'].replace(0, float("nan"))
        
        ratio_chart = alt.Chart(df_grouped).mark_line(
            strokeWidth=2,
            point=alt.OverlayMarkDef(size=60, filled=True)
        ).encode(
            x=alt.X("Season:N", title=None, axis=alt.Axis(labelAngle=-45, labelColor="#60a5fa", labelFontSize=9)),
            y=alt.Y("Goals_Assists_Ratio:Q", title="Ratio G/A", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Season:N", title="Temporada"),
                alt.Tooltip("Goals_Assists_Ratio:Q", title="Ratio G/A", format=".2f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(ratio_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Consistencia por Temporada</p>', unsafe_allow_html=True)
        st.markdown('<p class="chart-subtitle">Desviación estándar de G+A</p>', unsafe_allow_html=True)
        
        consistency_data = df_grouped.groupby('Player').agg({
            'GA': ['std', 'mean']
        }).reset_index()
        consistency_data.columns = ['Player', 'STD', 'Mean']
        
        consistency_chart = alt.Chart(consistency_data).mark_bar(
            cornerRadiusTopLeft=10,
            cornerRadiusTopRight=10,
            width=120
        ).encode(
            x=alt.X("Player:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            y=alt.Y("STD:Q", title="Desviación Estándar", axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("STD:Q", title="Desv. Estándar", format=".2f"),
                alt.Tooltip("Mean:Q", title="Media G+A", format=".2f")
            ]
        ).properties(height=400).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(consistency_chart, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# TAB 5: Comparativa Directa
with tab5:
    col1, col2, col3 = st.columns(3)
    
    # KPIs comparativos
    messi_total = df_filtered[df_filtered.Player=="Messi"]
    ronaldo_total = df_filtered[df_filtered.Player=="Ronaldo"]
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Comparación Total</p>', unsafe_allow_html=True)
        
        comparison_metrics = pd.DataFrame({
            'Métrica': ['Goles', 'Asistencias', 'Partidos', 'G+A'],
            'Messi': [
                int(messi_total['Goals'].sum()),
                int(messi_total['Assists'].sum()),
                int(messi_total['Matches'].sum()),
                int(messi_total['GA'].sum())
            ],
            'Ronaldo': [
                int(ronaldo_total['Goals'].sum()),
                int(ronaldo_total['Assists'].sum()),
                int(ronaldo_total['Matches'].sum()),
                int(ronaldo_total['GA'].sum())
            ]
        })
        
        comparison_melted = comparison_metrics.melt(id_vars=['Métrica'], var_name='Player', value_name='Total')
        
        comp_bar = alt.Chart(comparison_melted).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8
        ).encode(
            y=alt.Y("Métrica:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            x=alt.X("Total:Q", title=None, axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=alt.Legend(title=None, orient="top", labelColor="#e2e8f0")),
            yOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Métrica:N", title="Métrica"),
                alt.Tooltip("Total:Q", title="Total", format=",")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(comp_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Promedios por Partido</p>', unsafe_allow_html=True)
        
        avg_metrics = pd.DataFrame({
            'Métrica': ['G/Partido', 'A/Partido', 'G+A/Partido'],
            'Messi': [
                round(messi_total['Goals'].sum() / messi_total['Matches'].sum(), 2),
                round(messi_total['Assists'].sum() / messi_total['Matches'].sum(), 2),
                round(messi_total['GA'].sum() / messi_total['Matches'].sum(), 2)
            ],
            'Ronaldo': [
                round(ronaldo_total['Goals'].sum() / ronaldo_total['Matches'].sum(), 2),
                round(ronaldo_total['Assists'].sum() / ronaldo_total['Matches'].sum(), 2),
                round(ronaldo_total['GA'].sum() / ronaldo_total['Matches'].sum(), 2)
            ]
        })
        
        avg_melted = avg_metrics.melt(id_vars=['Métrica'], var_name='Player', value_name='Promedio')
        
        avg_bar = alt.Chart(avg_melted).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8
        ).encode(
            y=alt.Y("Métrica:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            x=alt.X("Promedio:Q", title=None, axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            yOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Métrica:N", title="Métrica"),
                alt.Tooltip("Promedio:Q", title="Promedio", format=".2f")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(avg_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('<p class="chart-title">Eficiencia Comparada</p>', unsafe_allow_html=True)
        
        eff_metrics = pd.DataFrame({
            'Métrica': ['Min/Gol', 'Min/Asist', 'Min/G+A'],
            'Messi': [
                round(messi_total['Minutes'].sum() / messi_total['Goals'].sum(), 1),
                round(messi_total['Minutes'].sum() / messi_total['Assists'].sum(), 1),
                round(messi_total['Minutes'].sum() / messi_total['GA'].sum(), 1)
            ],
            'Ronaldo': [
                round(ronaldo_total['Minutes'].sum() / ronaldo_total['Goals'].sum(), 1),
                round(ronaldo_total['Minutes'].sum() / ronaldo_total['Assists'].sum(), 1),
                round(ronaldo_total['Minutes'].sum() / ronaldo_total['GA'].sum(), 1)
            ]
        })
        
        eff_melted = eff_metrics.melt(id_vars=['Métrica'], var_name='Player', value_name='Minutos')
        
        eff_bar = alt.Chart(eff_melted).mark_bar(
            cornerRadiusTopLeft=8,
            cornerRadiusTopRight=8
        ).encode(
            y=alt.Y("Métrica:N", title=None, axis=alt.Axis(labelColor="#60a5fa")),
            x=alt.X("Minutos:Q", title=None, axis=alt.Axis(labelColor="#60a5fa", grid=True, gridColor="rgba(6, 182, 212, 0.1)")),
            color=alt.Color("Player:N", scale=alt.Scale(domain=["Messi", "Ronaldo"], range=["#06b6d4", "#a855f7"]), legend=None),
            yOffset="Player:N",
            tooltip=[
                alt.Tooltip("Player:N", title="Jugador"),
                alt.Tooltip("Métrica:N", title="Métrica"),
                alt.Tooltip("Minutos:Q", title="Minutos", format=".1f")
            ]
        ).properties(height=350).configure_view(strokeWidth=0, fill="#0a0d1f")
        
        st.altair_chart(eff_bar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Tabla comparativa
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">TABLA COMPARATIVA DETALLADA</h2>
    </div>
    """, unsafe_allow_html=True)
    
    comparison_table = pd.DataFrame({
        'Estadística': [
            'Goles Totales', 'Asistencias Totales', 'G+A Totales', 
            'Partidos Jugados', 'Minutos Jugados',
            'Goles/Partido', 'Asistencias/Partido', 'G+A/Partido',
            'Minutos/Gol', 'Minutos/Asistencia', 'Minutos/G+A'
        ],
        'Messi': [
            f"{int(messi_total['Goals'].sum()):,}",
            f"{int(messi_total['Assists'].sum()):,}",
            f"{int(messi_total['GA'].sum()):,}",
            f"{int(messi_total['Matches'].sum()):,}",
            f"{int(messi_total['Minutes'].sum()):,}",
            f"{messi_total['Goals'].sum() / messi_total['Matches'].sum():.2f}",
            f"{messi_total['Assists'].sum() / messi_total['Matches'].sum():.2f}",
            f"{messi_total['GA'].sum() / messi_total['Matches'].sum():.2f}",
            f"{messi_total['Minutes'].sum() / messi_total['Goals'].sum():.1f}",
            f"{messi_total['Minutes'].sum() / messi_total['Assists'].sum():.1f}",
            f"{messi_total['Minutes'].sum() / messi_total['GA'].sum():.1f}"
        ],
        'Ronaldo': [
            f"{int(ronaldo_total['Goals'].sum()):,}",
            f"{int(ronaldo_total['Assists'].sum()):,}",
            f"{int(ronaldo_total['GA'].sum()):,}",
            f"{int(ronaldo_total['Matches'].sum()):,}",
            f"{int(ronaldo_total['Minutes'].sum()):,}",
            f"{ronaldo_total['Goals'].sum() / ronaldo_total['Matches'].sum():.2f}",
            f"{ronaldo_total['Assists'].sum() / ronaldo_total['Matches'].sum():.2f}",
            f"{ronaldo_total['GA'].sum() / ronaldo_total['Matches'].sum():.2f}",
            f"{ronaldo_total['Minutes'].sum() / ronaldo_total['Goals'].sum():.1f}",
            f"{ronaldo_total['Minutes'].sum() / ronaldo_total['Assists'].sum():.1f}",
            f"{ronaldo_total['Minutes'].sum() / ronaldo_total['GA'].sum():.1f}"
        ]
    })
    
    st.dataframe(comparison_table, use_container_width=True, hide_index=True)