import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import matplotlib.ticker as mtick

from data_processing import build_processed_dataframes

COLOR_FONDO = "#F7F7F2"
COLOR_TEXTO = "#1F2937"
COLOR_GRID = "#D0D7DE"

COLOR_PRINCIPAL = "#1D4E89"
COLOR_SECUNDARIO = "#2A9D8F"
COLOR_RESALTE = "#E9C46A"
COLOR_ALERTA = "#D95D39"
COLOR_NEUTRO = "#8D99AE"

PALETA = [
    COLOR_PRINCIPAL,
    COLOR_SECUNDARIO,
    COLOR_RESALTE,
    COLOR_ALERTA,
    COLOR_NEUTRO,
    "#84A59D"
]

CMAP_CORR = "RdBu_r"

plt.rcParams.update({
    "figure.facecolor": COLOR_FONDO,
    "axes.facecolor": COLOR_FONDO,
    "savefig.facecolor": COLOR_FONDO,
    "axes.edgecolor": "#AAB4BE",
    "axes.labelcolor": COLOR_TEXTO,
    "axes.titlecolor": COLOR_TEXTO,
    "xtick.color": COLOR_TEXTO,
    "ytick.color": COLOR_TEXTO,
    "text.color": COLOR_TEXTO,
    "grid.color": COLOR_GRID,
    "grid.alpha": 0.35,
    "font.family": "sans-serif",
    "font.sans-serif": ["Aptos", "DejaVu Sans"],
    "axes.titlesize": 14,
    "axes.titleweight": "bold",
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 120
})

def _categorize_margin(abs_diff):
        """Clasifica un partido segun su diferencia absoluta de goles"""
        if abs_diff == 0:
            return "0 (Empate)"
        elif abs_diff == 1:
            return "1 (Cerrado)"
        elif abs_diff == 2:
            return "2 (Moderado)"
        else:
            return "3+ (Amplio)"


def plot_analisis_01(df_player_latest_imputed: pd.DataFrame):
    """Genera el heatmap de correlacion de atributos para jugadores de campo"""

    # Nos quedamos solo con jugadores de campo
    df_outfield = df_player_latest_imputed.copy()
    df_outfield = df_outfield[df_outfield["PLAYER_TYPE"] == "OUTFIELD"]

    # Seleccionamos atributos relevantes para jugadores de campo
    cols = [
        "OVERALL_RATING",
        "POTENTIAL",
        "CROSSING",
        "FINISHING",
        "SHORT_PASSING",
        "DRIBBLING",
        "LONG_PASSING",
        "BALL_CONTROL",
        "ACCELERATION",
        "SPRINT_SPEED",
        "REACTIONS",
        "SHOT_POWER",
        "STAMINA",
        "INTERCEPTIONS",
        "POSITIONING",
        "VISION",
        "STANDING_TACKLE"
    ]

    # Calculamos la matriz de correlacion
    df_corr = df_outfield[cols].copy()
    corr = df_corr.corr(method = "spearman")

    # Preparamos labels mas limpios para el grafico
    labels = [col.replace("_", " ") for col in corr.columns]

    # Graficamos el heatmap
    fig, ax = plt.subplots(figsize = (12, 9))
    im = ax.imshow(corr.values, cmap = CMAP_CORR, vmin = -1, vmax = 1)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation = 90, ha = "right")
    ax.set_yticklabels(labels)

    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr.values[i, j]
            color = "white" if abs(value) >= 0.60 else "black"
            ax.text(j, i, f"{value:.2f}", ha = "center", va = "center", color = color, fontsize = 8)

    ax.set_title("Correlación de atributos de jugadores de campo", loc = "left", pad = 15)
    ax.tick_params(length = 0)
    cbar = plt.colorbar(im, ax = ax, shrink=0.85)
    cbar.set_label("Correlación de Spearman")

    fig.tight_layout()
    return fig

