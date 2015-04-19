import pandas as pd
import requests

# add api key
from key import api_key

# set up api call
base_url = "https://maps.googleapis.com/maps/api/place/radarsearch/json"

# set up parameters
param = {
    "key" : api_key,
    "location" : "38.907192,-77.036871",
    "radius" : 30000
}

# import search terms
stores = pd.read_csv("types.csv")

# Calls
def callAPI(param, df, base):
    
    res = dict()
    for index, row in df.iterrows():
        
        # add additional params
        param['type'] = row['type']
        param[row['cat']] = row['cat_value']
        
        res[row['id']] = requests.get(base, params = param)
        
    return(res)

# clean up data
def clean(results):
    
    for k in results.keys():
        places = pd.DataFrame(results[k].json()['results'])
        # clean up geometry
        places['lat'] = [x['location']['lat'] for x in places['geometry']]
        places['long'] =  [x['location']['long'] for x in places['geometry']]
        

             
             