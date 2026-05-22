import pandas as pd
import numpy as np
import re
import sqlite3

# Helper functions
def _clean_column_names(col_names: list[str]) -> dict:
    """Cleans a list of strings and returns a dictionary that maps said said list to their cleaned versions"""
    cleaned_list = [name.strip().upper().replace(" ", "_").strip("_") for name in col_names]
    cleaned_list = [re.sub(r"[^A-Z_0-9]", "", name) for name in cleaned_list]
    cleaned_list = [re.sub(r"_+", "_", name) for name in cleaned_list]

    clean_column_dict = {}
    for index, name in enumerate(col_names):
        clean_column_dict[name] = cleaned_list[index]

    return clean_column_dict

def _clean_df_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Changes the column index of a dataframe for its cleaned version"""

    df_columns = df.columns.tolist()
    map_cleaned_columns = _clean_column_names(df_columns)
    df = df.rename(columns=map_cleaned_columns)

    return df

def _impute_categorical_nan_with_mode(df: pd.DataFrame, columns: list, group_col: str) -> pd.DataFrame:
    """Imputes missing values in categorical columns using the mode of each group in group_col"""

    df = df.copy()

    for col in columns:
        mode = df[col].mode(dropna=True)
        if len(mode) > 0:
            mode = mode.iloc[0]
        else:
            mode = "UNKNOWN"

        for group_value in df[group_col].dropna().unique():
            group_values = df[group_col].eq(group_value)
            group_mode = df.loc[group_values, col].mode(dropna=True)

            if len(group_mode) > 0:
                df.loc[group_values, col] = df.loc[group_values, col].fillna(group_mode.iloc[0])

        df[col] = df[col].fillna(mode)

    return df

def _impute_numeric_nan_with_median(df: pd.DataFrame, columns: list, group_col: str) -> pd.DataFrame:
    """Imputes missing values in numeric columns using the median of each group in group col"""

    df = df.copy()

    for col in columns:
        median = df[col].median()

        for group_value in df[group_col].dropna().unique():
            group_values = df[group_col].eq(group_value)
            group_median = df.loc[group_values, col].median()
            df.loc[group_values, col] = df.loc[group_values, col].fillna(group_median)

        df[col] = df[col].fillna(median)

    return df

def _infer_formation_from_row(row: pd.Series | pd.DataFrame, prefix: str) -> str:
    """Infers the formation of a team using the Y coordinates of the 11 players"""

    y_columns = [f"{prefix}_PLAYER_Y{i}" for i in range(1, 12)]
    y_values = row[y_columns].tolist()
    y_values = [int(value) for value in y_values if pd.notna(value)]

    # Si no tenemos los 11 jugadores, no inferimos la formacion
    if len(y_values) < 11:
        return np.nan

    # Contamos cuantos jugadores hay en cada linea vertical del esquema
    counts_by_y_value = pd.Series(y_values).value_counts().sort_index()

    # Si la primera linea tiene un solo jugador, asumimos que es el portero
    if len(counts_by_y_value) >= 2 and counts_by_y_value.iloc[0] == 1:
        counts_by_y_value = counts_by_y_value.iloc[1:]

    formation = "-".join([str(int(value)) for value in counts_by_y_value.tolist()])

    return formation

def _add_match_result_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Given a match df that has one row per team per match, adds extra result related columns"""

    df = df.copy()

    # Se agregan las columnas:
    # goal_diff (diferencia de goles HOME vs AWAY team)
    # abs_goal_diff (valor absoluto de la diferencia de goles)
    # total_goals (goles totales de ambos equipos)
    # results ("W" si gano, "D" si empato, "L" si perdio)
    # points (se agregan los puntos ganados en el sistema de la FIFA, 3 por ganar, 1 por empatar, 0 por perder)
    df["GOAL_DIFF"] = df["GOALS_FOR"] - df["GOALS_AGAINST"]
    df["ABS_GOAL_DIFF"] = df["GOAL_DIFF"].abs()
    df["TOTAL_GOALS"] = df["GOALS_FOR"] + df["GOALS_AGAINST"]
    df["RESULT"] = np.select([df["GOALS_FOR"] > df["GOALS_AGAINST"], df["GOALS_FOR"] == df["GOALS_AGAINST"]], ["W", "D"], default="L")
    df["POINTS"] = np.select([df["GOALS_FOR"] > df["GOALS_AGAINST"], df["GOALS_FOR"] == df["GOALS_AGAINST"]], [3, 1], default=0)

    return df

