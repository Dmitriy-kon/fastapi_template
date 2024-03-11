import secrets
import os

import redis.asyncio as aioredis

#
# client = aioredis.from_url("redis://localhost:6379", encoding="utf8", decode_responses=True)
exp_time = os.getenv("EXPIRE_TIME")


class SessionHandler:
    def __init__(self) -> None:
        self.client = aioredis.from_url(
            "redis://redisdb", encoding="utf8", decode_responses=True
        )

    async def create_session(self, user_name: str):
        session_id = secrets.token_hex(16)
        self.client.set(session_id, user_name, ex=exp_time)

    async def get_session(self, session_id: str) -> str | None:
        return self.client.get(session_id)

    async def delete_session(self, session_id: str):
        self.client.delete(session_id)
