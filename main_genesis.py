import pandas as pd
import json
import virus
import seaborn as sns
import properties
import genesis
import time

if __name__ == "__main__":

    tic = time.time()
    cols = ['day', 'suceptible', 'infected', 'removed']
    results = pd.DataFrame(columns=cols, index=range(properties.SIMULATION_DAYS), dtype=int)
    city_builder = genesis.CityBuilder()
    little_medallo = city_builder.create_city()
    print("...starting virus propagation simulation...")
    for day in range(properties.SIMULATION_DAYS):
        ts_count = 0
        for d_o_n in range(2):
            if (d_o_n ==0):
                
                for ts in range(3):
                    timeevent = f'd{day}_h{ts_count}'
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
        
    toc = time.time()
    print("finish the simulation, total time(seconds): ", toc - tic)
    results.to_csv("results.csv", index = False)
    results = pd.melt(results,id_vars='day',value_vars=["suceptible","infected","removed"], var_name="status")
    #Ploting curve
    ax = sns.relplot(x='day',y='value',hue='status',data=results, kind="line", height=10,aspect=3)
    ax.savefig('SIR_curve.png')