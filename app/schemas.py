from pydantic import BaseModel, Field

class Post(BaseModel):
    title: str = Field(alias="_id")
    content: str = Field()