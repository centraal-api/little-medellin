import random
from medellin import Person
from typing import List
import itertools



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