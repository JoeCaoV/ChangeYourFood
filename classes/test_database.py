import mysql.connector
from .api import Api
from .database import Database
from config import CATEGORIES
from secret import HOST, USER, PASSWD

class TestDb(Database):

    def __init__(self):
        """create the connector and create the database and
        all required elements if they don't exist yet
        """
        try:
            self.connector = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWD,
                database='TESTDB',
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
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS TESTDB")

        self.connector = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWD,
            database='TESTDB',
        )
        self.mycursor = self.connector.cursor()

    def drop_schema(self):
        """Delete the database"""
        self.mycursor.execute("DROP DATABASE IF EXISTS testdb")
