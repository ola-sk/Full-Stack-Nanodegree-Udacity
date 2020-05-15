import psycopg2
from psycopg2.extensions import AsIs
from psycopg2 import sql
from psycopg2 import extensions


# dbname – the database name, needs to exist already [`database` is a deprecated alias]
# user – user name used to authenticate
# password – password used to authenticate
# host – database host address (defaults to UNIX socket if not provided)
# port – connection port number (defaults to 5432 if not provided)

# AsIs from psycopg2.extensions should be used in order to format a string in python when
# https://www.psycopg.org/docs/extensions.html#psycopg2.extensions.AsIs

conn = psycopg2.connect(
  dbname='', 
  user='ola', 
  password='test123', 
  host='127.0.0.1', 
  port='5432')

# https://kb.objectrocket.com/postgresql/create-a-postgresql-database-using-the-psycopg2-python-library-755
# Open a cursor to perform database operations
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
conn.set_isolation_level( autocommit )
del autocommit
cur = conn.cursor()


# SQL string composition—on securely executing raw sql statements:
# https://www.psycopg.org/docs/sql.html
def recreate_db(dbname):
  cur.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(sql.Identifier( dbname )))
  cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier( dbname )))

def recreate_user(username, password):
  cur.execute(sql.SQL("DROP USER IF EXISTS {}").format(sql.Identifier( username )))
  # Error that I had that the uncomposable argument is passed (password) and that it doesn't support indexing. Solution was to make the password a tuple.
  cur.execute(sql.SQL("create user {} with encrypted password %s").format(sql.Identifier(username)), (password,))



dbname = 'psycopg2_test'
recreate_db(dbname)
conn.commit()
del dbname

user = 'user_x'
psw = '0h/9warrAttrgd8EF0gkvQ=='
recreate_user(user, psw)
conn.commit()
del user, psw

cur.close()
conn.close()
# After creating a new user and a database in the postgresql DBMS, let's change parameters of the connections, so that operations are performed by a new user
conn = psycopg2.connect(dbname='psycopg2_test', user='user_x', password='0h/9warrAttrgd8EF0gkvQ==', host='127.0.0.1', port='5432')
cur = conn.cursor()
# Drop any existing tables if they exist
cur.execute("DROP TABLE IF EXISTS todos")
conn.commit()
# (re)create the todos table
# (note: triple quotes allow multiline text in python)
SQL = sql.SQL("""
  CREATE TABLE todos (
    id serial PRIMARY KEY,
    completed boolean NOT NULL default false
  )
""")
cur.execute(SQL)
conn.commit()


data1 = ('3', 'true')
data2 = ('7', 'false')
SQL = sql.SQL("INSERT INTO todos (id, completed) VALUES %s, %s")
# here we have a literal representation of a tuple as written in python put straight to a SQL command.
cur.execute(SQL, (data1, data2))

# commit, so it does the executions on the db and persists data in the db
conn.commit()

cur.close()
conn.close()
