# Lectura, limpieza y agrupación de ventas por región, género y plataforma
import pandas as pd
# Creación de gráficas de barras horizontales interactivas
import plotly.express as px
import streamlit as st  # Construcción de la interfaz web nativa sin CSS

st.set_page_config(  # Configura el título de la pestaña y el modo ancho (wide) en una pantalla
    page_title="Análisis de Ventas de Videojuegos",
    page_icon="🎮",
    layout="wide",
)

# Encabezado compacto nativo sin CSS
st.header("🎮 Análisis Regional de Ventas de Videojuegos")
st.caption(  # Subtítulo ejecutivo con el propósito del análisis comercial
    "Explora el desempeño comercial por región, género y plataforma para"
    " identificar oportunidades de campaña."
)


@st.cache_data  # Guarda el dataset limpio en caché para evitar recargas en cada filtro
def load_data():
    try:
        # Lee el archivo desde la raíz del repo
        df = pd.read_csv("games.csv", encoding="latin-1")
        # Estandariza nombres de columnas a minúsculas
        df.columns = df.columns.str.lower()
        df["total_sales"] = (  # Calcula las ventas globales sumando las 4 regiones
            df["na_sales"] + df["eu_sales"] +
            df["jp_sales"] + df["other_sales"]
        )
        # Elimina registros incompletos
        df = df.dropna(subset=["year_of_release", "genre", "platform"])
        df["year_of_release"] = df["year_of_release"].astype(
            int)  # Convierte el año a entero
        # Imputa clasificaciones ESRB faltantes
        df["rating"] = df["rating"].fillna("Sin Clasificar")
        return df
    except Exception as e:
        # Muestra alerta nativa si falta el CSV
        st.error(f"Error al leer games.csv: {e}")
        return pd.DataFrame()


df = load_data()  # Carga el catálogo histórico de videojuegos

if not df.empty:
    # Barra lateral con etiquetas ejecutivas
    # Encabezado del panel de filtros
    st.sidebar.header("Filtros de Exploración")

    regiones_map = {  # Diccionario para traducir etiquetas ejecutivas a columnas del CSV
        "Global (Total Sales)": "total_sales",
        "Norteamérica (NA)": "na_sales",
        "Europa (EU)": "eu_sales",
        "Japón (JP)": "jp_sales",
    }
    region_label = st.sidebar.selectbox(  # Selector de mercado regional
        "Selecciona la Región", list(regiones_map.keys())
    )
    region = regiones_map[region_label]

    año_min, año_max = st.sidebar.slider(  # Control deslizante de rango de años de lanzamiento
        "Rango de Años de Lanzamiento", 1980, 2016, (2012, 2016)
    )

    # Lista ordenada de ESRB
    ratings_disponibles = ["Todas"] + sorted(df["rating"].unique().tolist())
    rating_sel = st.sidebar.selectbox(
        "Clasificación ESRB", ratings_disponibles)  # Filtro por clasificación

    # Aplicar filtros dinámicos
    df_filtered = df[
        (df["year_of_release"] >= año_min) & (df["year_of_release"] <= año_max)
    ]
    if rating_sel != "Todas":
        df_filtered = df_filtered[df_filtered["rating"] == rating_sel]

    if df_filtered.empty:
        # Aviso si el filtro queda vacío
        st.warning("No hay registros para esa combinación de filtros.")
    else:
        # Agregaciones principales para gráficos y KPIs
        top_genres = (  # Top 10 géneros ordenados por volumen de ventas
            df_filtered.groupby("genre")[region]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )
        top_platforms = (  # Top 10 consolas/plataformas ordenadas por volumen de ventas
            df_filtered.groupby("platform")[region]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        # Total de millones de copias vendidas
        ventas_totales = df_filtered[region].sum()
        # Cantidad de videojuegos en el periodo seleccionado
        total_juegos = len(df_filtered)
        # Género #1
        genero_lider = top_genres.iloc[0]["genre"] if not top_genres.empty else "-"
        # Plataforma #1
        plat_lider = top_platforms.iloc[0]["platform"] if not top_platforms.empty else "-"

        # Fila superior de 4 tarjetas KPI
        k1, k2, k3, k4 = st.columns(4)
        k1.metric(
            f"Ventas ({region_label.split()[0]})", f"{ventas_totales:,.1f} M")
        k2.metric("Títulos Analizados", f"{total_juegos:,}")
        k3.metric("Plataforma Líder", plat_lider)
        k4.metric("Género Líder", genero_lider)

        st.divider()  # Línea separadora nativa entre KPIs y gráficas

        # Dos gráficos lado a lado en una sola pantalla
        col_left, col_right = st.columns(2, gap="medium")

        with col_left:
            fig_genre = px.bar(  # Gráfico de barras horizontales para Top 10 Géneros
                top_genres,
                x=region,
                y="genre",
                orientation="h",
                title=f"Top 10 Géneros ({año_min}–{año_max})",
                labels={region: "Ventas (Millones)", "genre": ""},
                color=region,
                color_continuous_scale="Blues",
            )
            fig_genre.update_layout(  # Ordena de mayor a menor y ajusta márgenes compactos
                yaxis={"categoryorder": "total ascending"},
                coloraxis_showscale=False,
                height=360,
                margin=dict(l=10, r=10, t=38, b=10),
            )
            # Renderiza gráfica responsiva
            st.plotly_chart(fig_genre, use_container_width=True)

        with col_right:
            fig_plat = px.bar(  # Gráfico de barras horizontales para Top 10 Plataformas
                top_platforms,
                x=region,
                y="platform",
                orientation="h",
                title=f"Top 10 Plataformas ({año_min}–{año_max})",
                labels={region: "Ventas (Millones)", "platform": ""},
                color=region,
                color_continuous_scale="Teal",
            )
            fig_plat.update_layout(  # Ordena de mayor a menor y ajusta márgenes compactos
                yaxis={"categoryorder": "total ascending"},
                coloraxis_showscale=False,
                height=360,
                margin=dict(l=10, r=10, t=38, b=10),
            )
            # Renderiza gráfica responsiva
            st.plotly_chart(fig_plat, use_container_width=True)
else:
    st.warning("Sube el archivo games.csv para visualizar los datos.")
