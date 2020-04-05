
import random
import toolbox
import properties

def infection (person, person_contact, current_time: str):
    incubation_time = properties.INCUBATION_TIME
    infection_base_prob = properties.INFECTION_BASE_PROB
    if (person.status == 'r') or (person_contact.status == 'r') or (person.status == person_contact.status) or (person.status == 'i'):
        return True
    incubation_precond = (person_contact.status == 'i') and (person_contact.vector[0] != "")
    if incubation_precond:
        partner_infection_date = person_contact.vector[1]
        day_infected, hour_infected = toolbox.get_day_hour(partner_infection_date)
        current_day, current_hour = toolbox.get_day_hour(current_time)
        if ((current_day-day_infected) >= incubation_time) and (current_hour >= hour_infected):
            infection_prob = infection_base_prob * person.bad_habits * person.social_distance
            coin = random.random()
            if coin < infection_prob:
                person.status = 'i'
                person.update_vector(person_contact.name, current_time) 
                print (f"sorry {person.name} you are new positive covid!")
                print(f"your vector is {person.vector}")
                       
    else:
        coin = random.random()
        infection_prob = infection_base_prob * person.bad_habits * person.social_distance
        coin = random.random()
        if coin < infection_prob:
            person.status = 'i'
            person.update_vector(person_contact.name, current_time)
            print (f"sorry {person.name} you are new positive covid!")
            print(f"your vector is {person.vector}")
    return True
            

def remove_population(people, current_time_event):
    for person in people:
        if person.status == 'i':
            person_infection_day, person_infection_hour = toolbox.get_day_hour(person.vector[1])
            current_day, current_hour = toolbox.get_day_hour(current_time_event)
            removing_condition = ((current_day - person_infection_day) > properties.REMOVING_TIME) and (current_hour >= person_infection_hour)
            if removing_condition:
                person.status = 'r'        



