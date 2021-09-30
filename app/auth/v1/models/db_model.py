import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

class Quora_Db:
    """
    Create the connection to a database & create table
    """

    @classmethod
    def init_db(cls, db_name,db_host,db_password,db_user):
        """
        Method to initialize the database
        """
        cls.conn =  psycopg2.connect(
            host = db_host,
            password = db_password,
            database = db_name,
            user = db_user
        )
        cls.cur = cls.conn.cursor(cursor_factory=RealDictCursor)
        print("Database = ", cls.conn.get_dsn_parameters())

    @classmethod
    def build_tables(cls):
        """
        Method to create the tables in the database
        """
        try:
            cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS users(
                userId serial PRIMARY kEY,
                username VARCHAR NOT NULL,
                email VARCHAR UNIQUE NOT NULL,
                userpassword VARCHAR NOT NULL,
                confirm_password VARCHAR NOT NULL
            )
            """)
            cls.conn.commit()
            print('Tables successfully created')
        except Exception as e:
            Error(e)
            print('What happened? =>', e)

    @classmethod
    def add_to_db(cls, query_string, tuple_data):
        """
        method that saves queries into the database
        """
        try:
            cls.cur.execute(query_string, tuple_data)
            cls.conn.commit()
            response = cls.cur.fetchall()
            return response
        except Exception as e:
            print(e)

    @classmethod
    def retrieve_one(cls, query_string):
        """
        method returns data on a particular row from the database
        """
        cls.cur.execute(query_string)
        return cls.cur.fetchone()

    @classmethod
    def retrieve_all(cls, query_string):
        """
        returns all specified columns from table rows
        """
        cls.cur.execute(query_string)
        return cls.cur.fetchall()