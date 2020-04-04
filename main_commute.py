from medellin import *
from social import *
from virus import *
import pandas as pd
import json


if __name__ == "__main__":

    home = Location('home1', 'h')
    office = Location('office1', 'w')
    market = Location('store', 'n')
    transportation = Location('mini-metro', 't')

    # load strereo types    
    with open('config/stereotypes.json') as json_file:
        st = json.load(json_file)

    active_person = Stereotype('active_person', st['active_person_d'], 
        st['active_person_n'], public_transport = False)

    active_person_public = Stereotype('active_person_public', st['active_person_d'], 
        st['active_person_n'], public_transport = False)
    
    passive_person = Stereotype('passive_person', st['passive_person_d'], 
        st['passive_person_n'], public_transport = False)

    passive_person_res = Stereotype('passive_person', st['passive_person_res_d'], 
        st['passive_person_n'], public_transport = True)
    
    my_spots = {'h': home, 'w': office, 'n': market} # per zone in the next main

    workers = [Person(f'worker_{i}', stereotype=active_person,my_spots=my_spots) for i in range(1)]
    workers_public = [Person(f'p_worker_{i}', stereotype=active_person_public, my_spots=my_spots) for i in range(2)]
    homers = [Person(f'homers_{i}', stereotype=passive_person, my_spots=my_spots) for i in range(4)]
    dayers = [Person(f'dayers_{i}', stereotype=passive_person_res, my_spots=my_spots) for i in range(4)]
    simulation_days = 10
    infection_pro = 0.2

    cols = ['day', 'counts']
    results = pd.DataFrame(columns=cols, index=range(simulation_days))

    medayork = City('medayork', [home, office, market], public_transport=transportation, 
        citizens=[workers, workers_public, homers, dayers])

    home.update_population(medayork.citizens)

    for day in range(simulation_days):

        for d_o_n in range(2):
            for ts in range(3):
                timeevent = f'd{day}_h{ts}'
                medayork.pulse(d_o_n)
                medayork.public_commute(timeevent, infection_pro)                        
                medayork.commute_and_act(timeevent, infection_pro)

        
        results.loc[day].counts = count_infected(medayork.citizens)
        results.loc[day].day = f'd{day}'
        medayork.reset_contacts()

    print("finish the simulation")
    results.to_csv("results.csv", index = False)