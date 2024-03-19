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
import db
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


# @socketio.on('message_to_td')
# def handle_message(data):
#     print('received message: ' + data)
#     socketio.emit('message_to_td', data)

# @app.route('/api/imageData', methods=['GET', 'POST'])
# def image_data():
#     if request.method == 'GET':
#         requests.post('wss://echo.websocket.org', data={'Hello': 'World'})
#         return 'Hello, World'
        

@socketio.on('my event')  # Listening for the event named "my event"
def handle_my_custom_event(json):
    print('received json: ' + str(json))
    # You can emit back a response to the client or broadcast to all clients
    socketio.emit('my response', json)

async def websocket_test():
    uri = "wss://echo.websocket.org"
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send("Hello, World")
            response = await websocket.recv()
            return response
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/api/test_websocket', methods=['GET'])
def test_websocket_route():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(websocket_test())
    return result
