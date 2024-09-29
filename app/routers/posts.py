from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Body
from bson.objectid import ObjectId
from .. import models, database

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/",
        response_description="Get all posts",
        response_model=models.PostCollection,
        response_model_by_alias=False)
def get_posts():
    return models.PostCollection(posts=database.post_collection.find().to_list(1000))

@router.get("/{id}",
        response_description="Get one post",
        response_model=models.Post,
        response_model_by_alias=False)
def get_post(id: str):
    try:
        got_post = database.post_collection.find_one(
            {"_id": ObjectId(id)}
        )
        if not got_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    
    return got_post

@router.post("/", 
        response_description="Add new post",
        response_model=models.Post,
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False)
def create_post(post: models.Post = Body(...)):
    new_post = database.post_collection.insert_one(
        post.model_dump(by_alias=True, exclude=["id"])
    )
    created_post = database.post_collection.find_one(
        {"_id": new_post.inserted_id}
    )
    return created_post

@router.delete("/{id}", 
        response_description="Delete one post",
        status_code=status.HTTP_204_NO_CONTENT,
        response_model_by_alias=False)
def delete_posts(id: str):
    try:
        deleted_post = database.post_collection.delete_one(
            {"_id": ObjectId(id)}
        )
        if not deleted_post.deleted_count :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",
        response_description="Update one post",
        response_model=models.Post,
        response_model_by_alias=False)
def update_post(id: str, post: models.UpdatePost):
    update_operation = { '$set' : 
        dict(post)
    }
    try:
        update_post = database.post_collection.update_one({'_id': ObjectId(id)}, update_operation)
        if not update_post.modified_count :
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'post with id: {id} was not found')
        
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    updated_post = database.post_collection.find_one(
        {"_id": ObjectId(id)}
    )
    return updated_post