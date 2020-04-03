from medellin import *
from social import *
from virus import *
import pandas as pd

if __name__ == "__main__":
    # generate the persons:
    population = 20
    persons : List[Person] = [Person(f'person_{i}', stereotype=None) for i in range(population)]
    persons = initial_infect(persons,1)
    days = 20
    time_unit_per_day = 2 # 0 = sun 1 = night
    day = 'd1'
    infection_pro = 0.5
    pro_contact = 0.05
    results = pd.DataFrame()
    cols = ['day', 'counts']
    results = pd.DataFrame(columns=cols, index=range(days))

    for day in range(days): 
        
        for tu in range(time_unit_per_day):

            timeevent = f'd{day}_h{tu}'
            meets(persons, 0.05, contact_per_zone = 1, timeevent = timeevent)
        
        compute_possibles_infection(persons, infection_pro)
        reset_contacts(persons)
        results.loc[day].counts = count_infected(persons)
        results.loc[day].day = f'd{day}'
    
    results.to_csv("results.csv", index = False)
        

