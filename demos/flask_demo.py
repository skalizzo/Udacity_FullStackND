from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#Aufbau URI: 'postgresql://myusername:mypassword@localhost:5432/mydatabase'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' \
                                        'postgres:Postgresisamotherfucker01@localhost:5432/todoapp_development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    # -->wenn man will, dass die Tabelle anders heißt als Klasse,
    # ansonsten lower case version von Klassenname
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'Person ID: {self.id}, name: {self.name}'

#create
db.create_all()

#testperson = Person(name='Christian')
#db.session.add(testperson)
#db.session.commit()

@app.route('/')
def hello_world():
    person = Person.query.first()
    if person:
        print(person)
        return 'Hello ' + person.name
    else:
        return 'No entrys found in database'



if __name__ == '__main__':
  app.run(debug=True)