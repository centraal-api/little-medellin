import random
from medellin import Person
from typing import List
import itertools
import numpy as np

def initial_infect(people: List[Person], proportion):

    if (type(proportion)==int):
        persons_to_infect = random.sample(people, proportion)
    else:
        persons_to_infect = random.sample(people, int(len(people)*proportion))
    
    for infected in persons_to_infect:
        infected.status = 'i'
  
    susceptibles = list(set(people) - set (persons_to_infect))
    print("person infected:", [p.name for p in persons_to_infect])

    return (susceptibles + persons_to_infect)


def compute_possibles_infection(people_after_day : List [Person], infection_pro: float):

    for person in people_after_day:
        # if the person had conctacts
        if (len(person.contacts)>0):
            for contact in person.contacts:
                someone = contact.someone
                coin = random.random()
                condition = (someone.status == 'i') and (coin < infection_pro) and (person.status != 'i') # ask for vector and check time
                if (condition): 
                    person.status = 'i'
                    person.update_vector(someone.name, contact.timeevent)
                    print (f"sorry {person.name} you are new positive covid!")
                    print(f"your vector is {person.vector}")
                    break

def count_infected(people : List [Person]):
    counts = list(map(lambda p: p.status == 'i', people))
    return(np.sum(counts))