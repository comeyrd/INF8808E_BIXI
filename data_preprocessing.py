import pandas as pd
def load_and_process_for_page1():
    df = pd.read_csv('./data/station_information.csv')
    map_df = df[['station_id', 'name', 'lat', 'lon']].copy()
    map_df["station_id_s"] = map_df['station_id'].astype(str)

    return map_df
