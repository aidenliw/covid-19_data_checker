"""
The database management class is using Object pool pattern.
There are two databases are used in the model, which are SQLite3 and Redis Labs

Object pool is a creational design pattern that keeps a pool of objects and
provide access to them, rather than creating and destroying new objects,
which offers a significant performance boost

References: https://sourcemaking.com/design_patterns/object_pool/python/1
"""

from abc import ABC, abstractmethod
import sqlite3
import redis


# The re-usable SQLite DB connection that the object pool will manage
class ReusableSQLite:

    def __init__(self):
        self.myconn = sqlite3.connect("favourite.db")

    def __del__(self):
        self.myconn.close()


# Manages the pool of objects, offers acquire and release operations to
# give the objects to client code and accept them back
class ObjectPoolSQLite:

    # initialize the pool... in our case, just one re-usable object
    def __init__(self):
        self.__reusables = [ReusableSQLite()]

    # give the resource to a client
    def acquire(self):
        return self.__reusables.pop()

    # accept the resource back from a client
    def release(self, reusable):
        self.__reusables.append(reusable)


class Model():

    # Initialize the database tables
    def initialize(self, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        # Create tables
        cur.execute('''CREATE TABLE IF NOT EXISTS country (name text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS province (name text, abbreviation text)''')

        # Save (commit) the changes and close the connection
        db.myconn.commit()
        pool.release(db)

    # Insert new country data
    def insert_country(self, country_name, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute("SELECT * FROM country WHERE name = ?", (country_name,))
        result = cur.fetchone()

        # If the data already exists, do nothing
        if result:
            pass
        else:
            # Insert a row of data
            cur.execute("INSERT INTO country VALUES (?)", (country_name,))
            db.myconn.commit()

        pool.release(db)

    # Insert new country data
    def insert_province(self, province_name, abbreviation, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute('SELECT * FROM province WHERE name = ?', (province_name,))
        result = cur.fetchone()

        # If the data already exists, do nothing
        if result:
            pass
        else:
            # Insert a row of data
            cur.execute("INSERT INTO province VALUES (?, ?)", (province_name, abbreviation))
            db.myconn.commit()

        pool.release(db)

    # Get all countries data
    def get_all_countries(self, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute('SELECT * FROM country ORDER BY name')
        rows = [r[0] for r in cur]
        pool.release(db)
        return rows

    # Get the specified country data
    def get_country(self, name, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute('SELECT * FROM country WHERE name = ?', (name,))
        rows = [r[0] for r in cur]
        pool.release(db)
        return rows

    # Get all provinces data
    def get_all_provinces(self, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute('SELECT * FROM province ORDER BY name')
        rows = [r[0] for r in cur]
        pool.release(db)
        return rows

    # Get the specified province data
    def get_province(self, name, pool):
        db = pool.acquire()
        cur = db.myconn.cursor()
        cur.execute('SELECT * FROM province WHERE name = ?', (name,))
        rows = [r[0] for r in cur]
        pool.release(db)
        return rows

    # def delete_country(self, con, country_name):
    #     cur = con.cursor()
    #     cur.execute("DELETE FROM country WHERE name=?", (country_name,))
    #
    # def delete_province(self, con, province_name):
    #     cur = con.cursor()
    #     cur.execute("DELETE FROM province WHERE name=?", (province_name,))


# Create an object pool
my_sql_pool = ObjectPoolSQLite()

# test = Model()
# test.initialize(my_sql_pool)
# test.insert_country("Canada", my_sql_pool)
# print(test.get_all_countries())


# Redis database connection
class Redis:

    def __init__(self):
        self.redis = redis.Redis(
            host='redis-15205.c74.us-east-1-4.ec2.cloud.redislabs.com',
            port=15205,
            password='xCIM2XUdlfccoZZSICnMRlo4ncsqT7vk',
            decode_responses=True)




