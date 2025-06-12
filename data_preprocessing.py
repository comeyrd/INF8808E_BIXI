import pandas as pd
def load_and_process_for_page1():
    df = pd.read_csv('./data/station_information.csv')
    map_df = df[['station_id', 'name', 'lat', 'lon']].copy()
    map_df["station_id_s"] = map_df['station_id'].astype(str)

    line_chart_df = pd.read_csv('./data/bixi_comptage_week_2024.csv')
    line_chart_df['week_date'] = pd.to_datetime(line_chart_df['week'], unit='ms')
    line_chart_df["station_id_s"] = line_chart_df['station_id'].astype(str)
    line_chart_df = line_chart_df.sort_values('week_date')
    return map_df,line_chart_df
