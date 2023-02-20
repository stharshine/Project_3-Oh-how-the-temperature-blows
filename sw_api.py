import requests
import json
from datetime import datetime
import csv 
import pandas as pd

def get_temp_data():

    lat = [51.50, 53.48, 53.41, 51.48, 55.95, 52.20, 51.75, 52.49, 52.40, 51.46, 55.86, 57.15, 50.82, 51.38, 54.91, 57.20, 51.52, 56.46, 53.57]
    lon = [-0.12, -2.24, -2.99, -3.18, -3.20, -0.12, -1.26, -1.90, -1.51, -2.59, -4.25, -2.10, -0.14, -2.36, -1.38, -2.29, -0.25, -2.97, -2.43]


    City=[
    "London",
    "Manchester",
    "Liverpool",
    "Cardiff",
    "Edimburgh",
    "Cambridge",
    "Oxford",
    "Birmingham",
    "Coventry",
    "Bristol",
    "Glasgow",
    "Aberdeen",
    "Brighton",
    "Bath",
    "Sunderland",
    "Blackburn",
    "Luton",
    "Dundee",
    "Bolton"]


    list_df=[]
    for i in range(len(lat)):

        data = {"lat": lat[i],
            "lon": lon[i],
            "model": "gfs",
            "parameters": ["temp"],
            "key": "4WZikmNBYvwrcB6jHJ6prLnhRaiAkT3G"
            }

        r = requests.post('https://api.windy.com/api/point-forecast/v2', json = data)
        result = json.loads(r.text)
        result.pop('warning')
        result.pop('units')
        length_output=len(result['ts'])
        city_list=[City[i]]*length_output
        city_dic={"city":city_list}
        city_dic.update(result)
    
        
        #print(result)
        list_df.append(pd.DataFrame(city_dic))


    temp_df = pd.concat(list_df)


    temp_df_clean = temp_df.rename(columns={"city": "City", "ts": "Timestamp", "temp-surface": "Temperature", "wind_u-surface": "Wind W-E", "wind_v-surface": "Wind E-W", "pressure-surface": "Pressure", "past3hprecip-surface": "Precipitation", "ptype-surface": "Type of Precipitation"})

    # Define a new column "Celsius"
    temp_df_clean["Celsius"] = 0.0
    print(temp_df_clean)


    temp_df_clean["Celsius"] = (temp_df_clean["Temperature"] - 273.15)


    # Remove column name 'Temperature'
    temp_df_final = temp_df_clean.drop(['Temperature'], axis=1)
    temp_df_final


    temp_df_final['Timestamp'] = pd.to_datetime(temp_df_clean['Timestamp'], unit='ms')
    print(temp_df_final)



    temp_df_clean.to_csv('./dataset/temp.csv', index=False)
    return temp_df_clean

def get_wind_data():

    lat = [51.50, 53.48, 53.41, 51.48, 55.95, 52.20, 51.75, 52.49, 52.40, 51.46, 55.86, 57.15, 50.82, 51.38, 54.91, 57.20, 51.52, 56.46, 53.57]
    lon = [-0.12, -2.24, -2.99, -3.18, -3.20, -0.12, -1.26, -1.90, -1.51, -2.59, -4.25, -2.10, -0.14, -2.36, -1.38, -2.29, -0.25, -2.97, -2.43]


    City=[
    "London",
    "Manchester",
    "Liverpool",
    "Cardiff",
    "Edimburgh",
    "Cambridge",
    "Oxford",
    "Birmingham",
    "Coventry",
    "Bristol",
    "Glasgow",
    "Aberdeen",
    "Brighton",
    "Bath",
    "Sunderland",
    "Blackburn",
    "Luton",
    "Dundee",
    "Bolton"]


    list_df=[]
    for i in range(len(lat)):

        data = {"lat": lat[i],
            "lon": lon[i],
            "model": "gfs",
            "parameters": ["wind", "pressure", "precip", "ptype"],
            "key": "4WZikmNBYvwrcB6jHJ6prLnhRaiAkT3G"
            }

        r = requests.post('https://api.windy.com/api/point-forecast/v2', json = data)
        result = json.loads(r.text)
        result.pop('warning')
        result.pop('units')
        length_output=len(result['ts'])
        city_list=[City[i]]*length_output
        city_dic={"city":city_list}
        city_dic.update(result)
    
        
        #print(result)
        list_df.append(pd.DataFrame(city_dic))


    wind_df = pd.concat(list_df)


    wind_df_clean = wind_df.rename(columns={"city": "City", "ts": "Timestamp", "temp-surface": "Temperature", "wind_u-surface": "Wind W-E", "wind_v-surface": "Wind E-W", "pressure-surface": "Pressure", "past3hprecip-surface": "Precipitation", "ptype-surface": "Type of Precipitation"})

    
    wind_df_clean['Timestamp'] = pd.to_datetime(wind_df_clean['Timestamp'], unit='ms')
    print(wind_df_clean)

    wind_df_clean.to_csv('./dataset/wind.csv', index=False)
    return wind_df_clean
