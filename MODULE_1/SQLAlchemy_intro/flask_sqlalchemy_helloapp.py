# —————————————————————————————————————————————————————————————————————————————
# RUN DEVELOPMENT SERVER
# —————————————————————————————————————————————————————————————————————————————
# enable debug mode with either:
# $ export FLASK_ENV=development
# or
# $ export FLASK_DEBUG=true
# Exported variables persist per the terminal session.
# Export prior to running `flask run`. Or call together with `flask run`:
# 
# $ FLASK_APP=flask_helloapp.py FLASK_DEBUG=true flask run
# You can also export FLASK_APP=flask_helloapp.py from it's directory and `flask run`

# thanks to the code at the end of this file:
# if __name__ == '__main__':
#   app.run()
# you can simply execute in terminal:
# $ python flask_helloapp.py to run the server
# —————————————————————————————————————————————————————————————————————————————
# SET UP LINTING IN VS CODE
# —————————————————————————————————————————————————————————————————————————————
# For MS Code add following to the project's `.vscode/settings.json` to disable pylint yielding errors and warnings on some correct flask and flask-sqlalchemy specific code structuring:
# 
# {
#   "python.linting.pylintArgs": [
#     "--load-plugins",
#     "pylint-flask",
#     "pylint-flask-sqlalchemy",
#   ],
# }
# —————————————————————————————————————————————————————————————————————————————
# APP CONTENT
# —————————————————————————————————————————————————————————————————————————————
# —————————————————————————————————————————————————————————————————————————————
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# TODO
# Manually create postgresql database set up in the app.config['SQLALCHEMY_DATABASE_URI']:
# 'SQLservertype://username:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# —————————————————————————————————————————————————————————————————————————————
# MODELS
# —————————————————————————————————————————————————————————————————————————————
class Person(db.Model):
  __tablename__ = 'persons'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(), nullable=False)
  
  def __repr__(self):
    return f'<Person ID: {self.id}, name: {self.name}>'


# trivially (w/o migrations) create tables in our database for every declared db.Model
db.create_all()
# TODO
# Manually add the record with your name in the table created by SQLAlchemy as specified in the  the `Person` Model.
# —————————————————————————————————————————————————————————————————————————————
# HANDLE ROUTES
# —————————————————————————————————————————————————————————————————————————————
@app.route('/')
@app.route('/home')
@app.route('/hello')
# We can handle multiple routes with a single function by simply stacking additional route decorators above any route handling function.
# To learn more: https://hackersandslackers.com/flask-routes/
def index():
  # query from the database table mapped to the `Person` Model class.
  person = Person.query.first()
  return 'Hello {}!'.format(person.name)
# —————————————————————————————————————————————————————————————————————————————
# FOR OPTIONAL RUNNING THE APP WITH `PYTHON` COMMAND
# —————————————————————————————————————————————————————————————————————————————
if __name__ == '__main__':
  app.run()
