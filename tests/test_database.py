"""Modules to create test and Mock"""
import unittest
from unittest.mock import patch
from config import CATEGORIES
from classes.api import Api
from classes.test_database import TestDb

class TestsDatabase(unittest.TestCase):
    """Class containing the test for the API class"""
    def setUp(self):

        self.database = TestDb()
        self.api = Api()
        self.mock = [
                ('product_name1', 25, 'image_url.com','url.com'),
                ('product_name2', 12, 'image_url.com','url.com'),
                ('product_name3', 5, 'image_url.com','url.com'),
                ('product_name4', 25, 'image_url.com','url.com'),
                ('product_name5', 12, 'image_url.com','url.com'),
                ('product_name6', 5, 'image_url.com','url.com'),
                ('product_name7', 25, 'image_url.com','url.com'),
                ('product_name8', 12, 'image_url.com','url.com'),
                ('product_name9', 5, 'image_url.com','url.com'),
                ('product_name10', 25, 'image_url.com','url.com'),
                ('product_name11', 12, 'image_url.com','url.com'),
                ('product_name12', 5, 'image_url.com','url.com'),
            ]

    def test_1_import_categories(self):
        """Check if every categories have been imported"""
        categories = self.database.get_categories()
        self.assertEqual(len(categories), len(CATEGORIES))
    
    @patch('classes.api.Api.get_products')
    def test_2_import_products(self, mock_api):
        """trying the method insering the products list to the database
        here, the data supposed to come from Api.get_products are mocked
        """
        mock_api.return_value = self.mock
        products_before = self.database.get_products()
        self.database.insert_products_from_api()
        products_after = self.database.get_products()
        self.assertEqual(len(products_before) + 12 * len(CATEGORIES),
                         len(products_after))

    def test_3_get_products_by_category_page_1(self):
        """Testing if this method return correctly 10 out of 12 product"""
        products = self.database.get_products_by_category('Glaces', 1)
        self.assertTrue(len(products) == 10)

    def test_4_get_products_by_category_page_2(self):
        """Testing if this method return correctly 2 out of 12 product"""
        products = self.database.get_products_by_category('Glaces', 2)
        self.assertTrue(len(products) == 2)

    def test_9_final(self):
        """Sorry dear database, you were only here for the tests
        now I'm destroying you.
        OMAE WA MOU SHINDEIRU"""
        self.database.drop_schema()

if __name__ == "__main__":
    unittest.main()
