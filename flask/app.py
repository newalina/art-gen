
# File imports
from flask import Flask
from flask import request, jsonify
import numpy as np
from pymongo import MongoClient
import requests
from flask_cors import CORS
from flask_socketio import SocketIO
from google.cloud import storage
import asyncio
import websockets
import base64

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

### User NoSQL representation ###
# User:
# {
#     "username": "string",
#     "media": ["string"]
# }

CORS(app)

API_KEY = '3x1ffNiowcASHEnfhbH7KkcylZTkRfQfytyyL4JE'

# Initialize Google Cloud Storage client
storage_client = storage.Client.from_service_account_json('gcp-key.json')
# MongoDB connection 
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]



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

# Route to connect to Google Cloud API
@app.route('/api/google-cloud', methods=['GET', 'POST'])
def google_cloud_api():
    if request.method == 'GET':
        # retrieve list of image_id from DB
        results = collection.find_one({"username": request.args.get('username')})
        return list(results['media'])

    else:
        username, file, filetype = request.args.get('username'), request.files.get('media'), requests.args.get('filetype')
        # Upload the file to Google Cloud Storage
        pub_url = gcs_upload_media(file, filetype)
        if filetype == 'video/mp4':
            # calculate thumbnail
            thumbnail = extract_first_frame(file.stream)
            # upload to gcp
            thumbnail_url = gcs_upload_media(thumbnail, filetype) # how to convert from jpg to file
            new_media = (thumbnail_url,pub_url)
        else: 
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
            
        return jsonify({'message': 'Image uploaded successfully', 'username': username}), 200
    
# function to upload file to GCS
def gcs_upload_media(file, type):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.filename.split("/")[-1])
    blob.content_type = type # example: 'image/jpeg'
    blob.upload_from_file(file.stream)
    public_url: str = blob.public_url
    return public_url

def extract_first_frame(mp4_stream):
    # Convert mp4 stream to bytes-like object
    mp4_bytes = mp4_stream.read()
    # Convert bytes-like object to numpy array
    np_array = np.frombuffer(mp4_bytes, np.uint8)
    # Decode video using OpenCV
    video_capture = cv2.VideoCapture()
    video_capture.open(np_array)
    # Check if video capture is successful
    if not video_capture.isOpened():
        raise ValueError("Error: Unable to open video stream.")
    # Read the first frame from the video
    success, frame = video_capture.read()
    # Check if frame is successfully read
    if not success:
        raise ValueError("Error: Unable to read first frame from video.")
    # Release the video capture object
    video_capture.release()
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        raise ValueError("Error: Unable to encode frame to JPEG format.")
    # Convert encoded image to bytes
    jpeg_bytes = encoded_image.tobytes()

    return jpeg_bytes



# requested parameters
# @app.route('/api/particle_cloud/forest
# @app.route('/api/particle_cloud/ocean', methods=['GET', 'POST'])
# @app.route('/api/particle_cloud/fire', methods=['GET', 'POST'])
    


# ************************************************** SOCKET FUNCTION **************************************************
    
@socketio.on('data')
def handle_data(data):
    # decode the data base64

    # send the data to the front end
    requests.post('http://localhost:3000', data=data)

# more api endpoints per request


 
# ws://127.0.0.1:5000

@socketio.on('TD event')  # Listening for the event named "my event"
def handle_my_custom_event(binaryData):  # The function that will run when the event is received
    print('received binary data:')
    # decode the data base64
    decoded_data = base64.b64decode(binaryData)
    # send the data to the front end
    requests.post('http://localhost:3000', data=decoded_data)

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