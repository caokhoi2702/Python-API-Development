from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from bson.json_util import dumps
from .config import settings
from dotenv import load_dotenv
import os

# Initialize FastAPI
app = FastAPI()

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

class Post(BaseModel):
    title: str
    content: str

# my_posts = [
#     {
#         "id": 1,
#         "title": "title of book 1",
#         "content": "content of book 1"
#     },
#     {
#         "id": 2,
#         "title": "favorite foods",
#         "content": "I like pizza"
#     }
# ]

# def find_post(id):
#     for item in my_posts:
#         if id == item["id"]:
#             return item
        
# def find_index_post(id):
#     for idx, item in enumerate(my_posts):
#         if id == item["id"]:
#             return idx

# request Get method url: "/"
@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    get_posts = client["main_db"]["Posts"].find({})
    posts = []
    for document in get_posts:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return {"Data": posts}

@app.get("/posts/{id}")
def get_post(id: str):
    post = client["main_db"]["Posts"].find_one(ObjectId(id))

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    post["_id"] = str(post["_id"])
    return {"data": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    client["main_db"]["Posts"].insert_one(dict(post))
    get_posts = client["main_db"]["Posts"].find({})
    posts = []
    for document in get_posts:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return {"Data": posts}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: str):
    client["main_db"]["Posts"].delete_one({"_id": ObjectId(id)})
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: str, post: Post):
    update_operation = { '$set' : 
        dict(post)
    }
    update_post = client["main_db"]["Posts"].update_one({'_id': ObjectId(id)}, update_operation)
    if (update_post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    post = client["main_db"]["Posts"].find_one(ObjectId(id))
    post["_id"] = str(post["_id"])
    return {"Data": post}