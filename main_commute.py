from medellin import City
from social import Person, Stereotype, Location
import pandas as pd
import json
import virus
#import seaborn as sns


if __name__ == "__main__":

    home = Location('home1', 'h', 0.001)
    office = Location('office1', 'w')
    market = Location('store', 'n')
    transportation = Location('mini-metro', 't', 0.1)
    simulation_days = 30
    infection_pro = 0.3


    # load strereo types    
    with open('config/stereotypes.json') as json_file:
        st = json.load(json_file)

    active_person = Stereotype('active_person', st['active_person_d'], 
        st['active_person_n'], public_transport = False)

    active_person_public = Stereotype('active_person_public', st['active_person_d'], 
        st['active_person_n'], public_transport = True)
    
    passive_person = Stereotype('passive_person', st['passive_person_d'], 
        st['passive_person_n'], public_transport = False)

    passive_person_res = Stereotype('passive_person', st['passive_person_res_d'], 
        st['passive_person_n'], public_transport = True)
    
    my_spots = {'h': home, 'w': office, 'n': market} # per zone in the next main

    workers = [Person(f'worker_{i}', stereotype=active_person,my_spots=my_spots) for i in range(20)]
    workers_public = [Person(f'p_worker_{i}', stereotype=active_person_public, my_spots=my_spots) for i in range(30)]
    homers = [Person(f'homers_{i}', stereotype=passive_person, my_spots=my_spots) for i in range(100)]
    dayers = [Person(f'dayers_{i}', stereotype=passive_person_res, my_spots=my_spots) for i in range(50)]
    
    cols = ['day', 'suceptible', 'infected', 'removed']
    results = pd.DataFrame(columns=cols, index=range(simulation_days))

    medayork = City('medayork', [home, office, market], public_transport=transportation, 
        citizens=[workers, workers_public, homers, dayers])

    medayork.initial_infect(1)

    home.update_population([workers, workers_public, homers, dayers])


    for day in range(simulation_days):

        ts_count = 0

        for d_o_n in range(2):

            if (d_o_n ==0):
                
                for ts in range(3):
                    timeevent = f'd{day}_h{ts_count}'
                    print(timeevent)
                    medayork.pulse(d_o_n)
                    medayork.public_commute(timeevent, infection_pro)                        
                    medayork.commute_and_act(timeevent, infection_pro)
                    ts_count += 1
                    medayork.reset_contacts()
                    virus.remove_population(medayork.citizens,timeevent)
                    
            else:
                for ts in range(2):
                    timeevent = f'd{day}_h{ts_count}'
                    print(timeevent)
                    medayork.pulse(d_o_n)
                    medayork.public_commute(timeevent, infection_pro)                        
                    medayork.commute_and_act(timeevent, infection_pro)
                    ts_count += 1
                    medayork.reset_contacts()
                    virus.remove_population(medayork.citizens,timeevent)
                    

        p_suceptible, p_infected, p_removed = medayork.sir_population_count() 
        results.loc[day].suceptible = p_suceptible
        results.loc[day].infected = p_infected
        results.loc[day].removed = p_removed
        print(f' the d{day} we have ' , p_suceptible, p_infected, p_removed, " suceptible, infected, removed")
        results.loc[day].day = f'd{day}'

    print("finish the simulation")
    #TODO plot curve SIR model
    results.to_csv("results.csv", index = False)