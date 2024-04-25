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
from moviepy.editor import VideoFileClip
from PIL import Image

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
        username, source, isVideo, timestamp = request.args.get('username'), request.args.get('source'), bool(request.args.get('isVideo')), int(request.args.get('timestamp')) # isVideo: Bool, username: Str, source: Str, timeStamp: int
        
        # define video and thumbnail files
        video_output_filename, thumbnail_output_filename  = "trimmed_video.mp4","thumbnail.jpg"        
        
        # trim video
        trim_video(source,timestamp,10,video_output_filename)
        
        # Upload the trimmed video file to Google Cloud Storage
        video_url = gcs_upload_media(video_output_filename, 'video/mp4')

        # generate thumbnail
        generate_thumbnail(source,thumbnail_output_filename,timestamp)

        # Upload the trimmed video file to Google Cloud Storage
        thumbnail_url = gcs_upload_media(thumbnail_output_filename, 'image/jpg')

        # Format MongoDB output
        new_media = (thumbnail_url,video_url,isVideo) # (thumbnail, video, is_video)

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
    
"""
Uploads a media file to Google Cloud Storage and returns its public URL.

Parameters:
    file (str): The path to the file to be uploaded.
    type (str): The content type of the file (e.g., 'image/jpeg').

Returns:
    str: The public URL of the uploaded file.
"""
def gcs_upload_media(file, type):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.split("/")[-1])
    blob.content_type = type 
    blob.upload_from_filename(file)
    public_url: str = blob.public_url
    return public_url

"""
Trim a video from the specified start time to the end time and save it to the output path.

Parameters:
    input_file (str): The path to the input video file.
    start_time (float): The start time in seconds for trimming the video.
    duration (float): The duration in seconds for trimming the video.
    output_file (str): The path to save the trimmed video.

    Returns:
        None
"""
def trim_video(input_file, start_time, duration, output_file):
    # Load the video clip
    video_clip = VideoFileClip(input_file)

    # Trim the video to the specified duration
    trimmed_clip = video_clip.subclip(start_time, start_time + duration)

    # Save the trimmed video
    trimmed_clip.write_videofile(output_file)


"""
Generate a thumbnail image for a video at the specified time.

Parameters:
    video_path (str): The path to the input video file.
    output_path (str): The path to save the generated thumbnail image.
    time (float): The time in seconds at which to capture the thumbnail.

Returns:
    None
"""
def generate_thumbnail(video_path, output_path, time):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Capture a frame at the specified time
    thumbnail = video_clip.get_frame(time)

    # Convert frame (numpy array) to image
    thumbnail = Image.fromarray(thumbnail)

    # Save the thumbnail image
    thumbnail.save(output_path)

    # Close the video clip
    video_clip.close()

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