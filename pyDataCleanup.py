import pandas as pd
import numpy as np
import requests
import json
from config import gkey

#read in the large file
df =  pd.read_csv('./resources/data/Consumer_Airfare_Report__Table_1a_-_All_U.S._Airport_Pair_Markets.csv')

#filter the years and where the origin is AUS
df = df[(df['Year'] >= 2007) & (df['Year'] <= 2017) & (df['airport_1'] == 'AUS')]

#per the dataset documentation, the column passengers holds the value for passengers per day
#the data is provided on a per quarter basis
#so the real value of the number of passengers should be the multiplied by the number of days in a quarter, or by 91 days
df['passengers'] = df['passengers'] * 91

#save this condensed dataset
df.to_csv('./resources/data/AUS.csv', index=False)

#get the list of destination_airports to query for lat and lng
destination_airports = df['airport_2'].unique().tolist()

#get the lat and lng from google
coords = []
for i in range(len(destination_airports)):
    coord = {}
    coord['airport_2'] = destination_airports[i]
    
    # Build the endpoint URL
    target_url = (f'https://maps.googleapis.com/maps/api/geocode/json?address={destination_airports[i]}&key={gkey}')
    
    #get the json data
    geo_data = requests.get(target_url).json()
    
    #get the lat and the lng
    coord['lat']= geo_data["results"][0]["geometry"]["location"]["lat"]
    coord['lng'] = geo_data["results"][0]["geometry"]["location"]["lng"]    
    coords.append(coord)

#save this dataset to a csv
pd.DataFrame(coords).to_csv('./resources/data/destination_airports_lat_lng.csv', index=False)