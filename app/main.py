from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()
username = os.getenv("API_USERNAME")
password = os.getenv("API_PASSWORD")

uri = "mongodb+srv://"+username+":"+password+"@python-api-developer.rylyi.mongodb.net/?retryWrites=true&w=majority&appName=Python-API-Developer"

# Create a new client and connect to the server
client = MongoClient(uri)
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

my_posts = [
    {
        "id": 1,
        "title": "title of book 1",
        "content": "content of book 1"
    },
    {
        "id": 2,
        "title": "favorite foods",
        "content": "I like pizza"
    }
]

def find_post(id):
    for item in my_posts:
        if id == item["id"]:
            return item
        
def find_index_post(id):
    for idx, item in enumerate(my_posts):
        if id == item["id"]:
            return idx

# request Get method url: "/"

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/create_posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    my_posts.append(post)
    return {"data": my_posts}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} was not found')
    return {"data": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int):
    idx = find_index_post(id)
    if (idx == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    my_posts.pop(idx)
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # deleting post

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    idx = find_index_post(id)
    if (idx == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post with id: {id} does not exist')
    post_dict = post.dict()

    my_posts[idx] = post_dict
    my_posts[idx]['id'] = id

    return {"data": post_dict}