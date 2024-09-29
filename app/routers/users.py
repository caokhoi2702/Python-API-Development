from fastapi import Response, status, HTTPException, APIRouter
from fastapi.params import Body
from bson.objectid import ObjectId
from .. import models, database, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/",
        response_description="Get all users",
        response_model=models.UserCollection,
        response_model_by_alias=False)
def get_posts():
    return models.UserCollection(users=database.user_collection.find().to_list(1000))

@router.post("/", 
        response_description="Add new user",
        response_model=models.UserOut,
        status_code=status.HTTP_201_CREATED,
        response_model_by_alias=False)
def create_post(user: models.CreateUser = Body(...)):
    # Hash the password - user.password
    user.password = utils.hash(user.password)

    new_user = database.user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )

    created_user = database.user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.get("/{id}",
        response_description="Get one user",
        response_model=models.UserOut,
        response_model_by_alias=False)
def get_post(id: str):
    try:
        got_user = database.user_collection.find_one(
            {"_id": ObjectId(id)}
        )
        if not got_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'user with id: {id} was not found')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(error))
    
    return got_user