def plot_analisis_02(df_player_latest_imputed: pd.DataFrame):
    """Genera el heatmap de correlacion de atributos para porteros"""

    # Nos quedamos solo con porteros
    df_goalkeepers = df_player_latest_imputed.copy()
    df_goalkeepers = df_goalkeepers[df_goalkeepers["PLAYER_TYPE"] == "GOALKEEPER"]

    # Seleccionamos atributos relevantes para porteros
    cols = [
        "OVERALL_RATING",
        "POTENTIAL",
        "REACTIONS",
        "JUMPING",
        "GK_DIVING",
        "GK_HANDLING",
        "GK_KICKING",
        "GK_POSITIONING",
        "GK_REFLEXES",
        "GK_MEAN"
    ]

    # Calculamos la matriz de correlacion
    df_corr = df_goalkeepers[cols].copy()
    corr = df_corr.corr(method = "spearman")

    # Preparamos labels mas limpios para el grafico
    labels = [col.replace("_", " ") for col in corr.columns]

    # Graficamos el heatmap
    fig, ax = plt.subplots(figsize = (12, 9))
    im = ax.imshow(corr.values, cmap = CMAP_CORR, vmin = -1, vmax = 1)

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation = 90, ha = "right")
    ax.set_yticklabels(labels)

    for i in range(len(labels)):
        for j in range(len(labels)):
            value = corr.values[i, j]
            color = "white" if abs(value) >= 0.60 else "black"
            ax.text(j, i, f"{value:.2f}", ha = "center", va = "center", color = color, fontsize = 8)

    ax.set_title("Correlación de atributos de jugadores porteros", loc = "left", pad = 15)
    ax.tick_params(length = 0)

    cbar = plt.colorbar(im, ax = ax, shrink = 0.85)
    cbar.set_label("Correlación de Spearman")

    fig.tight_layout()
    return fig

def plot_analisis_03(df_player_latest_imputed: pd.DataFrame):
    """Genera el histograma del gap de desarrollo para jugadores de campo jovenes"""

    df_gap = df_player_latest_imputed.copy()

    # Filtramos solo jugadores jovenes
    df_gap = df_gap[df_gap["AGE"].between(18, 23)].copy()

    # Calculamos el gap entre potential y overall rating
    df_gap["GAP"] = df_gap["POTENTIAL"] - df_gap["OVERALL_RATING"]

    # Nos quedamos solo con jugadores de campo
    df_gap_outfield = df_gap[df_gap["PLAYER_TYPE"] == "OUTFIELD"].copy()

    # Como el gap es entero, usamos un bucket por valor entero
    out_min = int(df_gap_outfield["GAP"].min())
    out_max = int(df_gap_outfield["GAP"].max())

    bins_outfield = np.arange(out_min - 0.5, out_max + 1.5, 1)
    x_ticks = np.arange(out_min, out_max + 1, 1)

    # Estilo base del histograma
    hist_style = {"alpha": 0.9, "edgecolor": "white", "linewidth": 1.2}

    # Graficamos
    fig, ax = plt.subplots(figsize = (12, 6))

    ax.hist(df_gap_outfield["GAP"].dropna(), bins = bins_outfield, color = COLOR_PRINCIPAL, **hist_style)

    ax.set_title("Distribución del gap de desarrollo en jugadores de campo jóvenes (18-23)", fontsize = 16, fontweight = "bold", pad = 18)
    ax.set_xlabel("Gap de desarrollo (Potential - Overall Rating)", fontsize = 12)
    ax.set_ylabel("Numero de jugadores", fontsize = 12)
    ax.grid(axis = "y", alpha = 0.2, linestyle = "--", linewidth = 0.8)

    ax.set_xlim(out_min - 0.5, out_max + 0.5)
    ax.set_xticks(x_ticks)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(0.5, 0.02, "Gap positivo = potencial sin desarrollar", ha = "center", fontsize = 10, style = "italic", color = COLOR_NEUTRO)

    plt.tight_layout()
    plt.subplots_adjust(bottom = 0.12)
    return fig

