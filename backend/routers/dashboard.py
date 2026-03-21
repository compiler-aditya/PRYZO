"""WebSocket endpoint for live hunt dashboard updates."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from routers.hunt import register_ws, unregister_ws

router = APIRouter()


@router.websocket("/ws/dashboard/{session_id}")
async def dashboard_ws(ws: WebSocket, session_id: str):
    await ws.accept()
    register_ws(session_id, ws)
    try:
        while True:
            # Keep connection alive; client sends pings
            await ws.receive_text()
    except WebSocketDisconnect:
        unregister_ws(session_id, ws)
