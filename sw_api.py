import pandas as pd

def get_temp_data():

    temp_df_clean = pd.read_csv("./dataset/temp.csv")
    return temp_df_clean

def get_wind_data():

    wind_df_clean = pd.read_csv("./dataset/wind.csv")
    return wind_df_clean
