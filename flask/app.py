# requirements.txt
# pip install -U Flask
# pip install requests
# pip install -U flask-cors
# pip install flask flask-socketio
# pip install Flask-SQLAlchemy
# pip install websockets

# File imports
from flask import Flask
from flask import request
import requests
from flask_cors import CORS
from datetime import date
# import db
from flask_socketio import SocketIO

from flask_sqlalchemy import SQLAlchemy
import sqlite3
import asyncio
import websockets

# Create the Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
socketio = SocketIO(app)

# database with whoever does that
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)

CORS(app)

API_KEY = '3x1ffNiowcASHEnfhbH7KkcylZTkRfQfytyyL4JE'

# makes it so that the url is http://127.0.0.1:5000/api/????
@app.route('/api/apod', methods=['GET', 'POST'])
def api():
    if request.method == 'GET':
        request_data = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + API_KEY)
        requests.post('http://localhost:3000', data=request_data.json()['url'])
        return request_data.json()['url']
    else:
        request_data = requests.get('https://api.nasa.gov/planetary/apod?api_key=' + API_KEY)
        return request_data.json()['url']
    
@app.route('/api/slider1', methods=['GET', 'POST'])
def slider1():
    if request.method == 'POST':
        # get the data from the request
        data = request.json
        # send the data to the front end
        socketio.emit('slider1', data)
        return data
    else:
        return 'GET request'
    
@socketio.on('data')
def handle_data(data):
    # decode the data base64

    # send the data to the front end
    requests.post('http://localhost:3000', data=data)

# more api endpoints per request
    
# example login function
# @app.route('/api/login', methods=['POST'])
# def login():
#     db.create_all()
#     if request.method == 'POST':
#         username = request.json['username']
#         password = request.json['password']
        
#         # Query the database for the user
#         user = User.query.filter_by(username=username).first()
        
#         # Check if user exists and password matches
#         if user and user.password == password:
#             # Successful login
#             requests.post('http://localhost:3000', data='Logged in')
#             return {'message': 'Logged in'}, 200
#         else:
#             # Failed login
#             requests.post('http://localhost:3000', data='Invalid credentials')
#             return {'message': 'Invalid credentials'}, 401



@socketio.on('TD event')  # Listening for the event named "my event"
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    # You can emit back a response to the client or broadcast to all clients
    requests.post('http://localhost:3000', data=json)
# ws://127.0.0.1:5000
