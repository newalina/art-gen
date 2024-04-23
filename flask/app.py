# File imports
import base64
import json
import requests
import websockets
from flask_cors import CORS
from flask_socketio import SocketIO
from google.cloud import storage
from pymongo import MongoClient
from flask import Flask, jsonify, request

# ********************************************************* INIT SERVER **************************************************
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
socketio = SocketIO(app, logger=True)
socketio.run(app, host='127.0.0.1', port=5001)
CORS(app)


# ********************************************************* API DATA INIT **************************************************
environmental_apis = {
    'Carbon Dioxide' : 'https://global-warming.org/api/co2-api',
    'Methane' : 'https://global-warming.org/api/methane-api',
    'Nitrous Oxide' : 'https://global-warming.org/api/nitrous-oxide-api',
    'Ocean Temperature' : 'https://global-warming.org/api/ocean-warming-api'
}

def format_data(data_name, data):
        out = []
        if data_name == 'Ocean Temperature':
            result = data['result']
            for key, value in result.items():
                out.append(float(value))
        else:
            if data_name == 'Carbon Dioxide':
                key = 'co2'
            elif data_name == 'Methane':
                key = 'methane'
            elif data_name == 'Nitrous Oxide':
                key = 'nitrous'
            result = data[key]
            for dict in result:
                out.append(float(dict['trend']))
        return out  

# load environmental data
def load_api_data(apis, output_file):
    # Dictionary to store data from each API
    api_data = {}

    # Loop through each API URL
    for api_name, api_url in apis.items():
        try:
            # Make GET request to API
            response = requests.get(api_url)
            data = response.json()  # Extract JSON data from response
            data = format_data(api_name, data)
            # Store data in dictionary with URL as key
            api_data[api_name] = data
        except Exception as e:
            print(f"Failed to fetch data from {api_url}: {e}")

    # Write API data to JSON file
    with open(output_file, 'w') as f:
        json.dump(api_data, f, indent=4)

load_api_data(environmental_apis,'daily_data.json')  

# ********************************************************* DATABASE ROUTER **************************************************

# Initialize Google Cloud Storage client
storage_client = storage.Client.from_service_account_json('gcp-key.json')
# MongoDB connection 
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]
      

# Route to connect to Google Cloud API
@app.route('/api/google-cloud', methods=['GET', 'POST'])
def google_cloud_api():
    if request.method == 'GET':
        # retrieve list of image_id from DB
        results = collection.find_one({"username": request.args.get('username')})
        return list(results['media'])

    else:
        username, file, filetype = request.args.get('username'), request.files.get('media'), request.args.get('filetype') # edit request to include thumbnail and video
        # Upload the file to Google Cloud Storage
        pub_url = gcs_upload_media(file, filetype)
        new_media = (pub_url,pub_url)

        # check if user exists in db
        user = collection.find_one({'username': username})
        if user is not None:
            # Update user's media field
            collection.update_one({"username": username}, {"$push": {"media": new_media}})

        else:
            # Add new user to the db
            user = {'username': username, 'media': [new_media]}
            collection.insert_one(user)
            
        return jsonify({'message': 'Media uploaded successfully', 'username': username}), 200
    
# function to upload file to GCS
def gcs_upload_media(file : str, type):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.filename.split("/")[-1])
    blob.content_type = type # example: 'image/jpeg'
    blob.upload_from_file(file.stream)
    public_url: str = blob.public_url
    return public_url



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