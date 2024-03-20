from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db' #se llama la base task.db, es el nombre que tu le quieras poner
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable=False) #Puede ser nulo o no, en este caso, le estamos indicando que no
    status = db.Column(db.Boolean, default=False) # Falso significa que aún no está completado
    
    def rellenar(self):
        diccionario = {
            'ID': self.id,
            'name': self.name,
            'status': self.status
        }
        return diccionario
        
    
    def __init__(self, name, status):
        self.name = name
        self.status = status
        
    
    def __repr__(self):
        return f'<Task {self.name}>'
    
    
@app.route('/create')
def create_tables():
    db.create_all()
    return "Tables created..."

@app.route('/')
def index():
    return 'Welcome to my ORM app'

@app.route('/create_task')
def create():
    task = Task('First task', False)
    db.session.add(task)
    db.session.comit()
    return 'Task added'

@app.route('/create_task2', methods = ['POST'])
def create2():
    if not request.json or not 'name' in request.json: #La llave es name, por eso la pongo aqui
        abort(404, error = "Hijole, hay un error")
        
    name = request.json['name']
    status = request.json.get( 'status', False )
    new_task = Task(name=name, status=status)
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'task': new_task.rellenar()}), 201 
     

@app.route('/task')
def read():
    task = Task.query.all()
    print(task)
    return 'Task fetched'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Tables created...")
    app.run(debug=True)
