import json
import random
from social import Location
import uuid

class CityBuilder:
    def __init__(self, city_file: str = 'config/city_init.json'):
        # city initialization file    
        with open(city_file) as json_file:
            init_file = json.load(json_file)

        self.city_distribution = init_file
        
    def create_locations(self):
        number_of_locations = self.city_distribution['total_locations']
        location_types = self.city_distribution['locations']
        loc_dict = {}
        for key in location_types.keys():
            loc_dict[key] = []

        for l in range(number_of_locations):
            coin = random.random()
            if coin <= location_types['h']['proportion']:
                l_temp = loc_dict['h']
                home = Location(str(uuid.uuid4()),location_type='h', pro_contact=location_types['h']['contact_prob'])
                l_temp.append(home)
                loc_dict['h']=l_temp
            elif coin >= location_types['h']['proportion'] and coin <= (location_types['w']['proportion'] + location_types['h']['proportion']):
                l_temp = loc_dict['w']
                home = Location(str(uuid.uuid4()),location_type='w', pro_contact=location_types['w']['contact_prob'])
                l_temp.append(home)
                loc_dict['w']=l_temp
            else:
                l_temp = loc_dict['n']
                home = Location(str(uuid.uuid4()),location_type='n', pro_contact=location_types['n']['contact_prob'])
                l_temp.append(home)
                loc_dict['n']=l_temp
        self.locations_city = loc_dict





    