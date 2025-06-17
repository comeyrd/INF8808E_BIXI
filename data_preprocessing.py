import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import json

def load_and_process_for_page1():
    df = pd.read_csv('./data/station_information.csv')
    map_df = df[['station_id', 'name', 'lat', 'lon']].copy()
    map_df["station_id_s"] = map_df['station_id'].astype(str)

    # Données hebdomadaires
    line_chart_df = pd.read_csv('./data/bixi_comptage_week_2024.csv')
    line_chart_df['week_date'] = pd.to_datetime(line_chart_df['week'], unit='ms')
    line_chart_df["station_id_s"] = line_chart_df['station_id'].astype(str)
    line_chart_df = line_chart_df.sort_values('week_date')

    # Données journalières
    day_df = pd.read_csv('./data/bixi_comptage_day_2024.csv')
    day_df['day_date'] = pd.to_datetime(day_df['day'], unit='ms')
    day_df["station_id_s"] = day_df['station_id'].astype(str)
    day_df = day_df.sort_values('day_date')

    annual_df = (
        line_chart_df.groupby('station_id', as_index=False)['nb_passages']
        .sum()
    )
    
    # Ajouter colonne mois
    day_df['month'] = day_df['day_date'].dt.month

    # Somme des passages par station et par mois
    monthly_df = (
        day_df.groupby(['station_id', 'month'], as_index=False)['nb_passages']
        .sum()
    )

    return map_df, line_chart_df, day_df, annual_df, monthly_df