def plot_analisis_04(df_player_latest_imputed: pd.DataFrame):
    """Genera el histograma del gap de desarrollo para porteros jovenes"""

    df_gap = df_player_latest_imputed.copy()

    # Filtramos solo jugadores jovenes
    df_gap = df_gap[df_gap["AGE"].between(18, 23)].copy()

    # Calculamos el gap entre potential y overall rating
    df_gap["GAP"] = df_gap["POTENTIAL"] - df_gap["OVERALL_RATING"]

    # Nos quedamos solo con porteros
    df_gap_gk = df_gap[df_gap["PLAYER_TYPE"] == "GOALKEEPER"].copy()

    # Como el gap es entero, usamos un bucket por valor entero
    gk_min = int(df_gap_gk["GAP"].min())
    gk_max = int(df_gap_gk["GAP"].max())

    bins_gk = np.arange(gk_min - 0.5, gk_max + 0.5, 1)
    x_ticks = np.arange(gk_min, gk_max + 1, 1)

    # Estilo base del histograma
    hist_style = {"alpha": 0.9, "edgecolor": "white", "linewidth": 1.2}

    # Graficamos
    fig, ax = plt.subplots(figsize = (12, 6))

    ax.hist(df_gap_gk["GAP"].dropna(), bins = bins_gk, color = COLOR_SECUNDARIO, **hist_style)

    ax.set_title("Distribución del gap de desarrollo en porteros jóvenes (18-23)", fontsize = 16, fontweight = "bold", pad = 18)
    ax.set_xlabel("Gap de desarrollo (Potential - Overall Rating)", fontsize = 12)
    ax.set_ylabel("Número de porteros", fontsize = 12)
    ax.grid(axis = "y", alpha = 0.2, linestyle = "--", linewidth = 0.8)

    ax.set_xlim(gk_min - 0.5, gk_max + 0.5)
    ax.set_xticks(x_ticks)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.text(
        0.5,
        0.02,
        "Gap positivo = potencial sin desarrollar",
        ha = "center",
        fontsize = 10,
        style = "italic",
        color = COLOR_NEUTRO
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom = 0.12)
    return fig

