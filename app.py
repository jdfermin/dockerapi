from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Directories(db.Model):
    __tablename__ = 'directories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    emails = db.Column(db.ARRAY(db.String(50))) 

    def json(self):
        return{'id': self.id, 'name': self.name, 'emails': self.emails}

db.create_all()

@app.route('/status',methods=['GET'])
def status():
    return make_response('pong',200)

#crear directorio
@app.route('/directories', methods=['POST'])
def create_directory():
    try:
        data = request.get_json()
        new_directory = Directories(name=data['name'], emails=data['emails'])
        db.session.add(new_directory)
        db.session.commit()
        return make_response(jsonify({'message': 'directorio creado'}), 201)
    except e:
        return make_response(jsonify({'message': 'error al crear direcotorio'}), 500)

#consultar todos los directorios
@app.route('/directories', methods=['GET'])
def get_directories():
    try:
        directories = Directories.query.all()
        if directories:
            return make_response(jsonify({'directories': [directory.json() for directory in directories]}), 200)
        return make_response(jsonify({'message': 'no hay directorios registrados'}), 404)
    except e:
        return make_response(jsonify({'message': 'error al consultar directorios'}), 500)

#consultar directorio por id
@app.route('/directories/<int:id>', methods=['GET'])
def get_directory(id):
    try:
        directory = Directories.query.filter_by(id=id).first()
        if directory:
            return make_response(jsonify({'directorio': directory.json()}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except e:
        return make_response(jsonify({'message': 'error al consultar directorio'}), 500)

# actualizar directorio
@app.route('/directories/<int:id>', methods=['PUT'])
def update_directory(id):
    try:
        directory = Directories.query.filter_by(id=id).first()
        if directory:
            data = request.get_json()
            directory.name = data['name']
            directory.emails = data['emails']
            db.session.commit()
            return make_response(jsonify({'message': 'directorio actualizado'}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except e:
        return make_response(jsonify({'message': 'error al actualizar directorio'}), 500)


#eliminar directorio
@app.route('/directories/<int:id>', methods=['DELETE'])
def delete_directory(id):
    try:
        directory = Directories.query.filter_by(id=id).first()
        if directory:
            db.session.delete(directory)
            db.session.commit()
            return make_response(jsonify({'message': 'directorio eliminado'}), 200)
        return make_response(jsonify({'message': 'directorio no encontrado'}), 404)
    except e:
        return make_response(jsonify({'message': 'error al eliminar directorio'}), 500)

