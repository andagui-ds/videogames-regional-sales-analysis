[🇺🇸 Read in English](#-video-game-sales-analysis-regional-strategy-for-2017) | [🇲🇽 Leer en Español](#-análisis-de-ventas-de-videojuegos-estrategia-regional-para-2017)

---

# 🎮 Video Game Sales Analysis: Regional Strategy for 2017

> Exploratory Data Analysis (EDA) and statistical hypothesis testing to identify commercial success patterns in video games and plan regional marketing campaigns for 2017.

🚀 **[Launch Interactive Streamlit App](https://videogames-regional-sales-analysis.streamlit.app/)** | 🌐 **[View Quarto Web Report](https://andagui-ds.github.io/videogames-regional-sales-analysis/)**

---

## 🎯 Business Problem

The online video game store **Streamchik** (Ice) needs to identify what drives a video game's commercial success in order to plan its advertising and marketing campaigns for 2017.

The analysis addresses three key questions:
1. Which platforms and genres dominate the current market?
2. Are there significant differences in user preferences across North America (NA), Europe (EU), and Japan (JP)?
3. Do user and critic reviews affect sales in the same way across all platforms?

## 📊 Data and Preprocessing

* **Source:** `games.csv` (16,713 records and 11 columns).
* **Data Cleaning:**
  * Replaced `TBD` (*To Be Determined*) values in `user_score` with `NaN` and cast the column to float.
  * Imputed missing release years (`year_of_release`) by cross-referencing other platforms for the same game title.
  * Filled missing ESRB ratings with the `"Unknown"` category.
  * Created the derived column `total_sales` (sum of NA + EU + JP + Other sales).
* **Temporal Filtering:** Data prior to 2013–2014 was determined to be non-representative for forecasting 2017 (consoles have a ~5-year lifecycle). The final analysis focused on the modern era (2013–2016).

## 🧠 Key Findings (EDA)

1. **Platform Lifecycle:** Consoles typically have a 5-to-7-year lifespan. Historical leaders (PS2, Xbox 360) have been displaced by eighth-generation hardware.
2. **Recent Leaders (2013–2016):** **PS4** and **Xbox One (XOne)** overwhelmingly dominate sales volume in the current era.
3. **Review Impact (PS4 Case Study):**
   * **Critic** reviews show a moderate positive correlation with sales (`0.40`).
   * **User** reviews show virtually zero correlation (`-0.04`), indicating that players rate games based on emotional engagement rather than factors that predict commercial performance.

## 📈 Regional Profiles

Critical differences in consumer behavior were identified by region:

* **North America (NA) & Europe (EU):** Dominant platforms are PS4 and XOne. Top genres are **Action** and **Shooter**. The most popular ESRB ratings are "M" (Mature) and "E" (Everyone).
* **Japan (JP):** A completely distinct market. The leading platform is the handheld **Nintendo 3DS**, and the dominant genre is **Role-Playing (RPG)**. ESRB ratings hold minimal relevance in Japan (most titles are `"Unknown"`).

## 🔬 Statistical Hypothesis Testing (Alpha = 0.05)

**Independent two-sample Student's t-tests** were conducted (using `equal_var=False` / Welch's t-test after validating unequal variances via Levene's test):

* **Hypothesis 1:** *"Average user ratings for Xbox One and PC are the same."*
  * *Result:* Failed to reject the Null Hypothesis. Statistically, average user ratings are equal.
* **Hypothesis 2:** *"Average user ratings for Action and Sports genres are different."*
  * *Result:* Rejected the Null Hypothesis. There is a statistically significant difference in player ratings between these two genres.

## ✅ Business Recommendations (2017 Campaign)

1. **Prioritize PS4 and Xbox One:** Focus marketing budgets on these eighth-generation platforms.
2. **Glocal Strategy (Global + Local):**
   * **NA & EU:** Invest heavily in campaigns for *AAA* Action, Shooter, and Sports titles.
   * **Japan:** Execute a parallel strategy centered on handheld consoles (Nintendo) and Role-Playing Games (RPG).
3. **Do Not Rely on User Scores:** To forecast sales, focus promotional efforts on securing strong reviews from specialized gaming press (Critics), which correlate far better with financial performance.

## 🛠️ Tech Stack

* **Language:** Python
* **Libraries:** Pandas, NumPy, SciPy (Stats), Matplotlib, Seaborn, Plotly, Streamlit
* **Techniques:** EDA, Data Cleaning, Multivariate Analysis, Student's t-test, Levene's Test.

## 🔗 Full Analysis & Production App

* 📓 [Original Jupyter Notebook with full code and visualizations](notebooks/analisis-videojuegos.ipynb)
* 🚀 [Interactive Regional Sales Explorer (Streamlit)](https://videogames-regional-sales-analysis.streamlit.app/)

## ▶️ How to Run Locally

    pip install -r requirements.txt
    streamlit run app.py

---

# 🎮 Análisis de Ventas de Videojuegos: Estrategia Regional para 2017

> Análisis exploratorio de datos (EDA) y pruebas de hipótesis estadísticas para identificar los patrones de éxito de los videojuegos y planificar campañas comerciales regionales para el año 2017.

🚀 **[Abrir App Interactiva en Streamlit](https://videogames-regional-sales-analysis.streamlit.app/)** | 🌐 **[Ver Reporte Web en Quarto](https://andagui-ds.github.io/videogames-regional-sales-analysis/)**

---

## 🎯 Problema de Negocio

La tienda de videojuegos **Streamchik** (Ice) necesita identificar qué hace que un videojuego tenga éxito comercial para planificar sus campañas de marketing y publicidad de cara a 2017.

El análisis debe responder a tres preguntas clave:
1. ¿Qué plataformas y géneros dominan el mercado actual?
2. ¿Existen diferencias significativas en las preferencias de los usuarios entre Norteamérica (NA), Europa (EU) y Japón (JP)?
3. ¿Las reseñas de los usuarios y críticos afectan de la misma manera a las ventas en todas las plataformas?

## 📊 Datos y Preprocesamiento

* **Fuente:** `games.csv` (16,713 registros y 11 columnas).
* **Limpieza:**
  * Reemplazo de valores `TBD` (*To Be Determined*) en `user_score` por nulos (`NaN`) y conversión a tipo flotante.
  * Imputación de años faltantes (`year_of_release`) cruzando información de otras plataformas para el mismo juego.
  * Relleno de clasificaciones ESRB nulas con la categoría `"Unknown"`.
  * Cálculo de la columna derivada `total_sales` (suma de ventas NA + EU + JP + Other).
* **Filtrado Temporal:** Se determinó que los datos anteriores a 2013-2014 no son representativos para predecir 2017 (las consolas tienen un ciclo de vida de ~5 años). El análisis final se centró en la era reciente (2013-2016).

## 🧠 Hallazgos Clave (EDA)

1. **Ciclo de Vida de las Plataformas:** Las consolas suelen tener una vida útil de 5 a 7 años. Las plataformas líderes históricas (PS2, Xbox 360) han sido desplazadas por la octava generación.
2. **Líderes Recientes (2013-2016):** **PS4** y **Xbox One (XOne)** dominan abrumadoramente el volumen de ventas en la era actual.
3. **Impacto de las Reseñas (Caso PS4):**
   * Las reseñas de **Críticos** tienen una correlación positiva moderada con las ventas (`0.40`).
   * Las reseñas de **Usuarios** tienen una correlación prácticamente nula (`-0.04`), indicando que los usuarios califican por motivaciones emocionales y no necesariamente predicen el éxito comercial.

## 📈 Perfiles Regionales

Se identificaron diferencias críticas en el comportamiento del consumidor por región:

* **Norteamérica (NA) y Europa (EU):** Las plataformas dominantes son PS4 y XOne. Los géneros favoritos son **Action** y **Shooter** (disparos). Las clasificaciones ESRB más populares son "M" (Maduro) y "E" (Todos).
* **Japón (JP):** El mercado es completamente distinto. La plataforma líder es la portátil **Nintendo 3DS**. El género dominante es **Role-Playing (RPG)**. La clasificación ESRB casi no tiene relevancia en Japón (la mayoría son "Unknown").

## 🔬 Pruebas de Hipótesis Estadísticas (Alpha = 0.05)

Se utilizó la **prueba t de Student para muestras independientes** (con `equal_var=False` / Prueba de Welch, tras validar varianzas desiguales con la prueba de Levene).

* **Hipótesis 1:** "Las calificaciones promedio de los usuarios para Xbox One y PC son las mismas".
  * *Resultado:* No se rechaza la Hipótesis Nula. Estadísticamente, las calificaciones son iguales.
* **Hipótesis 2:** "Las calificaciones promedio de los usuarios para los géneros de Acción y Deportes son diferentes".
  * *Resultado:* Se rechaza la Hipótesis Nula. Existe una diferencia estadísticamente significativa en la percepción de los jugadores hacia estos dos géneros.

## ✅ Recomendaciones de Negocio (Campaña 2017)

1. **Priorizar PS4 y Xbox One:** El presupuesto de marketing debe enfocarse en estas plataformas de octava generación.
2. **Estrategia Glocal (Global + Local):**
   * En **NA y EU**: Invertir fuertemente en campañas para juegos *AAA* de Acción, Shooters y Deportes.
   * En **Japón**: Desarrollar una estrategia paralela enfocada en consolas portátiles (Nintendo) y juegos de rol (RPG).
3. **No depender del *User Score*:** Para predecir ventas, enfocar los esfuerzos de marketing en obtener buenas reseñas de la prensa especializada (Critics), que demostraron una mejor correlación con el éxito financiero.

## 🛠️ Stack Técnico

* **Lenguajes:** Python
* **Librerías:** Pandas, NumPy, SciPy (Stats), Matplotlib, Seaborn, Plotly, Streamlit
* **Técnicas:** EDA, Limpieza de datos, Análisis Multivariado, Prueba t de Student, Prueba de Levene.

## 🔗 Ver el Análisis Completo y App en Vivo

* 📓 [Notebook original con todo el código y las gráficas](notebooks/analisis-videojuegos.ipynb)
* 🚀 [Explorador Interactivo de Ventas Regionales (Streamlit)](https://videogames-regional-sales-analysis.streamlit.app/)

## ▶️ Cómo ejecutar localmente

    pip install -r requirements.txt
    streamlit run app.py
