from fastapi import FastAPI

from app.api.routes import auth,chat,voice

app = FastAPI(title="Jarvis")

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(voice.router)

@app.get('/')
def welcome():
    return {"message": "Hello I am Jarvis"}
    