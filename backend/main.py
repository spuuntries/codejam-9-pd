"""
To run the code, write in the terminal:
uvicorn main:app --reload
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

