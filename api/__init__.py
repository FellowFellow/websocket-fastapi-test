import sys
from pathlib import Path
from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse

sys.path.append(".")

app = FastAPI()


from api.websocket.router import router
from api.websocket.helper import handle_websocket

app.include_router(router)


@app.get("/")
async def index():
    return FileResponse(Path(
        "/Users/ben/dev/meine/websocket-fastapi-test/index.html"
    ))

@app.websocket("/ws")
async def websocket_endpoint(
    socket: WebSocket
):
  await handle_websocket(socket)  

import os
os.system("clear")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("api:app", reload=True, reload_dirs="api")

