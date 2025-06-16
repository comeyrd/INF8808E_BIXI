import data_preprocessing

page1_map_df, page1_line_df, page1_day_df, page1_annual_df = data_preprocessing.load_and_process_for_page1()
page3_viz2_gdf = data_preprocessing.load_and_process_for_page3()

try:
    df_page2_data = data_preprocessing.load_and_process_for_page2()
except Exception as e:
    print("Erreur dans load_and_process_for_page2 :", e)
    df_page2_data = {}
