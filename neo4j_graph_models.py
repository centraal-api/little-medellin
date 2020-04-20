from neo4j import GraphDatabase
import toolbox
import pandas as pd

class GDBAlgHelper():

    def __init__(self, driver, uri=None, user = None, password = None):
        
        if driver is None:
            self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
            
        else:
            self.driver = driver
    
        self.person_features = ['mac', 'stereotype', 'high_promity', 'low_proximity', 'community_commute', 'status']

    def run_query(self, query, debug = True):
        if (debug):
            print("query: ", query)
        with self.driver.session() as session:
            return (session.run(query))


    def check_graph_catalog(self, catalog_name):
        results = self.run_query(f"CALL gds.graph.exists('{catalog_name}') YIELD exists;")
        return (results.value()[0])

    def create_graph_catalog(self, catalog_name,  node_query, relation_query):
        if (self.check_graph_catalog(catalog_name)):
            raise Exception("graph  already exists")
        else:
            query = f"""CALL gds.graph.create.cypher( '{catalog_name}',
            '{node_query}',
            '{relation_query}')
            """
            self.run_query(query)

    def delete_graph_catalog(self, catalog_name):
        if (not self.check_graph_catalog(catalog_name)):
            raise Exception("graph does not exist")
        else:
            query = f"CALL gds.graph.drop('{catalog_name}') YIELD graphName;"
            self.run_query(query)
    
    def create_meets_community_graph(self, graph_name, time_event, prop='community', proximity='<=2'):
        today = toolbox.get_timestamp(time_event)
        d_ago = today - 15*24*3600
        node_query = 'MATCH (n:Person) RETURN id(n) AS id'
        relation_query = f"""MATCH (a:Person)-[m:MEETS]->(b:Person) WHERE m.proximity{proximity} 
            AND m.timestamp >= {d_ago} AND m.timestamp <= {today} 
            RETURN id(a) AS source, id(b) AS target"""
        self.create_graph_catalog(graph_name, node_query, relation_query)
        model_query =f"CALL gds.louvain.write('{graph_name}',"
        model_query = model_query +  f" {{ writeProperty: '{prop}' }}) YIELD communityCount, modularity, modularities"
        modularity = self.run_query(model_query)
        modularity = modularity.data()[0]['modularity']
        self.delete_graph_catalog(graph_name)
        return(modularity)

    def create_se_mueve_community_graph(self, graph_name, time_event):
        today = toolbox.get_timestamp(time_event)
        d_ago = today - 15*24*3600
        node_query = 'MATCH (n) WHERE n:Person OR n:Location RETURN id(n) AS id'
        relation_query = f"""MATCH (a:Person)-[m:SE_MUEVE]->(l:Location) WHERE m.timestamp >= {d_ago} 
            AND m.timestamp <= {today} RETURN id(a) AS source, id(l) AS target"""
        self.create_graph_catalog(graph_name, node_query, relation_query)
        model_query =f"CALL gds.louvain.write('{graph_name}',"
        model_query = model_query +  " { writeProperty: 'community_commute' }) YIELD modularity"
        modularity = self.run_query(model_query)
        modularity = modularity.data()[0]['modularity']
        self.delete_graph_catalog(graph_name)
        return(modularity)

    def get_persons_df(self):
        person_q = f"MATCH (p:Person) RETURN {','. join([f'p.{f} AS {f}' for f in self.person_features])}"
        persons = self.run_query(person_q)
        persons_df = pd.DataFrame(persons.data())
        return (persons_df)
        