from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBasic
from app.adapters.redisDb.redis_gateway import SessionRedisHandler

from app.api.depends_stub import Stub


security = HTTPBasic()


async def auth_required_from_session(
    request: Request,
    session_handler: Annotated[SessionRedisHandler, Depends(Stub(SessionRedisHandler))],
):
    session_id = request.cookies.get("session_id")

    if session_id is None or await session_handler.get_session(session_id) is None:
        raise HTTPException(
            status_code=401, detail="Invalid session id. Please login again"
        )
