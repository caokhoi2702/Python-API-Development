from fastapi import FastAPI, Response, status, HTTPException
from .routers import posts, users

# Initialize FastAPI
app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World"}


    