def _build_team_match_side(df: pd.DataFrame, side: str) -> pd.DataFrame:
    """Builds the team-match dataframe for one side of the match"""

    if side == "HOME":
        opponent_side = "AWAY"
        is_home = 1
    elif side == "AWAY":
        opponent_side = "HOME"
        is_home = 0

    df_side = df[
        [
            "ID",
            "MATCH_API_ID",
            "DATE",
            "SEASON",
            "STAGE",
            "COUNTRY_ID",
            "COUNTRY_NAME",
            "LEAGUE_ID",
            "LEAGUE_NAME",
            f"{side}_TEAM_API_ID",
            f"{side}_TEAM_FIFA_API_ID",
            f"{side}_TEAM_LONG_NAME",
            f"{side}_TEAM_SHORT_NAME",
            f"{opponent_side}_TEAM_API_ID",
            f"{opponent_side}_TEAM_FIFA_API_ID",
            f"{opponent_side}_TEAM_LONG_NAME",
            f"{opponent_side}_TEAM_SHORT_NAME",
            f"{side}_TEAM_GOAL",
            f"{opponent_side}_TEAM_GOAL",
            f"{side}_FORMATION",
        ]
    ].copy()

    # Renombramos columnas
    df_side = df_side.rename(
        columns={
            "ID": "MATCH_ID",
            f"{side}_TEAM_API_ID": "TEAM_API_ID",
            f"{side}_TEAM_FIFA_API_ID": "TEAM_FIFA_API_ID",
            f"{side}_TEAM_LONG_NAME": "TEAM_LONG_NAME",
            f"{side}_TEAM_SHORT_NAME": "TEAM_SHORT_NAME",
            f"{opponent_side}_TEAM_API_ID": "OPPONENT_API_ID",
            f"{opponent_side}_TEAM_FIFA_API_ID": "OPPONENT_FIFA_API_ID",
            f"{opponent_side}_TEAM_LONG_NAME": "OPPONENT_LONG_NAME",
            f"{opponent_side}_TEAM_SHORT_NAME": "OPPONENT_SHORT_NAME",
            f"{side}_TEAM_GOAL": "GOALS_FOR",
            f"{opponent_side}_TEAM_GOAL": "GOALS_AGAINST",
            f"{side}_FORMATION": "FORMATION",
        }
    )

    df_side["MATCH_SIDE"] = side
    df_side["IS_HOME"] = is_home

    # Usamoe la helper function _add_match_result_columns para agregar columnas relevantes relacionadas a los resultados
    df_side = _add_match_result_columns(df_side)

    return df_side

