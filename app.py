from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from os form environ

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URL'] = environ.get('DB_URL')
db = SQLAlchemy(app)

@app.route('/status',methods=['GET'])
def status():
    return make_response(jsonify({'pong'}),200)