import json
import random
from social import Location, Person, Stereotype
from numpy.random import choice
import uuid

class CityBuilder:
    def __init__(self, city_file: str = 'config/city_init.json', 
        stereo_file = 'config/stereotypes.json'):
        # city initialization file    
        with open(city_file) as json_file:
            init_file = json.load(json_file)

         # load strereo types    
        with open(stereo_file) as json_file:
            stereos = json.load(json_file)

        self.city_distribution = init_file
        self.stereos = stereos
        
    def create_locations(self):
        number_of_locations = self.city_distribution['total_locations']
        location_types = self.city_distribution['locations']
        loc_dict = {}
        for key in location_types['location_proportion'].keys():
            loc_dict[key] = []

        for l in range(number_of_locations):

            type_location = self.get_label(location_types['location_proportion'])
            l_temp = loc_dict[type_location]
            density_type =  self.get_label(location_types['type_location_proportion'][type_location])
            custom_loc = Location(str(uuid.uuid4()),location_type=type_location, 
                pro_contact=location_types['contact_prob'][type_location], location_density=density_type)
            l_temp.append(custom_loc)
            loc_dict[type_location]=l_temp

        self.locations_city = loc_dict

    def populate(self):
        number_of_citizens = self.city_distribution['suceptibles']
        citizen_types = self.city_distribution['people']['people_proportion']
        stereotypes = self.city_distribution['people']['people_stereotypes']
        citizens_dict = {}
        stereo_dict = {}
        for key in citizen_types.keys():
            citizens_dict[key] = []
            stereo_value  = stereotypes[key]
            stereo_dict[key] = Stereotype(key, day_transition_matrix=self.stereos[stereo_value['d']], 
                night_transition_matrix=self.stereos[stereo_value['n']], 
                public_transport=stereo_value['public_transport'])
        
        for c in range(number_of_citizens):
            citizen_type = self.get_label(citizen_types)
            l_temp = citizens_dict[citizen_type]
            custom_citizen = Person(f'mac-{str(uuid.uuid4())}', 
                stereotype=stereo_dict[citizen_type])
            l_temp.append(custom_citizen)
            citizens_dict[citizen_type]=l_temp
        
        self.citizens = citizens_dict

    def load_city(self):
        for person_type, persons in self.citizens.items():
            for person in persons:
                custom_my_spots = {}
                for location_type, list_of_locations in self.locations_city.items():
                    density_type = self.get_label(self.city_distribution['locations']['population_spatial_distribution'])
                    custom_my_spots[location_type] = self.get_location_by_density(density_type, list_of_locations)
            
                person.update_myspots(custom_my_spots)

        return (None)


    def get_location_by_density(self, density_type: str, list_of_locations):
        """
        returns a specific location of list_of_locations with the same density type = density_type

        """
        filter_list_of_locations = [l for l in list_of_locations if l.location_density==density_type]
        location_selected = choice(filter_list_of_locations)
        return (location_selected)

    
    def get_label(self, labels_with_weigths):
        return (choice(list(labels_with_weigths.keys()), p = list(labels_with_weigths.values())))



    