"""Import mysql.connector to communicate with sever
and the CONSTANT var required
"""
import mysql.connector
from .api import Api
from config import CATEGORIES
from secret import HOST, USER, PASSWD

class Database:
    """This class is used for every iteraction with the database,
    even creating it if it doesn't exist yet"""

    def __init__(self):
        """create the connector and create the database and
        all required elements if they don't exist yet
        """
        try:
            self.connector = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWD,
                database='CYF',
                )
            self.mycursor = self.connector.cursor()

        except mysql.connector.errors.ProgrammingError:
            self.connector = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWD,
                )
            self.mycursor = self.connector.cursor()
            self.create_database()
            self.create_table_categories()
            self.insert_categories()
            self.create_table_product()
            self.create_table_alternative()

    def create_database(self):
        """Create the database if it doesn't exist then update the connector"""
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS CYF")

        self.connector = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWD,
            database='CYF'
        )
        self.mycursor = self.connector.cursor()

    #CATEGORIES TABLE

    def create_table_categories(self):
        """Create the table Categories"""
        table = "CREATE TABLE IF NOT EXISTS Categories" +\
                "(id INTEGER(2) PRIMARY KEY NOT NULL AUTO_INCREMENT," +\
                "name VARCHAR(155) NOT NULL)"
        self.mycursor.execute(table)

    def insert_categories(self):
        """Insert the categories into their table"""
        cat_query = self.get_categories()
        if not cat_query:
            query = "INSERT INTO Categories (id, name) VALUES (NULL, %s)"
            self.mycursor.executemany(query, CATEGORIES)
            self.connector.commit()

    def get_categories(self):
        """Return all the categories"""
        query = "SELECT * FROM Categories"
        self.mycursor.execute(query)
        result = self.mycursor.fetchall()
        return result

    def get_saved_categories(self):
        """Get the list of every Category cointaining
        saved alternative product
        """
        query = "SELECT DISTINCT Categories.id, Categories.name " +\
                "FROM Categories " +\
                "INNER JOIN Products ON Categories.id = Products.category_id " +\
                "INNER JOIN Alternatives On Products.id = Alternatives.product_id " +\
                "ORDER BY Categories.id ASC"
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    #PRODUCT TABLE

    def create_table_product(self):
        """Create the table of product if it doesn't exist"""
        query = "CREATE TABLE IF NOT EXISTS Products" +\
                "(id INTEGER(2) PRIMARY KEY NOT NULL AUTO_INCREMENT," +\
                "name VARCHAR(155) NOT NULL," +\
                "nutriscore INTEGER(2) NOT NULL," +\
                "image_url VARCHAR(255) NOT NULL," +\
                "url VARCHAR(255) NOT NULL," +\
                "category_id INTEGER(2) NOT NULL," +\
                "CONSTRAINT fk_category FOREIGN KEY (category_id)" +\
                "REFERENCES Categories(id)" +\
                ")"
        self.mycursor.execute(query)

    def insert_product(self, data, category):
        """Insert the product selected by the API into the database
        parameter 'data' must be a tuple containing :
        name, codebar, url, nutriscore, category_id
        """
        category += 1
        datas = data + (category, )
        query = "INSERT INTO Products VALUES (NULL, %s, %s, %s, %s, %s)"
        self.mycursor.execute(query, datas)
        self.connector.commit()

    def get_products(self):
        """get all the product"""
        query = "SELECT * FROM Products"
        self.mycursor.execute(query)
        return self.mycursor.fetchall()

    def get_products_by_category(self, category, page):
        """get 10 products from the given category"""
        query = "SELECT * FROM Products " +\
                "INNER JOIN Categories " +\
                "ON Categories.id = Products.category_id " +\
                "WHERE Categories.name = %s " +\
                "LIMIT 10 OFFSET %s"
        data = (category, (page-1)*10)
        self.mycursor.execute(query, data)
        return self.mycursor.fetchall()

    def get_product(self, prod_id):
        """get the id of an product"""
        query = "SELECT * FROM Products WHERE id = %s AND category_id = %s"
        data = (prod_id, )
        self.mycursor.execute(query, data)
        return self.mycursor.fetchone()

    def get_saved_products(self, category):
        """Get the list of every product with a alternative food saved
        and belonging to the given category
        """
        query = "SELECT * FROM Products " +\
                "INNER JOIN Alternatives ON Products.id = Alternatives.product_id " +\
                "WHERE Products.category_id = %s"
        data = (category, )
        self.mycursor.execute(query, data)
        return self.mycursor.fetchall()

    #ALTERNATIVE TABLE

    def create_table_alternative(self):
        """create the table of alternative product
        if it doesn't exist
        """
        query = "CREATE TABLE IF NOT EXISTS Alternatives" +\
                "(id INTEGER(2) PRIMARY KEY NOT NULL AUTO_INCREMENT," +\
                "name VARCHAR (155) NOT NULL," +\
                "codebar BIGINT (13) NOT NULL," +\
                "url VARCHAR(255) NOT NULL," +\
                "nutriscore INTEGER(2) NOT NULL," +\
                "product_id INTEGER (2) NOT NULL UNIQUE," +\
                "CONSTRAINT fk_product FOREIGN KEY (product_id) REFERENCES Products(id)" +\
                ")"
        self.mycursor.execute(query)

    def get_best_alternative(self, product):
        """find the best alternative product for the given product"""
        query = "SELECT * FROM Products " +\
                "INNER JOIN Categories " +\
                "ON Products.category_id = Categories.id " +\
                "WHERE Categories.id = %s " +\
                "AND Products.nutriscore < %s " +\
                "ORDER BY Products.nutriscore " +\
                "LIMIT 1"
        data = (product[5], product[2])
        self.mycursor.execute(query, data)
        return self.mycursor.fetchone()

    def insert_alternative(self, data):
        """Add the substitute product to the database
        the 'data parameter must be a tuple containing :
        name, codebar, url, nutriscore, produit_id
        """
        query = "INSERT INTO Alternatives VALUES (NULL, %s, %s, %s, %s, %s)"
        try:
            self.mycursor.execute(query, data)
            self.connector.commit()
            print("Le produit :", data[0], "a bien été enregistré")
        except mysql.connector.errors.IntegrityError:
            print("Ce produit a déjà été enregistré")

    def get_saved_alternative(self, product):
        """get the substitution of the given product"""
        query = "SELECT * FROM Alternatives WHERE product_id = %s"
        data = (product[0], )
        self.mycursor.execute(query, data)
        return self.mycursor.fetchone()

    #Method to insert data got from the api to insert them into products table

    def insert_products_from_api(self):
        api = Api()
        for index, category in enumerate(CATEGORIES):
            products = api.get_products(category)
            for product in products:
                self.insert_product(product, index)
