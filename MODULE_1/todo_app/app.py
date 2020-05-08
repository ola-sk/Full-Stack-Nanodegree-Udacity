# —————————————————————————————————————————————————————————————————————————————
# RUN DEVELOPMENT SERVER
# —————————————————————————————————————————————————————————————————————————————
# Enable debug mode with either:
# $ export FLASK_ENV=development
# or
# $ export FLASK_DEBUG=true
# Exported variables persist per the terminal session.
# Export prior to running `flask run`. Or call together with `flask run`:
# 
# $ FLASK_APP=app.py FLASK_DEBUG=true flask run
# —————————————————————————————————————————————————————————————————————————————
# RUNNING THE APP
# —————————————————————————————————————————————————————————————————————————————
# 1st way:
# Terminal: in the directory of app.py
# $ export FLASK_APP=app.py
# $ flask run
# or
# $ FLASK_APP=app.py flask run

# 2nd way:
# Append this snippet to the end of the app.py file:
# 
# if __name__ == '__main__':
#   app.run()
# 
# and run the file with python:
# $ python app.py
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
# —————————————————————————————————————————————————————————————————————————————
# APP CONTENT
# —————————————————————————————————————————————————————————————————————————————

from flask import Flask, render_template, request, redirect, url_for, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
# TODO
# Manually create postgresql database set up in the app.config['SQLALCHEMY_DATABASE_URI']:
# 'SQLservertype://username:password@host:port/databasename
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ola:test123@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# —————————————————————————————————————————————————————————————————————————————
# MODELS
# —————————————————————————————————————————————————————————————————————————————
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String(), nullable=False)
  completed = db.Column(db.Boolean, nullable=False, default=False)
  def __repr__(self):
    return f'<Todo {self.id} {self.description}>'

# —————————————————————————————————————————————————————————————————————————————
# HANDLE ROUTES
# —————————————————————————————————————————————————————————————————————————————
@app.route('/todos/set-completed', methods=['POST'])
def set_completed_todo():
  error = False
  body = {}
  try:
    updateId = request.get_json()['id']
    isCompleted = request.get_json()['completed']
    todo = Todo.query.get(updateId)
    todo.completed = isCompleted
    db.session.commit()
    body['id'] = updateId
    body['completed'] = todo.completed
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description=description)
    db.session.add(todo)
    db.session.commit()
    body['id'] = todo.id
    body['completed'] = todo.completed
    body['decription'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    return jsonify(body)

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.order_by('completed').order_by('id').all())

# —————————————————————————————————————————————————————————————————————————————
# FOR OPTIONAL RUNNING THE APP WITH `PYTHON` COMMAND
# —————————————————————————————————————————————————————————————————————————————
if __name__ == '__main__':
  app.run()