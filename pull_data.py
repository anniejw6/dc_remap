import pandas as pd
import requests

# add api key
from key import api_key

# Calls
def callRadar(df, key, loc = '38.907192,-77.036871', rad = 30000):
    
    """Loop through Radar Search on a df of categories
    
    Input: 
        df should have the following columns:
            id: user-assigned category id
            type: type (per google's definitions)
            cat: custom api category
            cat_value: value of custom category
        
        key: api_key
        loc: lat-long of center
        rad: radius of search in meters
    
    Output: dictionary where key = id and value = request output
    """
    
    # set up api call
    base_url = "https://maps.googleapis.com/maps/api/place/radarsearch/json"
    
    res = dict()
    for index, row in df.iterrows():

        # set up parameters
        param = {
            "key" : key,
            "location" : loc,
            "radius" : rad,
            "type" : row['type'],
            row['cat'] : row['cat_value']
        }
        
        # call
        res[row['id']] = requests.get(base_url, params = param)
        
    return(res)

def cleanRadar(df):
    
    """ Turns radar output into dict of dataframes. 
    
    Input: object from callRadar
    
    Output:
        dict in which keys correspond to ids given to radar search
        each entry is a dataframe:
            place_id: google-assigned unique locator
            lat: latitude
            lng: longitude
            cat_id: category id (from radar search)
    """
    
    # loop through each category
    for k in df.keys():
        
        # turn json to df
        places = pd.DataFrame(df[k].json()['results'])
        
        # clean up geometry
        places['lat'] = [x['location']['lat'] for x in places['geometry']]
        places['lng'] =  [x['location']['lng'] for x in places['geometry']]
        
        # clean up dataframe
        places = places[['place_id', 'lat', 'lng']]
        places['cat_id'] = k
        
        df[k] = places
        
    return(df)
        

def callID(place_ids, key):
    """ Grab details for place_ids
    
    input: 
        place_ids: list of place_ids
        key: api_key
        
    output: dictionary where key = place_id and value = request output
    """
    
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    param = {"key" : key}
    
    res = dict()
    for pid in place_ids:
        
        # add pid
        param["placeid"] = pid
        
        res[pid] = requests.get(base_url, params = param)
    
    return(res)
    
def cleanID(df):
    """ Turns place_id output into nice dataframes 
    
    Input: callID output
    Output: dataframe
        place_id: google place id
        name: google's name of organization
        lat: latitude
        lng: longitude
        address: formatted address
        city: city
        state: state """
    
    for i in 
    
    df = df['result']
    # Name
    df['name']
    # Lat 
    df['geometry']['location']['lat']
    # Long
    df['geometry']['location']['lng']
    
    # address
    df['formatted_address']
    # city
    df['address_components'][2]['long_name']
    # state
    df['address_components'][3]['short_name']
    # PlaceID
    
if __name__ == "__main__":
    
    # import search terms
    stores = pd.read_csv("types.csv")
    
    # get placeids and clean
    res = callRadar(stores, api_key, 
                    loc = '38.907192,-77.036871', rad = 30000)
    res = cleanRadar(res)
    
    # get placeID
    places = callID(res['place_id'], api_key)
    
    
    
    
    
