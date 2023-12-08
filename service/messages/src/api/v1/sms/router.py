import json

from core.authorization import (
    get_user_from_access_token,
    get_user_from_header_access_token,
)
from core.http_exceptions import NotAuthenticated
from core.users import SimpleUserAuth
from fastapi import APIRouter, Body, Depends, Query, WebSocket, WebSocketDisconnect

from .manager import manager

router = APIRouter(prefix='/sms')


@router.get('/send')
async def send_message(
    user_id: str = Query(),
    message_dict: dict = Body(),
    user_auth: SimpleUserAuth = Depends(get_user_from_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated

    message = json.dumps(message_dict)
    await manager.send_personal_message(message, user_id)


@router.websocket('/ws')
async def websocket_endpoint(
    websocket: WebSocket,
    user_auth: SimpleUserAuth = Depends(get_user_from_header_access_token),
):
    if not user_auth.is_authenticated:
        raise NotAuthenticated

    await manager.connect(user_auth.user_payload.user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f'Message text was: {data}')
    except WebSocketDisconnect:
        manager.disconnect(user_auth.user_payload.user_id)


@router.websocket('/ws_test')
async def websocket_endpoint2(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f'Message text was: {data}')
