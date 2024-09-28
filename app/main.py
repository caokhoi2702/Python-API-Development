from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from . import models
from .database import client, database, post_collection

# Initialize FastAPI
app = FastAPI()

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
    get_posts = post_collection.find({})
    posts = []
    for document in get_posts:
        document["_id"] = str(document["_id"])
        posts.append(document)
    return {"Data": posts}

@app.get("/posts/{id}")
def get_post(id: str):
    try:
        post = client["main_db"]["Posts"].find_one(ObjectId(id))
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    
    post["_id"] = str(post["_id"])
    return {"data": post}

@app.post("/posts", 
          response_description="Add new post",
          response_model=models.Post,
          status_code=status.HTTP_201_CREATED,
          response_model_by_alias=False)
def create_post(post: models.Post = Body(...)):
    new_post = post_collection.insert_one(
        post.model_dump(by_alias=True, exclude=["id"])
    )
    created_post = post_collection.find_one(
        {"_id": new_post.inserted_id}
    )
    return created_post

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: str):
    try:
        delete_post = client["main_db"]["Posts"].delete_one({"_id": ObjectId(id)})
        if not delete_post.deleted_count :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: str, post: models.Post):
    update_operation = { '$set' : 
        dict(post)
    }
    try:
        update_post = client["main_db"]["Posts"].update_one({'_id': ObjectId(id)}, update_operation)
        if not update_post.modified_count :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
        
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))

    post = client["main_db"]["Posts"].find_one(ObjectId(id))
    post["_id"] = str(post["_id"])
    return {"Data": post}
    
    