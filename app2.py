import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

# Cargar los datos
df = pd.read_excel("./BASE.xlsx")

# Título de la aplicación
st.title("MARKETSHARE MATRICULAS")

# Filtros en la barra lateral
st.sidebar.header("Filtros")

# Filtro de Región
region = st.sidebar.multiselect(
    'Región:',
    options=df['REGION'].unique(),
    default=None,
    help="Selecciona una o más regiones"
)

filtered_df = df.copy()

if region:
    filtered_df = filtered_df[filtered_df['REGION'].isin(region)]

# Filtro de Financiamiento
financiamiento = st.sidebar.multiselect(
    'Financiamiento:',
    options=filtered_df['FINANCIAMIENTO'].unique(),
    default=None,
    help="Selecciona uno o más tipos de financiamiento"
)

if financiamiento:
    filtered_df = filtered_df[filtered_df['FINANCIAMIENTO'].isin(financiamiento)]

# Filtro de Nivel
nivel = st.sidebar.multiselect(
    'Nivel:',
    options=filtered_df['NIVEL'].unique(),
    default=None,
    help="Selecciona uno o más niveles"
)

if nivel:
    filtered_df = filtered_df[filtered_df['NIVEL'].isin(nivel)]

# Filtro de Facultad
facultad = st.sidebar.selectbox(
    'Facultad:',
    options=[None] + filtered_df['FACULTAD'].unique().tolist(),
    index=0,
    help="Selecciona una facultad"
)

if facultad:
    filtered_df = filtered_df[filtered_df['FACULTAD'] == facultad]

# Filtro de Carrera
carrera = st.sidebar.multiselect(
    'Carrera:',
    options=filtered_df['CARRERA'].unique(),
    default=None,
    help="Selecciona una o más carreras"
)

if carrera:
    filtered_df = filtered_df[filtered_df['CARRERA'].isin(carrera)]

# Agrupar por universidad y año
df_agrupado = filtered_df.groupby(['AÑO', 'UNIVERSIDAD']).agg({'MATRICULADOS': 'sum'}).reset_index()

# Verificar que haya datos
if df_agrupado.empty:
    st.write("No hay datos con los filtros seleccionados.")
    st.stop()

# Calcular la participación
df_agrupado['PARTICIPACION'] = df_agrupado.groupby('AÑO')['MATRICULADOS'].transform(lambda x: x / x.sum())

# Crear la figura
fig = go.Figure()

# Obtener los años únicos
años = df_agrupado['AÑO'].unique()

# Dibujar barras para cada año
for i, año in enumerate(años):
    df_year = df_agrupado[df_agrupado['AÑO'] == año]

    # Definir colores
    colors = [
        'rgb(84,93,89)' if universidad == "UNIVERSIDAD DE LAS AMERICAS" else 'rgb(0,102,0)'
        for universidad in df_year['UNIVERSIDAD']
    ]

    fig.add_trace(go.Bar(
        x=df_year['PARTICIPACION'],
        y=df_year['UNIVERSIDAD'],
        marker_color=colors,
        orientation='h',
        name=f'Año {año}',
        text=df_year['PARTICIPACION'].apply(lambda x: f'{x:.2%}'),
        textposition='auto'
    ))

# Configurar el diseño del gráfico
fig.update_layout(
    barmode='group',
    title='Participación por Universidad y Año',
    xaxis_title='Participación',
    yaxis_title='Universidades',
    template='plotly_white',
    height=700
)

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)