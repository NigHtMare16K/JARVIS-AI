from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def welcome():
    return "Heloo I am Jarvis"