# Main function
def build_processed_dataframes(database_path: str):
    """Main function, receives the path of the database and returns the dataframes to work with"""
    connection = sqlite3.connect(database_path)

    try:
        # Lectura de datos

        # Como el proposito de esta materia no es aprender sql, manipularemos los datos usando pandas Dataframes.
        # Es por esto que necesitamos leer cada una de las tablas de la base de datos como un dataframe.
        df_player = pd.read_sql_query("SELECT * FROM Player", connection)
        df_player_attributes = pd.read_sql_query("SELECT * FROM Player_Attributes", connection)
        df_team = pd.read_sql_query("SELECT * FROM Team", connection)
        df_team_attributes = pd.read_sql_query("SELECT * FROM Team_Attributes", connection)
        df_country = pd.read_sql_query("SELECT * FROM Country", connection)
        df_match = pd.read_sql_query("SELECT * FROM Match", connection)
        df_league = pd.read_sql_query("SELECT * FROM League", connection)

        # Preparacion del df_player_latest___________________________

        # Estandarizamos y limpiamos la columnnas de los dataframes df_player y df_player_attributes
        df_player_attributes = _clean_df_column_names(df_player_attributes)
        df_player = _clean_df_column_names(df_player)

        # Estandarizamos las columnas que tiene fechas
        df_player_attributes["DATE"] = pd.to_datetime(df_player_attributes["DATE"], errors="coerce").dt.floor("s")
        df_player["BIRTHDAY"] = pd.to_datetime(df_player["BIRTHDAY"], errors="coerce").dt.floor("s")

        # Convertimos los pesos de libras a kilogramos en df_player
        df_player["WEIGHT"] = (df_player["WEIGHT"] * 0.453592).round(0).astype(int)

        # Filtramos para quedarnos con los registros mas actuales de cada jugador en df_player_attributes
        df_player_attributes_latest = df_player_attributes.copy()
        df_player_attributes_latest = df_player_attributes_latest.sort_values(["PLAYER_API_ID", "DATE", "ID"]).copy()
        df_player_attributes_latest = df_player_attributes_latest.drop_duplicates(subset="PLAYER_API_ID", keep="last").reset_index(drop=True)

        # Ahora hacemos el left join entre Player y Player_Attribute (los dataframes) asi obtniendo toda la info de los jugadores en un mismo dataframe.
        df_player_latest = df_player.merge(df_player_attributes_latest, on="PLAYER_API_ID", how="left", suffixes=("_PLAYER", "_ATTR"))

        # Calculamos el promedio de los atributos relacionados a ser portero
        gk_columns = ["GK_DIVING", "GK_HANDLING", "GK_KICKING", "GK_POSITIONING", "GK_REFLEXES"]
        df_player_latest["GK_MEAN"] = df_player_latest[gk_columns].mean(axis=1)

        # Calculamos la mitad del promedio maximo para que funcione como threshold para determinar si un jugador es portero
        # Tambien esta la opcion de obtener este dato del dataframe match (probablemente lo ideal), pero se me complico. Este approach me parecio adecuado como sustitucion.
        threshold_gk_value = round(df_player_latest["GK_MEAN"].max() / 2, 0).astype(int)

        # Definimos dos nuevas columnas is_goalkeeper y player type.
        df_player_latest["IS_GOALKEEPER"] = df_player_latest["GK_MEAN"] >= threshold_gk_value
        df_player_latest["PLAYER_TYPE"] = np.where(df_player_latest["IS_GOALKEEPER"], "GOALKEEPER", "OUTFIELD")

        # Agregamos la columna de edad de los jugadores
        df_player_latest["AGE"] = (df_player_latest["DATE"] - df_player_latest["BIRTHDAY"]).dt.days / 365.25

        # Ahora definimos una copia donde resolveremos la presencia de nan
        df_player_latest_imputed = df_player_latest.copy()

        # Eliminamos filas sin overall o potential (son demasiado importantes)
        df_player_latest_imputed = (df_player_latest_imputed.dropna(subset=["OVERALL_RATING", "POTENTIAL", "AGE"]).reset_index(drop=True))

        # Definimos las columnas categoricas a imputar
        categorical_columns = ["PREFERRED_FOOT", "ATTACKING_WORK_RATE", "DEFENSIVE_WORK_RATE"]

        # Imputamos columnas categoricas con la moda por tipo de jugador
        df_player_latest_imputed = _impute_categorical_nan_with_mode(df_player_latest_imputed, categorical_columns, "PLAYER_TYPE")

        # Definimos las columnas numericas donde no debemos imputar nan
        numerical_columns_to_exclude = {
            "ID_PLAYER",
            "ID_ATTR",
            "PLAYER_API_ID",
            "PLAYER_FIFA_API_ID_PLAYER",
            "PLAYER_FIFA_API_ID_ATTR",
            "GK_MEAN",
            "IS_GOALKEEPER",
        }

        # Definimos las columnas numericas donde si debemos imputar nan
        numerical_columns_with_na = [col for col in df_player_latest_imputed.columns if df_player_latest_imputed[col].isna().any() and isinstance(df_player_latest_imputed[col].iloc[0], (int, float)) and col not in numerical_columns_to_exclude]

        # Imputamos columnas numericas con la mediana por tipo de jugador
        df_player_latest_imputed = _impute_numeric_nan_with_median(df_player_latest_imputed, numerical_columns_with_na, "PLAYER_TYPE")

        # Preparacion del df_team_match_____________________

        # Estandarizamos y limpiamos las columnas de los dataframes que vamos a usar
        df_match = _clean_df_column_names(df_match)
        df_team = _clean_df_column_names(df_team)
        df_league = _clean_df_column_names(df_league)
        df_country = _clean_df_column_names(df_country)

        # Estandarizamos la columna "date" del df_match
        df_match["DATE"] = pd.to_datetime(df_match["DATE"], errors="coerce").dt.floor("s")

        # Creamos copias de los dataframes no principales (i.e. no df_match) y modificamos acordemente para hacer los joins mas claros con paises, ligas y equipos
        df_league_temp = df_league[["ID", "NAME"]].copy()
        df_league_temp = df_league_temp.rename(columns={"ID": "LEAGUE_ID", "NAME": "LEAGUE_NAME"})

        df_country_temp = df_country[["ID", "NAME"]].copy()
        df_country_temp = df_country_temp.rename(columns={"ID": "COUNTRY_ID", "NAME": "COUNTRY_NAME"})

        df_home_team_temp = df_team[["TEAM_API_ID", "TEAM_FIFA_API_ID", "TEAM_LONG_NAME", "TEAM_SHORT_NAME"]].copy()
        df_home_team_temp = df_home_team_temp.rename(columns={"TEAM_API_ID": "HOME_TEAM_API_ID", "TEAM_FIFA_API_ID": "HOME_TEAM_FIFA_API_ID", "TEAM_LONG_NAME": "HOME_TEAM_LONG_NAME", "TEAM_SHORT_NAME": "HOME_TEAM_SHORT_NAME"})

        df_away_team_temp = df_team[["TEAM_API_ID", "TEAM_FIFA_API_ID", "TEAM_LONG_NAME", "TEAM_SHORT_NAME"]].copy()
        df_away_team_temp = df_away_team_temp.rename(columns={"TEAM_API_ID": "AWAY_TEAM_API_ID", "TEAM_FIFA_API_ID": "AWAY_TEAM_FIFA_API_ID", "TEAM_LONG_NAME": "AWAY_TEAM_LONG_NAME", "TEAM_SHORT_NAME": "AWAY_TEAM_SHORT_NAME"})

        # Creamos una copia de df_match y agregamos nombres de liga, pais, equipo local y equipo visitante
        df_match_v2 = df_match.copy()

        df_match_v2 = df_match_v2.merge(df_league_temp, on="LEAGUE_ID", how="left")
        df_match_v2 = df_match_v2.merge(df_country_temp, on="COUNTRY_ID", how="left")
        df_match_v2 = df_match_v2.merge(df_home_team_temp, on="HOME_TEAM_API_ID", how="left")
        df_match_v2 = df_match_v2.merge(df_away_team_temp, on="AWAY_TEAM_API_ID", how="left")

        # Ahora usamos las tres helper functions definidas para obtener la formacion del equipo local y visitante para cada partido (que no tenga datos nulos en los campos relavantes)

        # Usando la funcion infer_formation_row, usando las coordenadas Y, que indican las lineas tacticas del equipo, inferimos la formacion de equipo por partido
        df_match_v2["HOME_FORMATION"] = df_match_v2.apply(_infer_formation_from_row, axis=1, prefix="HOME")
        df_match_v2["AWAY_FORMATION"] = df_match_v2.apply(_infer_formation_from_row, axis=1, prefix="AWAY")

        # Construimos el dataframe para el lado local del partido
        df_team_match_home = _build_team_match_side(df_match_v2, "HOME")

        # Construimos el dataframe para el lado visitante del partido
        df_team_match_away = _build_team_match_side(df_match_v2, "AWAY")

        # Concatenamos ambos para obtener el dataframe final
        df_team_match = pd.concat([df_team_match_home, df_team_match_away], axis=0).reset_index(drop=True)

        # Ordenamos el dataframe para que sea mas legible (ordenamos por equipo, por fecha y por contrincante)
        df_team_match = df_team_match.sort_values(["TEAM_API_ID", "DATE", "MATCH_API_ID"]).reset_index(drop=True)

        # Reordenamos columnas para dejar primero las mas importantes
        df_team_match = df_team_match[
            [
                "MATCH_ID",
                "MATCH_API_ID",
                "DATE",
                "SEASON",
                "STAGE",
                "COUNTRY_ID",
                "COUNTRY_NAME",
                "LEAGUE_ID",
                "LEAGUE_NAME",
                "TEAM_API_ID",
                "TEAM_FIFA_API_ID",
                "TEAM_LONG_NAME",
                "TEAM_SHORT_NAME",
                "OPPONENT_API_ID",
                "OPPONENT_FIFA_API_ID",
                "OPPONENT_LONG_NAME",
                "OPPONENT_SHORT_NAME",
                "MATCH_SIDE",
                "IS_HOME",
                "FORMATION",
                "GOALS_FOR",
                "GOALS_AGAINST",
                "GOAL_DIFF",
                "ABS_GOAL_DIFF",
                "TOTAL_GOALS",
                "RESULT",
                "POINTS",
            ]
        ].copy()

        return df_player_latest, df_player_latest_imputed, df_team_match
    
    finally:
        connection.close()