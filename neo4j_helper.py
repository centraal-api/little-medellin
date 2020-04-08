from neo4j import GraphDatabase
import social as s
from random import randint
import json as jso

class GDBModelHelper(object):
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
         
    def close(self):
        self._driver.close()

    def clear_db(self):
        with self._driver.session() as session:
            
            session.run(f"MATCH (n) OPTIONAL MATCH (n)-[r]-() DELETE n,r")

    def init_city(self, name):
        with self._driver.session() as session:
            session.run(f'CREATE (c:City) SET c.name="{name}"')
            #session.sync()

    def register_stereotype(self, st:s.Stereotype):
        st_name=st.name
        st_dayt=jso.dumps(st.day_transition_matrix.transition_prob)
        st_nightt=jso.dumps(st.night_transition_matrix.transition_prob)
        st_pt = st.public_transport

        with self._driver.session() as session:
            session.run(f"CREATE (st:Stereotype) SET st.name='{st_name}', st.day_transition='{st_dayt}', st.night_transition='{st_nightt}', st.public_transport='{st_pt}' RETURN st")
        
    def register_transport(self, l:s.Location):
        t_name = l.location_name
        t_type = l.location_type
        t_pro = l.pro_contact
        with self._driver.session() as session:
            session.run(f'CREATE (l:Transport) SET l.transport_name="{t_name}", l.transport_type="{t_type}", l.pro_contact ="{t_pro}"')

    def register_citizen(self, p:s.Person):  
        #, c:s.Ciudad
        mac = p.name
        status = p.status
        with self._driver.session() as session:
            session.run(f'CREATE (p:Person) SET p.mac="{mac}", p.status="{status}" RETURN p')
        
    
    def register_person(self, p:s.Person, city_name="Medayork"):
        mac = p.name
        
        with self._driver.session() as session:
            session.run(f'MATCH (p:Person) where p.mac="{mac}" MATCH (c:City) where c.name="{city_name}" CREATE (p)-[:VIVE]->(c)')
            session.run(f'MATCH (st:Stereotype) WHERE st.name="{p.stereotype.name}" MATCH(p:Person) WHERE p.mac="{mac}" CREATE (p)-[:ES_UN]->(st)')
        
            

    def register_location(self, l:s.Location, city_name="Medayork"):
        l_name = l.location_name
        l_type = l.location_type
        l_pro = l.pro_contact
        with self._driver.session() as session:
            session.run(f'CREATE (l:Location) SET l.location_name="{l_name}", l.location_type="{l_type}", l.pro_contact ="{l_pro}"')


    def register_commute(self, p:s.Person, l:s.Location, t_name):
        p_mac = p.name
        l_name = l.location_name
        with self._driver.session() as session:
            session.run(f'match(p:Person) where p.mac="{p_mac}" match(l:Location) where l.location_name="{l_name}" CREATE (p)-[:SE_MUEVE {{transporte:"{t_name}"}}]->(l)')

    def register_meeting(self, mac1, mac2, timeevent):
        with self._driver.session() as session:
            session.run(f'match(p:Person) where p.mac="{mac1}" match(q:Person) where q.mac="{mac2}" CREATE (p)-[:MEETS {{timestamp:"{timeevent}"}}]->(q)')


    def get_stereotype(self, stereoType):
        with self._driver.session() as session:
            ls = session.run(f'match (st:Stereotype) where st.name="{stereoType}" match (n:Person)-[:ES_UN]->(st) return n, st')
            lr = ls.records()
            people_st=[]
            for l in lr:            
                ite = l.get('n')
                itt = l.get('st')
                p_name =ite.get('mac')
                rlocs = session.run(f'match (p:Person) where p.mac="{p_name}" match (p)-[:SE_MUEVE]->(l) return l')
                locs = rlocs.records()
                l_loc = {}
                for lc in locs:
                    lcm= lc.get('l')
                    #print(lcm.keys())
                    if lcm.get('location_type') == 'h':
                        l_loc['h'] = s.Location(location_name=lcm.get('location_name'),location_type=lcm.get('location_type'),pro_contact=lcm.get('pro_contact'))
                    elif lcm.get('location_type') == 'w':
                        l_loc['w'] = s.Location(location_name=lcm.get('location_name'),location_type=lcm.get('location_type'),pro_contact=lcm.get('pro_contact'))
                    elif lcm.get('location_type') == 'n':
                        l_loc['n'] = s.Location(location_name=lcm.get('location_name'),location_type=lcm.get('location_type'),pro_contact=lcm.get('pro_contact'))
                #print(l_loc)   
                ster = s.Stereotype(name = p_name,day_transition_matrix=eval(itt.get('day_transition')),night_transition_matrix=eval(itt.get('night_transition')),public_transport=itt.get('public_stransport'))
                p_name = ite.get('mac')
                people_st.append(s.Person(name=p_name, stereotype=ster,my_spots=l_loc))
        return people_st

    def get_commutes(self, p:s.Person):
        p_name = p.name
        with self._driver.session() as session:
            ls = session.run(f'match (p:Person) where p.mac="{p_name}" match (p)-[:SE_MUEVE]-(loc) return loc')
        lr = ls.records()
        locs = []
        for l in lr:
            it = l.get('loc')
            locat = s.Location(location_name=it.get('location_name'),location_type=it.get('location_type'),pro_contact=it.get('pro_contact'))
            locs.append(locat)
        return locs

    def get_locations(self):
        with self._driver.session() as session:
            ls = session.run(f'match (l:Location) return l')
        lr = ls.records()
        locs = []
        for l in lr:
            it = l.get('l')
            locs.append(s.Location(location_name=it.get('location_name'),location_type=it.get('location_type'),pro_contact=float(it.get('pro_contact'))))
        return locs

