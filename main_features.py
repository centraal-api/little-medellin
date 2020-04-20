import pandas as pd
import json
import virus
import seaborn as sns
import properties
import genesis
import time
import numpy as np
from neo4j_graph_models import GDBAlgHelper

if __name__ == "__main__":

    tic = time.time()
    cols = ['day', 'suceptible', 'infected', 'removed']
    results = pd.DataFrame(columns=cols, index=range(properties.SIMULATION_DAYS), dtype=int)
    person_features = pd.DataFrame()
    city_builder = genesis.CityBuilder()
    alg_helper = GDBAlgHelper(city_builder.helper._driver)

    little_medallo = city_builder.create_city()
    print("...starting virus propagation simulation...")
    for day in range(properties.SIMULATION_DAYS):
        ts_count = 0
        for d_o_n in range(2):
            if (d_o_n ==0):
                
                for ts in range(3):
                    timeevent = str(day) +  f'd{day}_h{ts_count}'
                    print(timeevent)
                    little_medallo.pulse(d_o_n)
                    little_medallo.public_commute(timeevent)                        
                    little_medallo.commute_and_act(timeevent)
                    ts_count += 1
                    little_medallo.reset_contacts()
                    virus.remove_population(little_medallo.citizens,timeevent)
                    
            else:
                for ts in range(2):
                    timeevent = f'd{day}_h{ts_count}'
                    print(timeevent)
                    little_medallo.pulse(d_o_n)
                    little_medallo.public_commute(timeevent)                        
                    little_medallo.commute_and_act(timeevent)
                    ts_count += 1
                    little_medallo.reset_contacts()
                    virus.remove_population(little_medallo.citizens,timeevent)
                    

        p_suceptible, p_infected, p_removed = little_medallo.sir_population_count() 
        results.loc[day].suceptible = p_suceptible
        results.loc[day].infected = p_infected
        results.loc[day].removed = p_removed
        print(f' the d{day} we have ' , p_suceptible, p_infected, p_removed, " suceptible, infected, removed")
        results.loc[day].day = day
        print("compute graph features")
        low_pro_mod = alg_helper.create_meets_community_graph('low-meets-graph', timeevent, 
            prop=alg_helper.person_features[2] , proximity='<=2')
        high_pro_mod = alg_helper.create_meets_community_graph('high-meets-graph', timeevent, 
            prop=alg_helper.person_features[3] , proximity='>2')
        commute_mod = alg_helper.create_se_mueve_community_graph('commute-graph', timeevent)
        features = alg_helper.get_persons_df()
        features['day'] = day
        features['low_pro_mod'] = low_pro_mod
        features['high_pro_mod'] = high_pro_mod
        features['commute_mod'] = commute_mod
        person_features = pd.concat([person_features, features], ignore_index = True)
        for c in ['high_promity', 'low_proximity', 'community_commute']:
            person_features[f'infected_in_{c}'] = (person_features.groupby([c])['status']
                .transform(lambda x: np.sum(x=='i')))
        
    toc = time.time()
    print("finish the simulation, total time(seconds): ", toc - tic)
    results['change_s'] = results['suceptible'] - results['suceptible'].shift()
    results['beta'] = -results['change_s']*2000/ results['suceptible']/results['infected']
    results['change_r'] = results['removed'] - results['removed'].shift()
    results['gamma'] = results['change_r']/ results['infected']
    results['R0'] = results['beta']/ results['gamma']
    results= results.replace([np.inf, -np.inf], np.nan)
    R0 = results['R0'].describe()
    print(R0)
    results.to_csv("results.csv", index = False)
    print("saving features")
    person_features.to_csv("features.csv", index = False)
    results = pd.melt(results,id_vars='day',value_vars=["suceptible","infected","removed"], var_name="status")
    #Ploting curve
    ax = sns.relplot(x='day',y='value',hue='status',data=results, kind="line", height=10,aspect=3)
    ax.savefig('SIR_curve.png')