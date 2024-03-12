import secrets
import os

import redis.asyncio as aioredis

#
# client = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
exp_time = os.getenv("EXPIRE_TIME")
exp_time = 4000

class SessionHandler:
    def __init__(self) -> None:
        self.client = aioredis.from_url(
            "redis://redisdb", encoding="utf8", decode_responses=True
        )

    async def create_session(self, user_name: str):
        session_id = secrets.token_hex(16)
        await self.client.set(session_id, user_name, ex=exp_time)
        return session_id

    async def get_session(self, session_id: str) -> str | None:
        credentials = await self.client.get(session_id)
        return credentials

    async def delete_session(self, session_id: str):
        await self.client.delete(session_id)

session_handler = SessionHandler()
