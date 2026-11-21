import pandas as pd  # Lectura, limpieza y agrupación de ventas por región, género y plataforma
import plotly.express as px  # Creación de gráficas de barras horizontales interactivas
import streamlit as st  # Construcción de la interfaz web nativa sin CSS

st.set_page_config(  # Configura el título de la pestaña y el modo ancho (wide) en una pantalla
    page_title="Análisis de Ventas de Videojuegos",
    page_icon="🎮",
    layout="wide",
)

st.header("🎮 Análisis Regional de Ventas de Videojuegos")  # Encabezado compacto nativo sin CSS
st.caption(  # Subtítulo ejecutivo con el propósito del análisis comercial
    "Explora el desempeño comercial por región, género y plataforma para"
    " identificar oportunidades de campaña."
)


@st.cache_data  # Guarda el dataset limpio en caché para evitar recargas en cada filtro
def load_data():
    try:
        df = pd.read_csv("games.csv", encoding="latin-1")  # Lee el archivo desde la raíz del repo
        df.columns = df.columns.str.lower()  # Estandariza nombres de columnas a minúsculas
        df["total_sales"] = (  # Calcula las ventas globales sumando las 4 regiones
            df["na_sales"] + df["eu_sales"] + df["jp_sales"] + df["other_sales"]
        )
        df = df.dropna(subset=["year_of_release", "genre", "platform"])  # Elimina registros incompletos
        df["year_of_release"] = df["year_of_release"].astype(int)  # Convierte el año a entero
        df["rating"] = df["rating"].fillna("Sin Clasificar")  # Imputa clasificaciones ESRB faltantes
        return df
    except Exception as e:
        st.error(f"Error al leer games.csv: {e}")  # Muestra alerta nativa si falta el CSV
        return pd.DataFrame()


df = load_data()  # Carga el catálogo histórico de videojuegos

if not df.empty:
    # Barra lateral con filtros dependientes (en cascada)
    st.sidebar.header("Filtros de Exploración")  # Encabezado del panel de filtros

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

    # Filtra primero por años y exige ventas > 0 en la región seleccionada
    df_base = df[
        (df["year_of_release"] >= año_min)
        & (df["year_of_release"] <= año_max)
        & (df[region] > 0)
    ]

    # Extrae únicamente las clasificaciones ESRB que sí tienen ventas > 0 en ese periodo y región
    ratings_con_datos = sorted(df_base["rating"].unique().tolist())
    ratings_disponibles = ["Todas"] + ratings_con_datos
    rating_sel = st.sidebar.selectbox("Clasificación ESRB", ratings_disponibles)  # Solo muestra opciones válidas

    # Aplica el filtro de clasificación ESRB si no se eligió "Todas"
    df_filtered = (
        df_base
        if rating_sel == "Todas"
        else df_base[df_base["rating"] == rating_sel]
    )

    if df_filtered.empty:
        st.warning("No hay registros con ventas en este rango de años y región.")  # Aviso si el periodo completo está vacío
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

        ventas_totales = df_filtered[region].sum()  # Total de millones de copias vendidas
        total_juegos = len(df_filtered)  # Cantidad de videojuegos con ventas en el periodo
        genero_lider = top_genres.iloc[0]["genre"] if not top_genres.empty else "-"  # Género #1
        plat_lider = top_platforms.iloc[0]["platform"] if not top_platforms.empty else "-"  # Plataforma #1

        # Fila superior de 4 tarjetas KPI
        k1, k2, k3, k4 = st.columns(4)
        k1.metric(f"Ventas ({region_label.split()[0]})", f"{ventas_totales:,.1f} M")
        k2.metric("Títulos con Ventas", f"{total_juegos:,}")
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
            st.plotly_chart(fig_genre, use_container_width=True)  # Renderiza gráfica responsiva

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
            st.plotly_chart(fig_plat, use_container_width=True)  # Renderiza gráfica responsiva
else:
    st.warning("Sube el archivo games.csv para visualizar los datos.")