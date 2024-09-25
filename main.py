from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/POSTS")
def get_posts():
    return {"data": "This is your posts"}