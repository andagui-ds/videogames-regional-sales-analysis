import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🎮 Análisis de Ventas de Videojuegos")
st.markdown("Explora las tendencias de ventas por región, género y plataforma.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv('games.csv')
        # Limpieza rápida
        df = df.dropna(subset=['year_of_release'])
        df['year_of_release'] = df['year_of_release'].astype(int)
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    region = st.sidebar.selectbox("Selecciona la Región", ["na_sales", "eu_sales", "jp_sales", "total_sales"])
    año_min, año_max = st.sidebar.slider("Rango de Años", 1980, 2016, (2010, 2016))
    
    df_filtered = df[(df['year_of_release'] >= año_min) & (df['year_of_release'] <= año_max)]
    
    # Top 10 Géneros
    top_genres = df_filtered.groupby('genre')[region].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig = px.bar(top_genres, x=region, y='genre', orientation='h', 
                 title=f"Top 10 Géneros en {region.upper()} ({año_min}-{año_max})",
                 labels={region: 'Ventas (Millones)', 'genre': 'Género'})
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    
    st.plotly_chart(fig)
else:
    st.warning("Sube el archivo games.csv para visualizar los datos.")
