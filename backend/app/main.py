from fastapi import FastAPI

from app.api.routes import auth

app = FastAPI(title="Jarvis")

app.include_router(auth.router)

@app.get('/')
def welcome():
    return {"message": "Hello I am Jarvis"}