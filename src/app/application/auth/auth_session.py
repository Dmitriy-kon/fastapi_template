from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.adapters.redisDb.redis_gateway import session_handler



security = HTTPBasic()


async def auth_required_from_session(
    request: Request,
):
    session_id = request.cookies.get("session_id")
    
    if session_id is None or await session_handler.get_session(session_id) is None:
        raise HTTPException(status_code=401, detail="Invalid session id. Please login again")
    
    
