import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

def load_and_process_for_page1():
    df = pd.read_csv('./data/station_information.csv')
    map_df = df[['station_id', 'name', 'lat', 'lon']].copy()
    map_df["station_id_s"] = map_df['station_id'].astype(str)

    line_chart_df = pd.read_csv('./data/bixi_comptage_week_2024.csv')
    line_chart_df['week_date'] = pd.to_datetime(line_chart_df['week'], unit='ms')
    line_chart_df["station_id_s"] = line_chart_df['station_id'].astype(str)
    line_chart_df = line_chart_df.sort_values('week_date')
    return map_df,line_chart_df

def load_and_process_for_page3():
    df_bixi_week_nbr = pd.read_csv("./data/bixi_comptage_week_2024.csv")
    df_bixi_week_nbr['week'] = pd.to_datetime(df_bixi_week_nbr['week'], unit='ms')
    df_bixi_week_nbr['year'] = df_bixi_week_nbr['week'].dt.year
    df_bixi_week_nbr['month'] = df_bixi_week_nbr['week'].dt.strftime('%b')
    df_bixi_week_nbr.loc[df_bixi_week_nbr['year'] == 2023, 'month'] = 'Jan'

    df_bixi_week_nbr['week'] = df_bixi_week_nbr['week'].dt.isocalendar().week

    df_bixi_week_nbr.loc[df_bixi_week_nbr['year'] == 2023, 'week'] = 0


    df_bixi_week_nbr = df_bixi_week_nbr[['station_id','nb_passages','week',]]

    df_bixi_index = pd.read_csv("./data/station_information.csv")
    df_bixi_index.rename(columns={"id":"station_id","long":"lon"},inplace=True)
    df_bixi_index = df_bixi_index[["station_id","lat","lon"]]
    df_full_data = pd.merge(df_bixi_week_nbr,df_bixi_index,how="left",on="station_id")
    geometry = [Point(xy) for xy in zip(df_full_data['lon'], df_full_data['lat'])]
    gdf = gpd.GeoDataFrame(df_full_data, geometry=geometry, crs="EPSG:4326")
    gdf = gdf.to_crs(epsg=3857)
    gdf = gdf.sort_values(by="week",ascending=True)
    return gdf