def plot_analisis_05(df_player_latest_imputed: pd.DataFrame):
    """Genera el grafico de barras de atributos que distinguen a jugadores de campo jovenes de alto potencial"""

    # Nos quedamos solo con jugadores de campo jovenes
    df_young = df_player_latest_imputed.copy()
    df_young = df_young[df_young["PLAYER_TYPE"] == "OUTFIELD"]
    df_young = df_young[df_young["AGE"].between(18, 23)]

    # Seleccionamos atributos de jugadores de campo
    attr_cols = [
        "CROSSING",
        "FINISHING",
        "HEADING_ACCURACY",
        "SHORT_PASSING",
        "VOLLEYS",
        "DRIBBLING",
        "CURVE",
        "FREE_KICK_ACCURACY",
        "LONG_PASSING",
        "BALL_CONTROL",
        "ACCELERATION",
        "SPRINT_SPEED",
        "AGILITY",
        "REACTIONS",
        "BALANCE",
        "SHOT_POWER",
        "JUMPING",
        "STAMINA",
        "STRENGTH",
        "LONG_SHOTS",
        "AGGRESSION",
        "INTERCEPTIONS",
        "POSITIONING",
        "VISION",
        "PENALTIES",
        "MARKING",
        "STANDING_TACKLE",
        "SLIDING_TACKLE"
    ]

    # Definimos el grupo de alto potencial como el top 10 por ciento
    potential_cutoff = df_young["POTENTIAL"].quantile(0.90)
    df_high_potential = df_young[df_young["POTENTIAL"] >= potential_cutoff].copy()

    # Definimos el grupo de referencia como el resto de jugadores jovenes
    df_reference = df_young[df_young["POTENTIAL"] < potential_cutoff].copy()

    # Calculamos diferencia de promedios por atributo
    mean_diff = df_high_potential[attr_cols].mean() - df_reference[attr_cols].mean()

    # Nos quedamos con los 12 atributos que mas distinguen al grupo
    mean_diff = mean_diff.sort_values(ascending=False).head(12).sort_values(ascending=True)

    # Preparamos labels y colores
    labels = [col.replace("_", " ") for col in mean_diff.index]

    bar_colors = [COLOR_PRINCIPAL] * len(mean_diff)    # Generamos la lista de colores usando list comprehension
    if len(bar_colors) >= 3:
        bar_colors[-1] = COLOR_RESALTE    # Resaltamos el atributo que mas distigue al grupo
        bar_colors[-2] = COLOR_RESALTE    # Resaltamos el 2do atributo que mas distingue al grupo
        bar_colors[-3] = COLOR_SECUNDARIO    # Resaltamos el 3er atributo que mas distingue al grupo, con un nivel de resalte menor al 1ro y 2do

    # Graficamos
    fig, ax = plt.subplots(figsize = (10, 7))
    bars = ax.barh(labels, mean_diff.values, color = bar_colors)

    # Agregamos el valor al final de cada barra
    for bar, value in zip(bars, mean_diff.values):
        ax.text(value + 0.25, bar.get_y() + bar.get_height() / 2, f"{value:.1f}", va = "center", fontsize = 9)    # .get_y obtiene el piso, .get_height()/2 lo centra verticalmente

    ax.set_title("Atributos que mas distinguen a jugadores jóvenes (18-23) de alto potencial (mejor 10%)", loc = "left", pad = 15)
    ax.set_xlabel("Diferencia de promedio frente al grupo de referencia (peor 90%)")
    ax.set_ylabel("")
    ax.grid(axis = "x")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.text(0.98, 0.03, f"Corte valor potencial: {potential_cutoff:.0f}\n# alto potencial: {len(df_high_potential)}", transform = ax.transAxes, ha = "right", va = "bottom", fontsize = 9)

    fig.tight_layout()
    return fig

def plot_analisis_06(df_team_match: pd.DataFrame):
    """Genera el grafico de anillo del margen de victoria en los partidos"""

    # Nos quedamos con un solo registro por partido
    df_matches = df_team_match[df_team_match["IS_HOME"] == 1].copy()
    df_matches = df_matches.dropna(subset = ["ABS_GOAL_DIFF"])

    df_matches["MARGIN"] = df_matches["ABS_GOAL_DIFF"].apply(_categorize_margin)

    # Se cuentan frecuencias y calculamos porcentajes
    margin_order = ["0 (Empate)", "1 (Cerrado)", "2 (Moderado)", "3+ (Amplio)"]

    margin_counts = (df_matches["MARGIN"].value_counts().reindex(margin_order, fill_value = 0))

    margin_pct = margin_counts / margin_counts.sum() * 100

    # Preparamos etiquetas con cantidad de partidos
    label_map = {
        "0 (Empate)": "Empate\n(0 goles de diferencia)",
        "1 (Cerrado)": "Cerrado\n(1 gol de diferencia)",
        "2 (Moderado)": "Moderado\n(2 goles de diferencia)",
        "3+ (Amplio)": "Amplio\n(3 o más goles de diferencia)"
    }

    # Usamos list comprehension para generar las etiquetas para cada categoria, incluyendo el conteo de partidos
    labels = [f"{label_map[categoria]}\n{margin_counts.loc[categoria]:,} partidos" for categoria in margin_order]

    # Se fijan colores para que el grafico sea consistente con la paleta de colores seleccionada
    donut_colors = [COLOR_NEUTRO, COLOR_SECUNDARIO, COLOR_RESALTE, COLOR_ALERTA]

    # Graficamos el anillo
    fig, ax = plt.subplots(figsize = (11, 8))

    wedges, texts, autotexts = ax.pie(
        margin_pct.values,
        labels = labels,
        autopct = "%1.1f%%",
        startangle = 90,
        counterclock = False,
        colors = donut_colors,
        wedgeprops = dict(width = 0.40, edgecolor = "white", linewidth = 2.5),    # Este parametro hace que el grafico de pie se convierta en uno de anillo
        pctdistance = 0.78,
        labeldistance = 1.12,
        textprops = dict(fontsize = 10, fontweight = "bold", color = COLOR_TEXTO)
    )

    # Ajustamos el estilo de los porcentajes dentro del anillo
    for autotext in autotexts:
        autotext.set_color("white")
        autotext.set_fontsize(10)
        autotext.set_fontweight("bold")

    # Texto central
    ax.text(0, 0, f"Total\n{int(margin_counts.sum()):,}\npartidos", ha = "center", va = "center", fontsize = 12, fontweight = "bold", color = COLOR_TEXTO)

    # Titulo
    ax.set_title("Distribución del margen de victoria en los partidos", fontsize = 15, fontweight = "bold", pad = 20)

    plt.tight_layout()
    return fig

