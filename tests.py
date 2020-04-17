import unittest   # The test framework
from genesis import CityBuilder
from numpy.random import choice
import properties
from neo4j_graph_models import GDBAlgHelper


class Test_Project(unittest.TestCase):

    def test_city_builder_creation(self):
        zeus = CityBuilder(city_file='config/city_init.json')
        print(zeus.city_distribution)
        self.assertGreater(len(zeus.city_distribution.keys()), 0)
        self.assertTrue('locations' in zeus.city_distribution.keys())
        #self.assertRaises(AttributeError,  zeus.citizens)

    def test_city_builder_location(self):
        zeus = CityBuilder(city_file='config/city_init.json')
        zeus.create_locations()
        self.assertGreater(len(zeus.locations_city.keys()), 1)
        print(zeus.locations_city.keys())

    def test_city_builder_citizens(self):
        zeus = CityBuilder(city_file='config/city_init.json')
        zeus.populate()
        self.assertGreater(len(zeus.citizens.keys()), 1)
        print(zeus.citizens.keys())

    def test_city_builder_load(self):
        ozymandias = CityBuilder(city_file='config/city_init.json')
        ozymandias.create_locations()
        ozymandias.populate()
        ozymandias.load_city()
        citizens = ozymandias.citizens
        jhon_doe = choice(citizens['homers'])
        print(jhon_doe.showme_your_id())
        print(jhon_doe.my_spots)
        self.assertGreater(len(jhon_doe.my_spots.keys()), 1)
    
    def test_assign_homes(self):
        ozymandias = CityBuilder(city_file='config/city_init.json')
        ozymandias.create_locations()
        ozymandias.populate()
        ozymandias.load_city()
        ozymandias.assign_homes()
        jhon_doe = choice(ozymandias.citizens['homers'])
        print(jhon_doe.showme_your_id())
        j_home = jhon_doe.my_spots['h']
        self.assertTrue(jhon_doe in j_home.population)

    def test_check_graph_operations(self):
        alg_helper = GDBAlgHelper(driver=None, uri=properties.URI, 
            user= properties.USER, password=properties.PASSWORD)
        ## the graph catalog does not exists
        self.assertFalse(alg_helper.check_graph_catalog('test'))
         ## the graph catalog does not exists
        self.assertRaises(Exception, alg_helper.delete_graph_catalog, 'test')
        node_query = "MATCH (n:Person) RETURN id(n) AS id"
        relation_query = "MATCH (a:Person)-[:MEETS]->(b:Person) RETURN id(a) AS source, id(b) AS target"
        # create
        alg_helper.create_graph_catalog('test',node_query, relation_query)
        self.assertTrue(alg_helper.check_graph_catalog('test'))
        # create but the grapdh exists
        self.assertRaises(Exception, alg_helper.create_graph_catalog, 'test', node_query, relation_query)
        # delete grapdh check that the graph was deleted
        alg_helper.delete_graph_catalog('test')
        self.assertFalse(alg_helper.check_graph_catalog('test'))
    
    def test_create_meets_community_graph(self):
        alg_helper = GDBAlgHelper(driver=None, uri=properties.URI, 
            user= properties.USER, password=properties.PASSWORD)
        modularity = alg_helper.create_meets_community_graph('near-community', 'd0_h4', proximity=2)
        print(modularity)
        


    
    
    if __name__ == '__main__':
        unittest.main()