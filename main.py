import asyncio

from fastapi import FastAPI, APIRouter
import uvicorn

from game import validate_password

app = FastAPI()
router = APIRouter(prefix="/game", tags=["game"])
app.include_router(router)


@app.post("/game")
async def root(password: str):
    return await validate_password(password)


async def main():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