if __name__ == "__main__":
    print("init")
    helper = GDBModelHelper("bolt://localhost:7687/neo4j","db_connect","Pr3M0rt3m")
    print('Cleaning db...')
    helper.clear_db()
    print('OK')
    helper.init_city(name="Medayork")
    st_apd = '{"h":{"h":0.025,"w":0.95,"n":0.025},"w":{"h":0.025,"w":0.95,"n":0.025},"n":{"h":0.05,"w":0.9,"n":0.05}}'
    st_apn = '{"h":{"h":0.95,"w":0.01,"n":0.04},"w":{"h":0.95,"w":0.01,"n":0.04},"n":{"h":0.9,"w":0.01,"n":0.09}}'
    st_ppd = '{"h":{"h":0.95,"w":0.0,"n":0.05},"w":{"h":1.0,"w":0.0,"n":0.0},"n":{"h":0.95,"w":0.0,"n":0.05}}'
    st_pprd = '{"h":{"h":0.25,"w":0.5,"n":0.25},"w":{"h":0.25,"w":0.5,"n":0.25},"n":{"h":0.5,"w":0.25,"n":0.25}}'
    st_ppn = '{"h":{"h":0.95,"w":0.0,"n":0.05},"w":{"h":0.95,"w":0.0,"n":0.05},"n":{"h":0.95,"w":0.0,"n":0.05}}'
    s_ap = s.Stereotype("active_person",eval(st_apd),eval(st_apn),False)
    s_app = s.Stereotype("active_person_public",eval(st_apd),eval(st_apn),True)
    s_pp = s.Stereotype("pasive_person",eval(st_ppd),eval(st_ppn),False)
    s_ppr = s.Stereotype("pasive_person_res",eval(st_pprd),eval(st_ppn),False)
    helper.register_stereotype(s_ap)
    helper.register_stereotype(s_app)
    helper.register_stereotype(s_pp)
    helper.register_stereotype(s_ppr)
    home = s.Location('home1', 'h', 0.001)
    office = s.Location('office1', 'w')
    market = s.Location('store', 'n')
    transportation = s.Location('mini-metro', 't', 0.1)
    helper.register_location(home)
    helper.register_location(office)
    helper.register_location(market)
    helper.register_location(transportation)
    #20w 30wp, 100h, 50d
    for i in range(20):
        c_name = str(randint(10,99))+':'+str(randint(10,99))+":"+str(randint(10,99))+":"+str(randint(10,99))
        person = s.Person(name=c_name,stereotype=s_ap,my_spots=[])
        helper.register_citizen(person)
        helper.register_person(person)
        #Todas las personas van a todas partes
        helper.register_commute(p=person,l=home,t_name= transportation.location_name)
        helper.register_commute(p=person,l=office,t_name= transportation.location_name)
        helper.register_commute(p=person,l=market,t_name= transportation.location_name)
    for i in range(30):
        c_name = str(randint(10,99))+':'+str(randint(10,99))+":"+str(randint(10,99))+":"+str(randint(10,99))
        person = s.Person(name=c_name,stereotype=s_app,my_spots=[])
        helper.register_citizen(person)
        helper.register_person(person)
        #Todas las personas van a todas partes
        helper.register_commute(p=person,l=home,t_name= transportation.location_name)
        helper.register_commute(p=person,l=office,t_name= transportation.location_name)
        helper.register_commute(p=person,l=market,t_name= transportation.location_name)
    for i in range(100):
        c_name = str(randint(10,99))+':'+str(randint(10,99))+":"+str(randint(10,99))+":"+str(randint(10,99))
        person = s.Person(name=c_name,stereotype=s_pp,my_spots=[])
        helper.register_citizen(person)
        helper.register_person(person)
        #Todas las personas van a todas partes
        helper.register_commute(p=person,l=home,t_name= transportation.location_name)
        helper.register_commute(p=person,l=office,t_name= transportation.location_name)
        helper.register_commute(p=person,l=market,t_name= transportation.location_name)
    for i in range(50):
        c_name = str(randint(10,99))+':'+str(randint(10,99))+":"+str(randint(10,99))+":"+str(randint(10,99))
        person = s.Person(name=c_name,stereotype=s_ppr,my_spots=[])
        helper.register_citizen(person)
        helper.register_person(person)
        #Todas las personas van a todas partes
        helper.register_commute(p=person,l=home,t_name= transportation.location_name)
        helper.register_commute(p=person,l=office,t_name= transportation.location_name)
        helper.register_commute(p=person,l=market,t_name= transportation.location_name)
    print('================================')
    #helper.get_commutes(person)
    #helper.get_stereotype("active_person_public")