def load_and_process_for_page2():
    stations = pd.read_csv("./data/station_information.csv")  
    comptage = pd.read_csv("./data/bixi_comptage_week_2024.csv")

    # Fusionner les données de comptage avec les arrondisements
    comptage_avec_arrondissement = comptage.merge(
        stations[["station_id", "arrondissement"]], on="station_id", how="left"
    )

    # Vérifier qu’il n’y a pas de station sans quartier
    if comptage_avec_arrondissement["arrondissement"].isnull().any():
        print("⚠️ Certaines stations n'ont pas d'arrondissement associé.")

    # Somme des passages par arrondissement
    passages_par_arrondissement = comptage_avec_arrondissement.groupby("arrondissement")["nb_passages"].sum().reset_index()

    # Trier par nombre de passages décroissant
    passages_par_arrondissement = passages_par_arrondissement.sort_values(by="nb_passages", ascending=False)

    # Réindexer par ordre alphabétique des arrondissements
    passages_par_arrondissement = passages_par_arrondissement.sort_values(by="arrondissement").reset_index(drop=True)


    # Calculer le nombre de stations par arrondissement
    stations_par_arrondissement = stations.groupby("arrondissement")["station_id"].nunique().reset_index()
    stations_par_arrondissement = stations_par_arrondissement.rename(columns={"station_id": "nb_stations"})

    # Fusion avec le DataFrame des passages
    df_district = passages_par_arrondissement.merge(stations_par_arrondissement, on="arrondissement", how="left")

    # Réorganiser les colonnes si besoin
    df_district = df_district[["arrondissement", "nb_passages", "nb_stations"]]

    # Lire le fichier brut
    with open("./data/reseau_cyclable.json", "r", encoding="utf-8") as f:
        df_json = json.load(f)

    # Normaliser uniquement les features -> une ligne par élément
    df_reseau = pd.json_normalize(df_json["features"])

    # Extraire les propriétés uniquement
    df_reseau = df_reseau.filter(like="properties.")

    # Supprimer le préfixe "properties." dans les noms de colonnes
    df_reseau.columns = df_reseau.columns.str.replace("properties.", "", regex=False)

    # Nettoyage des colonnes nécessaires
    df_reseau = df_reseau.dropna(subset=["NOM_ARR_VILLE_DESC", "LONGUEUR"])
    df_reseau["LONGUEUR_KM"] = df_reseau["LONGUEUR"] / 1000

    # Normaliser les tirets dans les noms d'arrondissements
    df_reseau["NOM_ARR_VILLE_DESC"] = df_reseau["NOM_ARR_VILLE_DESC"].str.replace("–", "-", regex=False)
    df_reseau["NOM_ARR_VILLE_DESC"] = df_reseau["NOM_ARR_VILLE_DESC"].str.replace("—", "-", regex=False)

    # Longueur totale par arrondissement
    longueur_totale = df_reseau.groupby("NOM_ARR_VILLE_DESC", as_index=False)["LONGUEUR_KM"].sum()
    longueur_totale = longueur_totale.rename(columns={"LONGUEUR_KM": "longueur_km"})

    # Longueur protégée par arrondissement
    df_protegee = df_reseau[df_reseau["PROTEGE_4S"] == "Oui"]
    longueur_protegee = df_protegee.groupby("NOM_ARR_VILLE_DESC", as_index=False)["LONGUEUR_KM"].sum()
    longueur_protegee = longueur_protegee.rename(columns={"LONGUEUR_KM": "longueur_protegee_km"})

    # Fusion des deux longueurs
    df_resultats = pd.merge(longueur_totale, longueur_protegee, on="NOM_ARR_VILLE_DESC", how="left")
    df_resultats["longueur_protegee_km"] = df_resultats["longueur_protegee_km"].fillna(0)

    # Renommer la colonne après la fusion
    df_resultats = df_resultats.rename(columns={"NOM_ARR_VILLE_DESC": "arrondissement"})

    # Dictionnaire de renommage : {ancien_nom: nouveau_nom}
    renommage_arrondissements = {
        "Côte-des-Neiges-Notre-Dame-de-Grâce": "Côte-des-Neiges - Notre-Dame-de-Grâce",
        "Mercier-Hochelaga-Maisonneuve": "Mercier - Hochelaga-Maisonneuve",
        "Rivière-des-Prairies-Pointe-aux-Trembles": "Rivière-des-Prairies - Pointe-aux-Trembles",
        "Rosemont-La Petite-Patrie": "Rosemont - La Petite-Patrie",
        "Villeray-Saint-Michel-Parc-Extension" : "Villeray—Saint-Michel—Parc-Extension"

    }

    # Appliquer le renommage sur la colonne "arrondissement"
    df_resultats["arrondissement"] = df_resultats["arrondissement"].replace(renommage_arrondissements)

    # Fusion des deux DataFrames sur 'arrondissement'
    df_merged = pd.merge(df_resultats, df_district, on="arrondissement", how="outer")

    # Remplacer les valeurs manquantes par 0
    df_merged = df_merged.fillna(0)


    # Lire le fichier avec point-virgule comme séparateur
    df_superficies = pd.read_csv("./data/superficies.csv", sep=";")

    # Merge avec df_merged sur la colonne 'arrondissement'
    df_merged = df_merged.merge(df_superficies, on="arrondissement", how="left")

    # Vérifier si des arrondissements n’ont pas été associés correctement
    if df_merged["superficie"].isnull().any():
        print("⚠️ Certaines lignes n'ont pas de superficie associée.")


    # Création des colonnes de densité
    df_merged["densite_piste_km_par_km2"] = df_merged["longueur_km"] / df_merged["superficie"]
    df_merged["densite_piste_protegee_km_par_km2"] = df_merged["longueur_protegee_km"] / df_merged["superficie"]
    df_merged["densite_station_par_km2"] = df_merged["nb_stations"] / df_merged["superficie"]

    df_merged["volume_par_km"] = df_merged.apply(
    lambda row: row["nb_passages"] / row["longueur_km"] if row["longueur_km"] > 0 else 0,
    axis=1)

    arrondissements_exclus = ["Longueuil", "Laval", "Boucherville"]

    df_filtered = df_merged[
    (df_merged["nb_stations"] != 0) &
    (~df_merged["arrondissement"].isin(arrondissements_exclus))
]

    return df_filtered






