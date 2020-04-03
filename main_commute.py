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
    
    workers = [Person(f'worker_{i}', stereotype=active_person) for i in range(1)]
    workers_public = [Person(f'p_worker_{i}', stereotype=active_person_public) for i in range(2)]
    homers = [Person(f'homers_{i}', stereotype=passive_person) for i in range(4)]
    dayers = [Person(f'dayers_{i}', stereotype=passive_person_res) for i in range(4)]

    simulation_days = 10
    all_city = []
    [all_city.append(p) for p in workers]
    [all_city.append(p) for p in workers_public]
    [all_city.append(p) for p in homers]
    [all_city.append(p) for p in dayers]

    home.update_population(all_city)

    for d in range(simulation_days):

        for d_o_n in range(2):

            if (d_o_n ==0):
                
                for ts in range(3):
                    

                    
                

            else:
                #night!




    