def plot_analisis_07(df_player_latest_imputed: pd.DataFrame):
    """Genera el boxplot de atributos para altas promesas de campo frente al resto de jugadores jovenes"""

    # Definimos los colores (rosa para las promesas, gris para el resto)
    paleta_boxplot = {"Alta Promesa (Top 10%)": COLOR_RESALTE, "Resto de Jovenes": COLOR_PRINCIPAL}

    # Nos quedamos solo con jugadores de campo jovenes
    df_young = df_player_latest_imputed.copy()
    df_young = df_young[df_young["PLAYER_TYPE"] == "OUTFIELD"]

    # Filtramos para comparar solo jugadores jovenes (18-23 años)
    df_young = df_young[df_young["AGE"].between(18, 23)]

    # Definimos el umbral del Top 10% de potencial
    umbral_top = df_young["POTENTIAL"].quantile(0.80)

    # Creamos una nueva columna para clasificar a los jugadores
    df_young["PROSPECT_LEVEL"] = np.where(df_young["POTENTIAL"] >= umbral_top, "Alta Promesa (Top 10%)", "Resto de Jovenes")

    # Seleccionamos 6 atributos clave para que el Boxplot sea legible
    atributos = ['BALL_CONTROL', 'VISION', 'REACTIONS', 'SHORT_PASSING', 'SPRINT_SPEED', 'STAMINA']

    # Transformamos los datos a formato largo (melt) para que Seaborn pueda agruparlos
    df_melted = df_young.melt(id_vars=["PROSPECT_LEVEL"], value_vars=atributos, var_name="ATRIBUTO", value_name="PUNTUACION")

    # Limpiamos los nombres de los atributos quitando el guion bajo
    df_melted["ATRIBUTO"] = df_melted["ATRIBUTO"].str.replace("_", " ")

    # Construimos y mostramos la grafica
    fig, ax = plt.subplots(figsize=(12, 6))

    sns.boxplot(data=df_melted, x="ATRIBUTO", y="PUNTUACION", hue="PROSPECT_LEVEL", palette=paleta_boxplot, ax=ax)

    # Titulos y etiquetas
    ax.set_title("Distribución de atributos de jugadores de campo jóvenes (18 - 23): Altas Promesas vs Resto de Jóvenes", loc="left", pad=15)
    ax.set_xlabel("Atributos Evaluados")
    ax.set_ylabel("Puntuación del Atributo")

    # Movemos la leyenda para que no tape los datos
    sns.move_legend(ax, "lower right", title="Nivel de Prospecto")
    ax.grid(axis='y', linestyle='--', alpha=0.6)

    fig.tight_layout()
    return fig

