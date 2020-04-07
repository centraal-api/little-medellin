import unittest   # The test framework
from genesis import CityBuilder
from numpy.random import choice


class Test_CityBuilder(unittest.TestCase):

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

    
    if __name__ == '__main__':
        unittest.main()