from fastapi import FastAPI

app = FastAPI()


@app.post("/")
async def index():
    return {"message": "Hello World"}
