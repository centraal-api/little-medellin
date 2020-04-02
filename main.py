from medellin import *
from social import *
from virus import *


if __name__ == "__main__":
    # generate the persons:
    population = 20
    persons : List[Person] = [Person(f'person_{i}') for i in range(population)]
    persons = initial_infect(persons,1)
    days = 20
    time_unit_per_day = 2 # 0 = sun 1 = night
    day = 'd1'
    infection_pro = 0.1
    pro_contact = 0.05

    for day in range(days):
        
        for tu in range(time_unit_per_day):

            timeevent = f'd{day}_h{tu}'
            meets(persons, 0.05, contact_per_zone = 1, timeevent = timeevent)
        
        compute_possibles_infection(persons, infection_pro)
        reset_contacts(persons)
