from fastapi import APIRouter

index_router = APIRouter()

@index_router.get("/")
async def main_page():
    return {"message": "Hello World"}