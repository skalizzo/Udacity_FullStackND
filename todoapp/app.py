import sys
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'postgres:Postgresisamotherfucker01@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)


# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'ID: {self.id}, description: {self.description}'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True)


# db.create_all() wird nicht mehr benötigt da alles über flask-migrate gesteuert wird
# db.create_all()


def fill_with_test_data():
    for i in range(5):
        test_data = Todo(description='do a thing ' + str(i))
        db.session.add(test_data)
    db.session.commit()

def fill_with_test_data2():
    list = TodoList(name='Urgent')
    todo = Todo(description='urgent todo 1')
    todo2 = Todo(description='urgent todo 2')
    todo3 = Todo(description='urgent todo 3')
    todo.list = list
    todo2.list = list
    todo3.list = list
    db.session.add(list)
    db.session.commit()
#fill_with_test_data2()

# fill_with_test_data()

@app.route('/todolist/create', methods=['POST'])
def create_todolist():
    error = False
    body = {}
    try:
        name = request.get_json()['name']
        todolist = TodoList(name=name)
        db.session.add(todolist)
        db.session.commit()
        body['name'] = todolist.name
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

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        todo = Todo(description=description)
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


@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        Todo.query.filter_by(id=todo_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({'success': True})


@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        print('completed', completed)
        todo = Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index.html',
                           lists=TodoList.query.order_by('id').all(),
                           active_list=TodoList.query.get(list_id),
                           todos=Todo.query.filter_by(list_id = list_id).order_by('id').all())


@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
    app.run(debug=True)
