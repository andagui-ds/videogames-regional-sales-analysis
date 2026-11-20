import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Análisis de Ventas de Videojuegos", layout="wide"
)

# CSS compacto para que todo quepa en una sola vista sin scroll
st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 0.5rem;
        }
        h1 {
            font-size: 1.85rem !important;
            margin-bottom: 0.15rem !important;
        }
        h3 {
            font-size: 1.12rem !important;
            margin-top: 0.35rem !important;
            margin-bottom: 0.35rem !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎮 Análisis Regional de Ventas de Videojuegos")
st.caption(
    "Explora el desempeño comercial por región, género y plataforma para"
    " identificar oportunidades de campaña."
)


@st.cache_data
def load_data():
  try:
    df = pd.read_csv("games.csv", encoding="latin-1")
    df.columns = df.columns.str.lower()
    df["total_sales"] = (
        df["na_sales"] + df["eu_sales"] + df["jp_sales"] + df["other_sales"]
    )
    df = df.dropna(subset=["year_of_release", "genre", "platform"])
    df["year_of_release"] = df["year_of_release"].astype(int)
    df["rating"] = df["rating"].fillna("Sin Clasificar")
    return df
  except Exception as e:
    st.error(f"Error al leer games.csv: {e}")
    return pd.DataFrame()


df = load_data()

if not df.empty:
  # Barra lateral con etiquetas ejecutivas
  st.sidebar.header("Filtros de Exploración")

  regiones_map = {
      "Global (Total Sales)": "total_sales",
      "Norteamérica (NA)": "na_sales",
      "Europa (EU)": "eu_sales",
      "Japón (JP)": "jp_sales",
  }
  region_label = st.sidebar.selectbox(
      "Selecciona la Región", list(regiones_map.keys())
  )
  region = regiones_map[region_label]

  año_min, año_max = st.sidebar.slider(
      "Rango de Años de Lanzamiento", 1980, 2016, (2012, 2016)
  )

  ratings_disponibles = ["Todas"] + sorted(df["rating"].unique().tolist())
  rating_sel = st.sidebar.selectbox("Clasificación ESRB", ratings_disponibles)

  # Aplicar filtros
  df_filtered = df[
      (df["year_of_release"] >= año_min) & (df["year_of_release"] <= año_max)
  ]
  if rating_sel != "Todas":
    df_filtered = df_filtered[df_filtered["rating"] == rating_sel]

  if df_filtered.empty:
    st.warning("No hay registros para esa combinación de filtros.")
  else:
    # Agregaciones principales
    top_genres = (
        df_filtered.groupby("genre")[region]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    top_platforms = (
        df_filtered.groupby("platform")[region]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    ventas_totales = df_filtered[region].sum()
    total_juegos = len(df_filtered)
    genero_lider = top_genres.iloc[0]["genre"] if not top_genres.empty else "-"
    plat_lider = (
        top_platforms.iloc[0]["platform"] if not top_platforms.empty else "-"
    )

    # Fila superior de 4 KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(f"Ventas ({region_label.split()[0]})", f"{ventas_totales:,.1f} M")
    k2.metric("Títulos Analizados", f"{total_juegos:,}")
    k3.metric("Plataforma Líder", plat_lider)
    k4.metric("Género Líder", genero_lider)

    st.divider()

    # Dos gráficos lado a lado en una sola pantalla
    col_left, col_right = st.columns(2, gap="medium")

    with col_left:
      fig_genre = px.bar(
          top_genres,
          x=region,
          y="genre",
          orientation="h",
          title=f"Top 10 Géneros ({año_min}–{año_max})",
          labels={region: "Ventas (Millones)", "genre": ""},
          color=region,
          color_continuous_scale="Blues",
      )
      fig_genre.update_layout(
          yaxis={"categoryorder": "total ascending"},
          coloraxis_showscale=False,
          height=360,
          margin=dict(l=10, r=10, t=38, b=10),
      )
      st.plotly_chart(fig_genre, use_container_width=True)

    with col_right:
      fig_plat = px.bar(
          top_platforms,
          x=region,
          y="platform",
          orientation="h",
          title=f"Top 10 Plataformas ({año_min}–{año_max})",
          labels={region: "Ventas (Millones)", "platform": ""},
          color=region,
          color_continuous_scale="Teal",
      )
      fig_plat.update_layout(
          yaxis={"categoryorder": "total ascending"},
          coloraxis_showscale=False,
          height=360,
          margin=dict(l=10, r=10, t=38, b=10),
      )
      st.plotly_chart(fig_plat, use_container_width=True)
else:
  st.warning("Sube el archivo games.csv para visualizar los datos.")
