from typing import List, Dict
import numpy
from maths_models import MarkovChain
from social import Contact

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

    def __init__(self, name, stereotype: Stereotype, status = 's' ):
        self.name   = name
        self.status  = status
        self.occupation  =  ''
        self.contacts : List[Contact] = []
        self.vector = ''
        self.stereotype : Stereotype = stereotype
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
    
    def commute(self, location_type, day_or_nigth):
         next_destin = self.stereotype.sstay_or_sgo(location_type, day_or_nigth)
         self.my_spots[next_destin]
         return(self.my_spots[next_destin])


class Location(object):
    
    def __init__(self, location_name, location_type):
        self.location_name = location_name
        self.location_type = location_type
        self.population = None
    
    def update_population(self, new_population : List[Person]):
        self.population = new_population

    def commute_decision(self, day_or_nigth):

        if (len(self.population)<=0):
            print("the zone is empty!!")
        else:
            for p in self.population:
                destino = p.stereotype.sstay_or_sgo(self.location_type, day_or_nigth)

    def dance(self):
        pass # meets should be called!


