"""
To run the code, write in the terminal:
uvicorn main:app --reload
"""
from fastapi import FastAPI, WebSocket, status
from db import DatabaseHandler

app = FastAPI()
db = DatabaseHandler()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.websocket("/ws")
async def ws_end(ws: WebSocket):
    await ws.accept()
    while True:
        json = await ws.receive_json()
        if not json or not json["route"]:
            await ws.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        match json["route"]:
            case "get_user_documents":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    documents = await db.get_user_documents(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(documents)

            case "update_score":
                if not json["user_id"] or not json["score"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.update_score(json["user_id"], json["score"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "get_user":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    user = await db.get_user(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(user)

            case "get_document":
                if not json["doc_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    document = await db.get_document(json["doc_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(document)

            case "update_document":
                if not json["doc_id"] or not json["doc_name"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.update_document(json["doc_id"], json["doc_name"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "delete_document":
                if not json["doc_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.delete_document(json["doc_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "delete_user":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.delete_user(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")
            case "create_user":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.create_user(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "create_document":
                if not json["doc_name"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.create_document(json["doc_name"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "write_document":
                if not json["doc_id"] or not json["char"] or not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    await db.write_document(json["doc_id"], json["char"])
                    anum = (
                        "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                    )
                    current_char_count = await db.get_char_count(json["user_id"])
                    index = anum.index(json["char"])
                    current_char_count = current_char_count[index] - 1
                    await db.update_char_count(json["user_id"], current_char_count)
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send("Success!")

            case "read_document":
                if not json["doc_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    document = await db.read_document(json["doc_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(document)

            case "get_char_count":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    char_count = await db.get_char_count(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(char_count)

            case "get_score":
                if not json["user_id"]:
                    await ws.close(code=status.WS_1008_POLICY_VIOLATION)
                    return
                try:
                    score = await db.get_score(json["user_id"])
                except ValueError as e:
                    await ws.send(e.args[0])
                    await ws.close()
                    return
                await ws.send(score)
