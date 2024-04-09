
# File imports
from flask import Flask
from flask import request
import requests
from flask_cors import CORS
from flask_socketio import SocketIO
import asyncio
import websockets
import base64
import json

# ********************************************************* INIT SERVER **************************************************
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
socketio = SocketIO(app, logger=True)
socketio.run(app, host='127.0.0.1', port=5001)
CORS(app)

# ********************************************************* DATABASE (INC) **************************************************

# database with whoever does that
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String(80), nullable=False)


# ********************************************************* API ENDPOINTS **************************************************

# Server runs on http://127.0.0.1:5000

# ************************ Example API endpoint ************************

# API key for NASA API
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
    
    
# requested parameters
# get more data from datasets here: https://www.ncei.noaa.gov/access/search/dataset-search?observationTypes=Land%20Surface
# @app.route('/api/particle_cloud/forest', methods=['GET'])
@app.route('/api/particle_cloud/ocean', methods=['GET'])
def ocean():
    request_data = requests.get('https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-marine&amp;dataTypes=WIND_DIR,WIND_SPEED&amp;stations=AUCE&amp;startDate=2016-01-01&amp;endDate=2016-01-02&amp;boundingBox=90,-180,-90,180')
    # STATION	DATE	LATITUDE	LONGITUDE	WIND_DIR	WIND_SPEED
    tosend = request_data.json().split('\n')
    try:
        websocket = websockets.connect("ws://127.0.0.1:5000")
        for line in tosend:
            websocket.send(line.split(',')[4:])
    except Exception as e:
        return f"An error occurred: {e}"

MAP_KEY = 'e8aa84fba48bdd97c918f27b26ad74c6'
@app.route('/api/particle_cloud/fire', methods=['GET'])
def fire():
    # format /api/area/csv/[MAP_KEY]/[SOURCE]/[AREA_COORDINATES]/[DAY_RANGE]
    # area coordinates expect [-90...90]
    # ex: https://firms.modaps.eosdis.nasa.gov/api/area/csv/e8aa84fba48bdd97c918f27b26ad74c6/VIIRS_SNPP_NRT/world/1
    request_data = requests.get('https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_SNPP_NRT/world/1')
    # gives latitude,longitude,bright_ti4,scan,track,acq_date,acq_time,satellite,instrument,confidence,version,bright_ti5,frp,daynight

    # send latitude, longitude, and brightness to touchdesigner the first three values in each line
    tosend = request_data.json().split('\n')
    # for line in tosend:
    #     requests.post('http://localhost:3000', data=line.split(',')[0:3])
    try:
        websocket = websockets.connect("ws://127.0.0.1:5000")
        for line in tosend:
            websocket.send(line.split(',')[0:3])
    except Exception as e:
        return f"An error occurred: {e}"
    # return request_data.json()['latitude']

    


# ************************************************** SOCKET FUNCTION **************************************************

# https://127.0.0.1:5000/socket/initMessage
@app.route('/socket/initMessage', methods=['GET'])
def init_message():
    toSend = {"Slider1" : 0.56, "Slider2" : 0.72}
    jsonToSend = json.dumps(toSend)
    # socketio.emit('initMessage', jsonToSend)
    socketio.send(jsonToSend, json=True)
    return 'Message sent'

@socketio.on('data')
def handle_data(data):
    # decode the data base64

    # send the data to the front end
    requests.post('http://localhost:3000', data=data)

# more api endpoints per request


 
# ws://127.0.0.1:5001/socket.io/?EIO=4&transport=websocket

@socketio.on('TD event')  # Listening for the event named "my event"
def handle_my_custom_event(binaryData):  # The function that will run when the event is received
    print('received binary data:')
    # decode the data base64
    decoded_data = base64.b64decode(binaryData)
    # send the data to the front end
    requests.post('http://localhost:3000', data=decoded_data)

# async def websocket_test():
#     uri = "ws://127.0.0.1:5001/socket.io/?EIO=4&transport=websocket"
#     try:
#         async with websockets.connect(uri) as websocket:
#             await websocket.send("Hello, World")
#             response = await websocket.recv()
#             return response
#     except Exception as e:
#         return f"An error occurred: {e}"

# @app.route('/api/test_websocket', methods=['GET'])
# def test_websocket_route():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     result = loop.run_until_complete(websocket_test())
#     return result