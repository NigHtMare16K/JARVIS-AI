from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, chat, voice, assistant
from app.core.config import settings

app = FastAPI(title="Jarvis")

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Transcribed-Text", "X-Answer-Text"],
)

app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(voice.router)
app.include_router(assistant.router)


@app.get("/")
def welcome():
    return {"message": "Hello I am Jarvis"}
