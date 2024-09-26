from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

uri = "mongodb+srv://"+username+":"+password+"@python-api-developer.rylyi.mongodb.net/?retryWrites=true&w=majority&appName=Python-API-Developer"

client = MongoClient(uri)

result = client["sample_mflix"]["comments"][0]
print(result)