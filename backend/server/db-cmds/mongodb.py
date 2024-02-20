from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Accessing variables
database_url = os.getenv('DATABASE_URL')\
    #= "mongodb+srv://<username>:<password>@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority"
secret_key = os.getenv('SECRET_KEY')
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
