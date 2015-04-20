import pandas as pd
import requests

# add api key
from key import api_key

class GoogleRadarPlaces(object):
    
    """ Class to pull places based on radar searchs """
    
    def __init__(self, search_df, key,
                 center = '38.907192,-77.036871', 
                 rad = 30000):
        
        """ 
        Inputs: 
            search_df: dataframe
                    id: user-assigned category id
                    type: type (per google's definitions)
                    cat: custom api category
                    cat_value: value of custom category
            key: api key
            center: lat, long of center
            rad: how far search should extend (in meters)
        """
        
        self.search_df = search_df
        self.key = key
        self.center = center
        self.rad = rad
    
    def call_radar(self, key, loc, rad, typ, cat, cat_value):
        
        """ Individual radar search
        Input:
            key: api key
            loc: center locatin
            rad: center radius
            type: google catgory
            cat: custom category
            cat_value: custom category value
        Output: api return
        """
        
        base = "https://maps.googleapis.com/maps/api/place/radarsearch/json"
        
        param = {
            "key" : key,
            "location" : loc,
            "radius" : rad,
            "type" : typ,
            cat : cat_value
        }
        
        return(requests.get(base, params = param))

    def clean_radar(self, call_output):
        """ Turns radar output into dataframe
        
        Input: 
            call_output: output from _call_radar
        Output: 
            place_id: google-assigned unique locator
        """
        
        places = pd.DataFrame(call_output.json()['results'])
        return(places['place_id'])
    
    def call_places(self, place_id, key):
        """ Grab details for place_ids
        Input: 
            place_id: place_id
            key: api_key
        Output: API return
        """
        base = "https://maps.googleapis.com/maps/api/place/details/json"
        param = {"key" : key,
                 "placeid" : place_id}
        res = requests.get(base, params = param)
        return(res)
        
    def clean_places(self, places_out):
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
    
        df = places_out.json()['result']
        
        address = pd.DataFrame(df['address_components'])
        
        def _find_address(df):
            """ takes in address frame and returns city and state"""
            
            res = {'city' : None, 'state' : None}
            for index, row in df.iterrows():
                
                if 'locality' in row['types']:
                    res['city'] = row['short_name']
                elif 'administrative_area_level_2' in row['types']:
                    res['city'] = row['short_name']
                elif 'administrative_area_level_1' in row['types']:
                    res['state'] = row['short_name']
                    
            return(res)
            
        res = {'name' : df['name'],
        'lat' : df['geometry']['location']['lat'],
        'lng' : df['geometry']['location']['lng'],
        'address' : df['formatted_address']
        }
        
        res.update(_find_address(address))
        
        return(res)

        
    def run(self):
        
        """ Loop through search_df and grab Radar results
        
        Output: dict {search_cat id, dataframe of places}"""
        
        res_tot = dict()
        
        for index, row in self.search_df.iterrows():
            
            print(row['id'])
            # call radar search
            r_output = self.call_radar(key = self.key, loc = self.center,
                                       rad = self.rad,
                                       typ = row['type'], cat = row['cat'],
cat_value = row['cat_value'])

            # clean radar search
            r_output = self.clean_radar(r_output)
            
            # set up final list of places
            pid_res_tot = []
            
            for pid in r_output:
                
                # Search and clean individaul search
                pid_res = self.call_places(pid, self.key)
                pid_res = self.clean_places(pid_res)
                
                # add id
                pid_res['place_id'] = pid 
                
                # add to running list of places
                pid_res_tot.append(pid_res)
                
            # turn places to df
            pid_res_tot = pd.DataFrame(pid_res_tot)
            
            res_tot[row['id']] = pid_res_tot
            
        return(res_tot)
    
if __name__ == "__main__":
    
    # import search terms
    stores = pd.read_csv("types.csv")
    
    # get placeids and clean
    g_setup = GoogleRadarPlaces(stores, api_key, 
                              center = '38.907192,-77.036871',
                              rad = 30000)
    g_out = g_setup.run()
    
    for name in g_out.keys():
        g_out[name].to_csv('places_' + name + '.csv')
    