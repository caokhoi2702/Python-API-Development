from pydantic import BaseModel, Field, BeforeValidator, EmailStr, ConfigDict
from typing import Annotated, Optional

PyObjectId = Annotated[str, BeforeValidator(str)]

class Post(BaseModel):
    """
    Container for a single post record.
    """

    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(...)
    content: str = Field(...)

class UpdatePost(BaseModel):
    """
    A set of optional updates to be made to a post in the database.
    """

    title: Optional[str] = None
    content: Optional[str] = None

class PostCollection(BaseModel):
    """
    A container holding a list of `Post` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    posts: list[Post]