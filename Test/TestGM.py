import unittest
from YourChef.gmHelper import MapHelper
import os
gmap_key = os.environ.get('gmap_key')

invalid_inputs = [
    {
        'latitude': "10000",
        'longitude': "0",
        'name': "Uncle",
    },
    {
        'latitude': "0",
        'longitude': "-999",
        'name': "Uncle",
    }
]

empty_response = [
    {
        'latitude': "0",
        'longitude': "0",
        'name': "Uncle",
    },
    {
        'latitude': "70",
        'longitude': "0",
        'name': "asdfadsa",
    }
]

success_response = [
    {
        'latitude': "70",
        'longitude': "0",
        'name': "Korean",
    },
    {
        'latitude': "40",
        'longitude': "-74",
        'name': "KFC",
    }
]

class TestMap(unittest.TestCase):

    def setUp(self):
        self.app = MapHelper()

    def testInvalid(self):
        for case in invalid_inputs:
            assert self.app.get_restuarant_info(case['name'],case['latitude'], case['longitude']) == 'Zero Result'
        
    def testEmpty(self):
        for case in empty_response:
            assert self.app.get_restuarant_info(case['name'],case['latitude'], case['longitude']) == 'Zero Result'
        
    def testNormal(self):
        for case in success_response:
            assert self.app.get_restuarant_info(case['name'],case['latitude'], case['longitude']) != 'Zero Result'


if __name__ == '__main__':
    unittest.main()
