import sys

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'postgres:Postgresisamotherfucker01@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'ID: {self.id}, description: {self.description}'

db.create_all()

def fill_with_test_data():
    for i in range(5):
        test_data = Todo(description='do a thing ' + str(i))
        db.session.add(test_data)
    db.session.commit()
#fill_with_test_data()


@app.route('/todos/create', methods=['POST'])
def create_todo():
  error = False
  body = {}
  try:
    description = request.get_json()['description']
    todo = Todo(description2=description)
    db.session.add(todo)
    db.session.commit()
    body['description'] = todo.description
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return jsonify(body)


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())



if __name__ == '__main__':
  app.run(debug=True)