def plot_analisis_08(df_player_latest: pd.DataFrame):
    """Genera el grafico de lineas de nivel promedio de jugador por edad"""

    df_player = df_player_latest.copy()
    
    # Contamos cuantos jugadores hay por cada edad
    conteo_edades = df_player.groupby("AGE").size()

    # Nos quedamos solo con edades con muestra suficiente
    edades_validas = conteo_edades[conteo_edades >= 10].index
    df_player = df_player[df_player["AGE"].isin(edades_validas)]

    # Calculamos el overall promedio por edad
    promedio_por_edad = df_player.groupby("AGE")["OVERALL_RATING"].mean()

    # Graficamos
    fig, ax = plt.subplots(figsize = (10, 6))

    ax.plot(
        promedio_por_edad.index,
        promedio_por_edad.values,
        marker = "o",
        color = COLOR_PRINCIPAL,
        linewidth = 2.5,
        markersize = 6
    )

    ax.set_title("Nivel promedio de los jugadores según su edad (Overall Rating)", loc = "left", pad = 15)
    ax.set_xlabel("Edad")
    ax.set_ylabel("Nivel promedio (Overall Rating)")
    ax.grid(linestyle = "--", alpha = 0.6)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    return fig


def plot_analisis_09(df_team_match: pd.DataFrame):
    """Genera el bubble plot de formaciones: rendimiento vs frecuencia de uso"""

    # Filtramos y agrupamos por formacion
    df_form = (
        df_team_match
        .dropna(subset = ["FORMATION"])
        .groupby("FORMATION")
        .agg(
            count = ("MATCH_ID", "count"),
            avg_points = ("POINTS", "mean"),
            avg_goal_diff = ("GOAL_DIFF", "mean"),
            is_home_rate = ("IS_HOME", "mean")
        )
        .reset_index()
    )

    # Nos quedamos con las formaciones mas usadas
    df_form = (df_form[df_form["count"] >= 20].sort_values("count", ascending = False).head(10))

    # Graficamos
    fig, ax = plt.subplots(figsize = (11, 7))

    scatter = ax.scatter(
        df_form["avg_goal_diff"],
        df_form["avg_points"],
        s = df_form["count"] * 1.5,
        c = df_form["is_home_rate"],
        cmap = "Blues",
        alpha = 0.8,
        edgecolors = "white",
        linewidth = 1.2
    )

    # Barra de color
    cbar = plt.colorbar(scatter, ax = ax, shrink = 0.85)
    cbar.set_label("Tasa de partidos en casa", fontsize = 10, color = COLOR_TEXTO)
    cbar.outline.set_edgecolor(COLOR_GRID)

    # Se agregan etiquetas a cada burbuja y se ajustan sus posiciones para que sean legibles
    offsets = [0.012, -0.012]

    for i, row in enumerate(df_form.itertuples()):
        dy = offsets[i % len(offsets)]    # Para alternar entre arriba y abajo del centro

        ax.text(
            row.avg_goal_diff,
            row.avg_points + dy,
            row.FORMATION,
            ha = "center",
            va = "bottom" if dy > 0 else "top",
            fontsize = 9,
            fontweight = "bold",
            color = COLOR_TEXTO,
            bbox = dict(
                facecolor = "white",
                edgecolor = COLOR_GRID,
                boxstyle = "round,pad=0.2"
            )
        )

    ax.axvline(0, color = COLOR_GRID, linestyle = "--", linewidth = 1)
    ax.set_title("Formaciones: rendimiento vs frecuencia de uso", loc = "left", pad = 15)
    ax.set_xlabel("Diferencia de gol promedio")
    ax.set_ylabel("Puntos promedio por partido")
    ax.grid(alpha = 0.25, linestyle = "--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.margins(x = 0.2, y = 0.2)

    fig.text(
        0.31,
        0.02,
        "Tamano de burbuja = cantidad de partidos\nLas 10 formaciones mas usadas",
        ha = "center",
        fontsize = 10,
        color = COLOR_NEUTRO
    )

    plt.tight_layout()
    plt.subplots_adjust(bottom = 0.10)
    return fig


def plot_analisis_10(df_team_match: pd.DataFrame):
    """Genera el grafico de barras apiladas de victorias, empates y derrotas por formacion"""

    # Copiamos y limpiamos datos base
    df_form = df_team_match.copy()
    df_form = df_form.dropna(subset = ["FORMATION", "RESULT"])

    # Mapeamos de letra a palabra completa
    map_result = {
    "W": "WIN",
    "D": "DRAW",
    "L": "LOSS"
    }

    df_form["RESULT_CLEAN"] = df_form["RESULT"].map(map_result)

    # Agrupamos formaciones poco frecuentes como OTRAS
    conteo_formaciones = df_form["FORMATION"].value_counts()
    min_partidos = 20

    formaciones_validas = conteo_formaciones[conteo_formaciones >= min_partidos].index

    df_form["FORMATION_CLEAN"] = df_form["FORMATION"].apply(
        lambda value: value if value in formaciones_validas else "OTRAS"
    )

    # Usando crosstab analisamos la proporcion de resultados por formacion
    tabla = pd.crosstab(
        df_form["FORMATION_CLEAN"],
        df_form["RESULT_CLEAN"],
        normalize = "index"
    )

    for col in ["WIN", "DRAW", "LOSS"]:
        if col not in tabla.columns:
            tabla[col] = 0

    # Ordenamos por victorias
    tabla = tabla[["WIN", "DRAW", "LOSS"]]
    tabla = tabla.sort_values(by = "WIN", ascending = False)

    # Graficamos
    fig, ax = plt.subplots(figsize = (12, 7))

    x = np.arange(len(tabla.index))

    ax.bar(x, tabla["WIN"], label = "Victoria", color = COLOR_SECUNDARIO)
    ax.bar(x, tabla["DRAW"], bottom = tabla["WIN"], label = "Empate", color = COLOR_RESALTE)
    ax.bar(x, tabla["LOSS"], bottom = tabla["WIN"] + tabla["DRAW"], label = "Derrota", color = COLOR_ALERTA)

    ax.set_xticks(x)
    ax.set_xticklabels(tabla.index, rotation = 90, ha = "right")
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))

    ax.set_title("Proporción de victorias, empates y derrotas por formación", loc = "left", pad = 15)
    ax.set_xlabel("Formación")
    ax.set_ylabel("Proporción de resultados")
    ax.grid(axis = "y", linestyle = "--")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.legend()
    fig.tight_layout()
    return fig

def build_graph_figures(database_path: str):
    """Corre todas las funciones de graficos y devuelve cada una de las figuras"""

    df_player_latest, df_player_latest_imputed, df_team_match = build_processed_dataframes(database_path)

    fig_analisis_01 = plot_analisis_01(df_player_latest_imputed)
    fig_analisis_02 = plot_analisis_02(df_player_latest_imputed)
    fig_analisis_03 = plot_analisis_03(df_player_latest_imputed)
    fig_analisis_04 = plot_analisis_04(df_player_latest_imputed)
    fig_analisis_05 = plot_analisis_05(df_player_latest_imputed)
    fig_analisis_06 = plot_analisis_06(df_team_match)
    fig_analisis_07 = plot_analisis_07(df_player_latest_imputed)
    fig_analisis_08 = plot_analisis_08(df_player_latest)
    fig_analisis_09 = plot_analisis_09(df_team_match)
    fig_analisis_10 = plot_analisis_10(df_team_match)

    return fig_analisis_01, fig_analisis_02, fig_analisis_03, fig_analisis_04, fig_analisis_05, fig_analisis_06, fig_analisis_07, fig_analisis_08, fig_analisis_09, fig_analisis_10