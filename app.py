from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class Directory(db.Model):
    __tablename__ = 'directory'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def json(self):
        return{'id': self.id, 'name': self.name}

db.create_all()

@app.route('/status',methods=['GET'])
def status():
    return make_response('pong',200)
