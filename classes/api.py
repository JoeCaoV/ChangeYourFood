# coding: utf-8
"""Module requests required to use the API"""
import requests

class Api:
    """contain the methods to request the API"""

    def __init__(self):
        self.search_url = 'https://fr-en.openfoodfacts.org/cgi/search.pl'

    def get_products(self, category):
        """Get 100 product from the API belonging to the given category
        only return the product with a name, nutriscore, image and url
        """
        params = {'search_terms' : category, 'json' : 1, 'page_size' : 100}
        api_get = requests.get(self.search_url, params=params).json()
        try:
            products = api_get['products']
        except (KeyError, IndexError, TypeError):
            return False
        else:
            result = []
            for count, product in enumerate(products):
                try:
                    product = (products[count]['product_name_fr'],
                               products[count]['nutriments']['nutrition-score-fr'],
                               products[count]['image_front_url'],
                               products[count]['url'])
                except (IndexError, KeyError):
                    continue
                else:
                    result.append(product)
        return result
