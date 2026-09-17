from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.postgres import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/i/u")
def upload_image():
    pass


@app.get("/i/v")
def view_image_page(id: str):
    pass


@app.get("/i/r")
def view_raw_image(id: str):
    pass
