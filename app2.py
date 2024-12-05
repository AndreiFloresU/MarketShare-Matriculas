import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

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
    # Filtrar datos por Región en el archivo
    filtered_df = filtered_df[filtered_df['REGION'].isin(region)]

# Filtro de Financiamiento
financiamiento = st.sidebar.multiselect(
    'Financiamiento:',
    options=filtered_df['FINANCIAMIENTO'].unique(),
    default=None,
    help="Selecciona uno o más tipos de financiamiento"
)

if financiamiento:
    # Filtrar datos por financiamiento en el archivo
    filtered_df = filtered_df[filtered_df['FINANCIAMIENTO'].isin(financiamiento)]

# Filtro de nivel
nivel = st.sidebar.multiselect(
    'Nivel:',
    options=filtered_df['NIVEL'].unique(),
    default=None,
    help="Selecciona uno o más niveles"
)

if nivel:
    # Filtrar datos por nivel en el archivo
    filtered_df = filtered_df[filtered_df['NIVEL'].isin(nivel)]

# Filtro de Facultad
facultad = st.sidebar.selectbox(
    'Facultad:',
    options=[None] + filtered_df['FACULTAD'].unique().tolist(),
    index=0,
    help="Selecciona una facultad"
)

if facultad:
    # Filtrar datos por facultad en el archivo
    filtered_df = filtered_df[filtered_df['FACULTAD'] == facultad]

# Filtro de Carrera
carrera = st.sidebar.multiselect(
    'Carrera:',
    options=filtered_df['CARRERA'].unique(),
    default=None,
    help="Selecciona una o más carreras"
)

if carrera:
    # Filtrar datos por carrera en el archivo
    filtered_df = filtered_df[filtered_df['CARRERA'].isin(carrera)]

# Agrupar por universidad y año
df_agrupado = filtered_df.groupby(['AÑO', 'UNIVERSIDAD']).agg({'MATRICULADOS': 'sum'}).reset_index()

# Calcular la participación para cada universidad en cada año
df_agrupado['PARTICIPACION'] = df_agrupado.groupby('AÑO')['MATRICULADOS'].transform(lambda x: x / x.sum())

# Crear una figura de Plotly
fig = go.Figure()

# Obtener los años únicos
años = df_agrupado['AÑO'].unique()

# Configurar la paleta de colores en tonos de azul (escala continua)
blues = px.colors.sequential.Blues

# Color para resaltar
highlight_color = px.colors.sequential.YlOrBr

# Dibujar barras para cada año
for i, año in enumerate(años):
    df_year = df_agrupado[df_agrupado['AÑO'] == año]

    # Generar los colores para cada barra (se resalta el de la universidads)
    colors = [
        highlight_color[i % len(highlight_color)] if universidad == "UNIVERSIDAD DE LAS AMERICAS" else blues[i % len(blues)]
        for universidad in df_year['UNIVERSIDAD']
    ]

    fig.add_trace(go.Bar(
        x=df_year['UNIVERSIDAD'],
        y=df_year['PARTICIPACION'],
        name=f'Año {año}',
        marker_color=colors,  # Colores
        text=df_year['PARTICIPACION'].apply(lambda x: f'{x:.2%}'),  # Texto con formato de porcentaje
        textposition='auto'  # Colocar los valores arriba de las barras
    ))

# Configurar el diseño del gráfico
fig.update_layout(
    barmode='group',
    title='Participación por Universidad y Año',
    xaxis_title='Universidades',
    yaxis_title='Participación',
    legend_title='Años',
    xaxis_tickangle=-45,
    template='plotly_white'
)

# Verificar si la universidad está presente en los datos filtrados
if "UNIVERSIDAD DE LAS AMERICAS" in df_agrupado['UNIVERSIDAD'].values:

    # Obtener la participación maxima calculada para la universidad
    participacion_universidad = df_agrupado.loc[
        df_agrupado['UNIVERSIDAD'] == "UNIVERSIDAD DE LAS AMERICAS", 'PARTICIPACION'
    ].max()

    # Agregar una anotación para la Universidad de las Américas
    fig.add_annotation(
        x="UNIVERSIDAD DE LAS AMERICAS",
        y=participacion_universidad,
        text="Universidad de las Américas",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor='yellow',
        font=dict(color='yellow', size=12)
    )

# Mostrar el gráfico en Streamlit
st.plotly_chart(fig)