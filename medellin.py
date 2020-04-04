from typing import List, Dict
import numpy
from maths_models import MarkovChain
#from social import meets ,reset_contacts
from virus import compute_possibles_infection
import random
import itertools


class Stereotype(object):

    def __init__(self, name, night_transition_matrix: Dict, day_transition_matrix: Dict, public_transport: bool):
        
        self.name = name
        self.night_transition_matrix : MarkovChain = MarkovChain(night_transition_matrix) 
        self.day_transition_matrix : MarkovChain  = MarkovChain(day_transition_matrix)  
        self.public_transport = public_transport
    
    def sstay_or_sgo(self, origin, day_or_nigth):
        
        if(day_or_nigth == 0):
            # day_transition_matrix
            destination = self.day_transition_matrix.next_state(origin)
        else :
            # night_transition_matrix
            destination = self.night_transition_matrix.next_state(origin)

        return(destination)

class Person(object):

    def __init__(self, name, stereotype: Stereotype, my_spots: Dict[(str, Location)],  status = 's' ):
        self.name   = name
        self.status  = status
        self.occupation  =  ''
        self.contacts : List[Contact] = []
        self.vector = ''
        self.stereotype : Stereotype = stereotype
        self.current_type_location = 'h'
        self.next_type_location = None
        self.my_spots : Dict[(str, Location)] = {}
    
    def meet(self, someone, timeevent):
        self.contacts.append(Contact(someone, timeevent))

    def showme_your_id(self):
        print(self.name, self.status)

    def list_my_contacts(self):
       for c in self.contacts:
          print(c.someone.name, c.someone.status)
        
    def contacts_infected(self):
        for c in self.contacts:
          if (c.someone.status == 'i'):
              print("take care you were in contact with:")
              print(c.someone.name)

    def update_vector(self, vector_name: str, timeevent):
        self.vector = (vector_name, timeevent)
    
    def decide_destination(self, location_type, day_or_nigth):
         self.next_type_location = self.stereotype.sstay_or_sgo(location_type, day_or_nigth)

    def going_to_metro(self):
        return (self.stereotype.public_transport and (self.current_type_location != self.next_type_location))

class Contact(object):
    def __init__(self, someone : Person, timeevent):
        self.someone = someone
        self.timeevent = timeevent

def meets(people_in_zone : List[Person], pro_contact_zone, contact_per_zone = 1, timeevent = ''):

    scenarios = itertools.combinations(people_in_zone, 2)

    for s in scenarios:
       for cn in range(contact_per_zone):
         if(random.random() < pro_contact_zone):
            s[0].meet(s[1], timeevent)
            s[1].meet(s[0], timeevent)


def reset_contacts(people: List[Person]):
    for p in people:
        p.contacts = []


class Location(object):
    
    def __init__(self, location_name, location_type):
        self.location_name = location_name
        self.location_type = location_type
        self.population = None
        self.pro_contact = 0.05
    
    def update_population(self, new_population : List[Person]):
        self.population = new_population

    def add_person(self, citizen : Person):
        self.population.append(citizen)

    def remove_person(self, citizen : Person):
        self.population.remove(citizen)

    def commute_decision(self, day_or_nigth):

        if (len(self.population)<=0):
            print("the zone is empty!!")
        else:
            for p in self.population:
                p.decide_destination(self.location_type, day_or_nigth)

    def dance(self, timeevent, infection_pro):
        if(self.population is None or len(self.population)<1):

            meets(self.population, self.pro_contact, contact_per_zone = 1, timeevent = timeevent)
            compute_possibles_infection(self.population, infection_pro)
    
    def clear(self):
        self.population=None

class City(object):

    def __init__(self, name, locations: List[Location], public_transport : Location, citizens: List[List[Person]]):
        self.name = name
        self.locations = locations
        self.public_transport= public_transport
        all_city = []
        [all_city.append(p) for pg in citizens for p in pg]
        self.citizens= all_city

    def pulse(self, day_or_nigth):
        for l in self.locations:
            l.commute_decision(day_or_nigth)

    def public_commute(self, timeevent, infection_pro):
        for p in self.citizens:
            if (p.going_to_metro):
                self.public_transport.add_person(p)
        
        self.public_transport.dance(timeevent, infection_pro)
        self.public_transport.clear()

    def commute_and_act(self, timeevent, infection_pro):

        for p in self.citizens:
            if(p.next_type_location != p.current_type_location):
                current_location = p.my_spots[p.current_type_location]
                next_location = p.my_spots[p.next_type_location]
                current_location.remove_person(p)
                next_location.add_person(p)

        for l in self.locations:
            l.dance(timeevent, infection_pro)

    def reset_contacts(self):
        # write contact to DB
        reset_contacts(self.citizens)

            

