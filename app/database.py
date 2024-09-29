from .config import settings
from pymongo.mongo_client import MongoClient


# Get config from .env
username = settings.API_USERNAME
password = settings.API_PASSWORD
uri = "mongodb+srv://"+username+":"+password+"@python-api-developer.rylyi.mongodb.net/?retryWrites=true&w=majority&appName=Python-API-Developer"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

database = client["main_db"]
post_collection = database["Posts"]
user_collection = database["Users"]
