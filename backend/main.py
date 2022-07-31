"""
To run the code, write in the terminal:
uvicorn main:app --reload
"""
from fastapi import FastAPI, WebSocket

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.websocket("/ws")
async def ws_end(ws: WebSocket, route):
    await ws.accept()
    match route:
        case 1:
            while True:
                data = await ws.receive_json()
                
                