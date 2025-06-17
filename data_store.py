import data_preprocessing

page1_map_df, page1_line_df, page1_day_df, page1_annual_df, page1_month_df = data_preprocessing.load_and_process_for_page1()
page3_viz2_gdf,page3_viz1_df = data_preprocessing.load_and_process_for_page3()
df_page2_data = data_preprocessing.load_and_process_for_page2()
