#########################################################################
##                                                                     ##
##   0. Imports                                                        ##
##                                                                     ##
#########################################################################

# 0.1 Import Flask, jsonify and render_template
from flask import Flask, jsonify, render_template, send_from_directory

# 0.2 Import our local functions to retrieve data from Wind API
from sw_api import get_wind_data, get_temp_data

# 0.3 Import SQLAlchemy and pandas and numpy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np

print("\n\n")
print("Server Dev Internal Debugging Prompts:\n")

#########################################################################
##                                                                     ##
##   1. Starting DB
##                                                                     ##
#########################################################################

db_path = "sqlite:///db/temp_wind.sql"

engine = create_engine(db_path)

#########################################################################
##                                                                     ##
##   2. Collect Data from SW API
##                                                                     ##
#########################################################################

# Collect temperature and wind data 

wind_df = get_wind_data()
print(f"Wind Speed collected for each and all cities: {len(wind_df)}")
wind_df.to_sql('Wind', con=engine, if_exists='replace', index=False)
print("\n============= Wind table ===================\n")
df = pd.read_sql("select * from Wind", con=engine)
df.to_csv('static/data/wind.csv', index=False)
wind_df1 = pd.read_csv("static/data/wind.csv")
print(wind_df1.head(2))
print("\n=============================================\n")

temp_df = get_temp_data()
print(f"Time Speed collected for each and all cities: {len(temp_df)}")
temp_df.to_sql('Temp', con=engine, if_exists='replace', index=False)
print("\n============= Temp table ====================\n")
df = pd.read_sql("select * from Wind", con=engine)
df.to_csv('static/data/temp.csv', index=False)
temp_df1 = pd.read_csv("static/data/wind.csv")
print(temp_df1.head(2))
print("\n=============================================\n")

#########################################################################
##                                                                     ##
##   3. Start Flask                                                   ##
##                                                                     ##
#########################################################################

# 3.1 Set app name as "app" and start Flask
app = Flask(__name__)

# # 3.2 Define what to do when a user hits the index route
@app.route("/")
# Return static HTML file with JS code
# Ideally would serve from independent web server, but not practical in test environment
def home():
    return render_template ("index.html")

# 3.3 Define route for the wind
@app.route("/wind")
def wind():
    return render_template ("wind.html")

# 3.4 Define route for the temperature
@app.route("/temperature")
def temperature():
    return render_template ("temp.html")

# 3.5 Define what to do when a user hits the /about route
@app.route("/about")
def about():
    print("Server received request for 'About' page...")
    return "Welcome to my 'About' page!"

# 3.6 Define what to do when a user hits the /about route
@app.route("/cityList")
def cityList():
    print("\n=========== city_list ========\n")
    
    df = pd.read_sql("select city from Wind", con=engine)
    
    city_list = df['City'].sort_values().unique()
    print(city_list)
    print("\n============================\n")
    
    city_list = list(np.ravel(city_list))
        
    return jsonify(city_list)

if __name__ == "__main__":
    app.run(debug=True)