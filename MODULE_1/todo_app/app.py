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

  # we should name the foreign key if we want to be able to downgrade the revision of migration. Otherwise it errors out with sqlalchemy.exc.CompileError that it cannot drop the foreign key constraint since the constraint has no name.

  # `server_default` vs `default` in SQLAlchemy:
  # SQLAlchemy uses two different options on Models' Columns to make INSERTions to have default values specified:
  # `default` works on application server's side. It renders the default expression in the INSERT or UPDATE statements and sends them to the database server. This option doesn't specify anything on the database side.
  # `server_default` works on database server's side. SQLAlchemy places the places the expression in the CREATE TABLE statement to put a default value there. Even if application server's side does not provide any value during an INSERT or UPDATE request, the database server puts the default there on its own.
  # read more: https://stackoverflow.com/questions/52431208/sqlalchemy-default-vs-server-default-performance

  list_id = db.Column(db.Integer(), db.ForeignKey('todolists.id', name='todolists_ref'), nullable=False, server_default='1')
  def __repr__(self):
    return f'<Todo {self.id} {self.description} in list {TodoList.query.filter_by(id=self.list_id).first()}>'

class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(), nullable=False)
  # db.relationship('ModelClassName', backref='this_is_how_the_chid_references_its_parent')
  todos = db.relationship('Todo', backref='list', lazy=True)
  def __repr__(self):
    return f'{self.id}: {self.name}'
# —————————————————————————————————————————————————————————————————————————————
# HANDLE ROUTES
# —————————————————————————————————————————————————————————————————————————————
@app.route('/todos/delete',methods=['DELETE'])
def delete_todo():
  error = False
  body = {}
  try:
    todo_id = request.get_json()['id']
    todo = Todo.query.get(todo_id) 
    db.session.delete(todo)
    db.session.commit()
    body['id'] = todo.id
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

@app.route('/todos/set-completed', methods=['PUT'])
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

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
  return render_template(
    'index.html', 
    lists=TodoList.query.all(), 
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('completed').order_by(Todo.id.desc()).all())

@app.route('/')
def index():
  return redirect(url_for('get_list_todos', list_id=1))
# —————————————————————————————————————————————————————————————————————————————
# FOR OPTIONAL RUNNING THE APP WITH `PYTHON` COMMAND
# —————————————————————————————————————————————————————————————————————————————
if __name__ == '__main__':
  app.run()