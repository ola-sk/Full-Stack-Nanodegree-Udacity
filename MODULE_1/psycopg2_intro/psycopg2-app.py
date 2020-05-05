import psycopg2
from psycopg2.extensions import AsIs


# dbname – the database name, needs to exist already [`database` is a deprecated alias]
# user – user name used to authenticate
# password – password used to authenticate
# host – database host address (defaults to UNIX socket if not provided)
# port – connection port number (defaults to 5432 if not provided)

# AsIs from psycopg2.extensions should be used in order to format a string in python when
# https://www.psycopg.org/docs/extensions.html#psycopg2.extensions.AsIs

name='user_x'
cur.execute("create user %s with password %s", (AsIs(name), '0h/9warrAttrgd8EF0gkvQ==',))

conn = psycopg2.connect(dbname='todos', user='postgres', password='', host='127.0.0.1', port='5432')

# Open a cursor to perform database operations
cur = conn.cursor()

# Drop any existing tables if they exist
cur.execute("DROP TABLE IF EXISTS todos;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
SQL = """
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    completed boolean NOT NULL default false
  );
"""
cur.execute(SQL)
data = [3, True, 7, False]
SQL = 'INSERT INTO table2 (id, completed) VALUES ({}, {}), ({}, {});'.format(*data)
del data

cur.execute(SQL)

# commit, so it does the executions on the db and persists data in the db
conn.commit()

cur.close()
conn.close()
