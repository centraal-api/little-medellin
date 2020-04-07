import random
from typing import List
import itertools
from maths_models import MarkovChain
from typing import List, Dict
import virus


class Stereotype():

    def __init__(self, name, day_transition_matrix: Dict, night_transition_matrix: Dict, public_transport: bool):
        
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

class Person:

    def __init__(self, name, stereotype: Stereotype, my_spots = None,  status = 's' ):
        self.name   = name
        self.status  = status
        self.occupation  =  ''
        self.contacts : List[Contact] = []
        self.vector = ''
        self.stereotype : Stereotype = stereotype
        self.current_type_location = 'h'
        self.next_type_location = None
        self.my_spots = my_spots
        self.social_distance = 1.0
        self.bad_habits = 1.0

    def update_myspots(self, my_spots):
        self.my_spots = my_spots
            
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

class Contact:
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

class Location:
    
    def __init__(self, location_name, location_type, pro_contact = 0.05, location_density=None):
        self.location_name = location_name
        self.location_type = location_type
        self.location_density = location_density
        self.population = []
        self.pro_contact = pro_contact
    
    def update_population(self, new_population : List[List[Person]]):
        pop = []
        [pop.append(p) for pg in new_population for p in pg]
        self.population = pop

    def add_person(self, citizen : Person):
        self.population.append(citizen)

    def remove_person(self, citizen : Person):

        #print("removing from ", self.location_name)
        if len(self.population) == 0:
            print(citizen.name + " is not here!")
        else:
            #print("removig from ", self.location_name, "this ", citizen.name)
            self.population.remove(citizen)

    def commute_decision(self, day_or_nigth):

        if (len(self.population)<=0 ):
            print("the zone is empty!!")
        else:
            for p in self.population:
                p.decide_destination(self.location_type, day_or_nigth)

    def compute_possibles_infection(self, people_after_day : List [Person], time_event: str):

        for person in people_after_day:
            # if the person had conctacts, posible need of copy
            p_current_status = person.status
            if (len(person.contacts)>0):
                for contact in person.contacts:
                    virus.infection(person,contact.someone, time_event)
                    if person.status != p_current_status:
                        break

    def dance(self, timeevent):
        if(not(self.population is None) or len(self.population)>1):

            meets(self.population, self.pro_contact, contact_per_zone = 1, timeevent = timeevent)
            self.compute_possibles_infection(self.population, timeevent)
    
    def clear(self):
        self.population=[]


  
