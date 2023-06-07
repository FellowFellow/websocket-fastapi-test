import asyncio
from fastapi import WebSocket, WebSocketDisconnect


all_channels: set[str] = set()
sockets_index: dict[int, tuple[WebSocket, set[str]]] = dict()

async def advertise_channel(channel: str, socket: WebSocket, delete: bool = False):
    data = {
        "t": "del" if delete else "new",
        "id": channel
    }
    await socket.send_json(data)


async def broadcast_advertise_channel(channel: str, delete: bool = False) -> None:
    await asyncio.gather(
        *[
            advertise_channel(channel, socket, delete)
            for socket, _ in sockets_index.values()
        ]
    )


async def handle_websocket(socket: WebSocket):
    await socket.accept()
    
    sock_id: int = id(socket)
    subscriptions = set()
    sockets_index[sock_id] = (socket, subscriptions)
    
    
    await asyncio.gather(
        *[advertise_channel(channel, socket, False) for channel in all_channels]
    )
    
    # TODO: periodic channel update -> 
    # dashboard - a update every 10 seconds is required how to do this?
    # pending docs - beat task every 5 seconds trigger a endpoint to update the channel
    
    # what do we need?
    # wait for client to sub or pop subscription
    # at the same time every x seconds run function 
    
    while True:
        try:
            msg = await socket.receive_text()
        
        except WebSocketDisconnect:
            del sockets_index[sock_id]
            break

        verb = msg[:3]
        print(verb)
        if verb == "sub":
            channel = msg[3:]
            if channel in all_channels:
                subscriptions.add(channel)
        elif verb == "pop":
            subscriptions.discard(msg[3:])
