"""Modules to create test and Mock"""
import unittest
from unittest.mock import patch

from classes.api import Api

class TestApi(unittest.TestCase):
    """Class containing the test for the API class"""
    def setUp(self):
        self.api = Api()
        self.mock = {'product_name_fr': 'product_name',
                'nutriments': {
                    'nutrition-score-fr': 25},
                'image_front_url': 'image_url.com',
                'url': 'url.com'}
        self.mock_no_name = {'image_front_url': 25,
                'nutriments': {
                    'nutrition-score-fr': 25},
                'url': 'url.com'}
        self.mock_no_score = {'name': 'product_name',
                'image_front_url': 'image_url.com',
                'url': 'url.com'}
        self.mock_no_url = {'name': 'product_name',
                'nutriments': {
                    'nutrition-score-fr': 25},
                'nutriscore': 25,
                'image_front_url': 'image_url.com',}
        self.mock_no_img = {'name': 'product_name',
                'nutriments': {
                    'nutrition-score-fr': 25},
                'url': 'url.com'}
        self.response = { 'products' : []}

    
    @patch('requests.get')
    def test_imports(self, mock_api):
        """Testing if the method only keep result with every wanted elements"""
        self.response["products"].extend([self.mock, self.mock_no_url,
                                          self.mock_no_img, self.mock_no_score,
                                          self.mock_no_name])
        mock_api.return_value.json.return_value = self.response
        result = ('product_name',
                  25,
                  'image_url.com',
                  'url.com')      
        self.assertEqual(self.api.get_products('test'), [result])

    @patch('requests.get')
    def test_import_none(self, mock_api):
        """Testing if a None result returns False"""
        mock_api.return_value.json.return_value = None      
        self.assertFalse(self.api.get_products('test'))

if __name__ == "__main__":
    unittest.main()
