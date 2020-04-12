from typing import List, Dict, NewType
import numpy
from social import Location, Person
import random
import itertools
import numpy as np
import neo4j_helper as nea

class City:

    def __init__(self, name, locations: List[Location], public_transport : Location, citizens: List[List[Person]]):
        self.name = name
        self.locations = locations
        self.public_transport= public_transport
        all_city = []
        [all_city.append(p) for pg in citizens for p in pg]
        self.citizens = all_city
        self.helper = nea.GDBModelHelper("bolt://localhost:7687/neo4j","db_connect","Pr3M0rt3m")

    def pulse(self, day_or_nigth):
        for l in self.locations:
            l.commute_decision(day_or_nigth)

    def public_commute(self, timeevent):
        for p in self.citizens:
            if (p.going_to_metro()):
                self.public_transport.add_person(p)
        
        self.public_transport.dance(timeevent)
        self.public_transport.clear()

    def commute_and_act(self, timeevent):

        for p in self.citizens:
            if(p.next_type_location != p.current_type_location):
                current_location = p.my_spots[p.current_type_location]
                next_location = p.my_spots[p.next_type_location]
                current_location.remove_person(p)
                next_location.add_person(p)
                p.current_type_location = p.next_type_location

        for l in self.locations:
            l.dance(timeevent)

    def reset_contacts(self):
        # write contact to DB
        a=0
        self.helper.register_meeting(self.citizens)
        for p in self.citizens:
            a+=len(p.contacts)
            p.contacts = []
        print(">",str(a))
    def initial_infect(self, proportion):

        if (type(proportion)==int):
            persons_to_infect = random.sample(self.citizens, proportion)
        else:
            persons_to_infect = random.sample(self.citizens, int(len(self.citizens)*proportion))
        
        for infected in persons_to_infect:
            infected.status = 'i'
            infected.update_vector('','d0_h0')
    
        susceptibles = list(set(self.citizens) - set(persons_to_infect))
        print("person infected:", [p.name for p in persons_to_infect])

        self.citizens = susceptibles + persons_to_infect

    def count_infected(self):
        names = [p.name for p in self.citizens if p.status=='i'][0:10]
        print(names)
        counts = list(map(lambda p: p.status == 'i', self.citizens))
        return(np.sum(counts))
    
    def count_removed(self):
        counts = list(map(lambda p: p.status == 'r', self.citizens))
        return(np.sum(counts))
    
    def count_suceptible(self):
        counts = list(map(lambda p: p.status == 's', self.citizens))
        return(np.sum(counts))
    
    def return_citizens(self):
        return(self.citizens.copy())

    def sir_population_count(self):
        return int(self.count_suceptible()), int(self.count_infected()),int(self.count_removed()) 

            

