import asyncio
from fastapi import APIRouter
import sys
sys.path.append(".")

from fastapi.responses import JSONResponse

from api.websocket.helper import all_channels, sockets_index
from api.websocket.helper import advertise_channel, broadcast_advertise_channel

router = APIRouter()


@router.get("/new")
async def new_channel(
    channel: str
):
    if channel in all_channels:
        return JSONResponse({
            'success': False, 
            'message': 'channel allready exsists'
            },
            status_code=400
        )
    
    all_channels.add(channel)
    await broadcast_advertise_channel(channel, False)
    
    print(all_channels)
    return JSONResponse({
        'success': True
    }) 

@router.get("/delete")
async def delete_channel(
    channel: str
):
    if channel not in all_channels:
        return JSONResponse({
            'success': False, 
            'message': 'channel doesn\'t exsist'
            },
            status_code=400
        )
        
    all_channels.discard(channel)
    for socket, subscriptions in sockets_index.values():
        # notify all clients that channel will be closed
        await advertise_channel(channel, socket, True)
        # close channel
        subscriptions.discard(channel)
        
    return JSONResponse({
        'success': True
    }) 
    
@router.post("/push/{channel}")
async def push_to_channel(
    channel: str,
    message: dict[str, str | dict | None]
):
    if channel not in all_channels:
        return JSONResponse({
            'success': False, 
            'message': 'channel doesn\'t exsist'
            },
            status_code=400
        )
    
    await asyncio.gather(
        *[
            socket.send_json(
                {"t": "msg", 
                 "id": channel, 
                 "msg": message
                }
            ) for socket, subscriptions in sockets_index.values() if channel in subscriptions
        ]
    )
    
    
    

