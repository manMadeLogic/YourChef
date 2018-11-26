import googlemaps
import os
gmap_key = os.environ.get('gmap_key')

class MapHelper:
    def __init__(self):
        self.gmaps = googlemaps.Client(key=gmap_key)
    def get_restuarant_info(self, restuarant_name,latitude, longitude):
        nearby_result =  self.gmaps.find_place(input=restuarant_name,input_type='textquery',
                                               fields=['formatted_address','name','opening_hours'],
                                               location_bias=
                                               'point:'+str(latitude)+','+str(longitude),
                                               language='en')
        print('point:'+str(latitude)+','+str(longitude))
        print(nearby_result)
        if(nearby_result['status']!="OK"):
            return "Zero Result"
        return nearby_result['candidates']