def load_and_process_for_page3():

    df_bixi_week_nbr = pd.read_csv("./data/bixi_comptage_week_2024.csv")
    df_bixi_week_nbr['week'] = pd.to_datetime(df_bixi_week_nbr['week'], unit='ms')
    df_bixi_week_nbr['year'] = df_bixi_week_nbr['week'].dt.year
    df_bixi_week_nbr['month'] = df_bixi_week_nbr['week'].dt.strftime('%b')
    df_bixi_week_nbr.loc[df_bixi_week_nbr['year'] == 2023, 'month'] = 'Jan'
    df_bixi_week_nbr['week'] = df_bixi_week_nbr['week'].dt.isocalendar().week
    df_bixi_week_nbr.loc[df_bixi_week_nbr['year'] == 2023, 'week'] = 0

    df_bixi_week_nbr = df_bixi_week_nbr[['station_id', 'nb_passages', 'week']]

    df_bixi_index = pd.read_csv("./data/station_information.csv")
    df_bixi_index.rename(columns={"id": "station_id", "long": "lon"}, inplace=True)
    df_bixi_index = df_bixi_index[["station_id", "name", "lat", "lon"]]

    df_full_data = pd.merge(df_bixi_week_nbr, df_bixi_index, how="left", on="station_id")
    geometry = [Point(xy) for xy in zip(df_full_data['lon'], df_full_data['lat'])]
    gdf = gpd.GeoDataFrame(df_full_data, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)
    gdf = gdf.sort_values(by="week", ascending=True)


    jours_fr_abbr = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    jours_fr = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
    mois_fr = ["Jan", "Fév", "Mar", "Avr", "Mai", "Juin", "Juil", "Aoû", "Sep", "Oct", "Nov", "Déc"]

    df = pd.read_csv("data/bixi_comptage_day_2024.csv")

    df["Date"] = pd.to_datetime(df["day"], unit='ms')
    df_day = df.groupby("Date")["station_id"].sum().reset_index(name="nb_passages")

    # Supprimer les dates hors 2024
    df_day = df_day[df_day["Date"].dt.year == 2024].copy()

    # Ajouter les infos temporelles
    df_day["WeekIndex"] = df_day["Date"].dt.isocalendar().week
    df_day["Jour"] = df_day["Date"].dt.weekday
    df_day["JourNum"] = df_day["Date"].dt.day
    df_day["Mois"] = df_day["Date"].dt.month

    # ⚠️ Corriger les jours de fin décembre ayant WeekIndex=1 → on force à 53
    mask_end_dec = (df_day["Mois"] == 12) & (df_day["JourNum"] >= 30)
    df_day.loc[mask_end_dec, "WeekIndex"] = 53

    # Ajouter noms français
    df_day["MoisStr"] = df_day["Mois"].apply(lambda x: mois_fr[x - 1])
    df_day["JourStr"] = df_day["Jour"].apply(lambda x: jours_fr_abbr[x])
    df_day["x_label"] = df_day.apply(
        lambda row: f"{row['JourStr']} {row['JourNum']} {row['MoisStr']}", axis=1
    )

    # Liste ordonnée des jours de la semaine (0=Lun, 6=Dim)
    jours_fr_ordered = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
    # S'assurer que 'JourStr' est une catégorie ordonnée
    df_day["JourStr"] = pd.Categorical(df_day["JourStr"], categories=jours_fr_ordered, ordered=True)

    heatmap_data = df_day.pivot_table(
        index="JourStr",
        columns="WeekIndex",
        values="nb_passages",
        aggfunc="sum",
        fill_value=0,
        observed=False
    )
    
    mois_matrix = df_day.pivot_table(
        index="JourStr",
        columns="WeekIndex",
        values="Mois",
        aggfunc=lambda x: x.mode().iloc[0] if not x.mode().empty else None,
        observed=False
    )

    
    ## Trouver les x_labels où le mois change
    #df_day_sorted = df_day.sort_values("Date")
    #month_change_labels = df_day_sorted[df_day_sorted["Mois"].diff().fillna(0) != 0]["x_label"].tolist()
#
    ## Indices des colonnes dans la heatmap
    #mois_separateurs = [heatmap_data.columns.get_loc(label) - 0.5 for label in month_change_labels if label in heatmap_data.columns]

    # Construction des séparateurs de mois (index des changements de mois)
    mois_separateurs = df_day.drop_duplicates("Mois", keep="first")["WeekIndex"].tolist()

    return gdf, df_day, heatmap_data, mois_matrix