import uuid
import warnings
from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile
from PIL import Image

from app import config
from app.postgres import database

warnings.simplefilter("error", Image.DecompressionBombWarning)

IMAGE_PATH = config.IMAGE_PATH
THUMB_PATH = config.THUMB_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/i/u")
async def upload_image(file: UploadFile):
    content = await file.read()

    if len(content) > (1024 * 1024 * 10):  # 10 mb
        return {"error": "image too large"}

    try:
        image = Image.open(file.file)
    except Image.DecompressionBombError:
        return {"error": "image too large"}

    if image.format not in ["JPEG", "PNG", "WEBP"]:
        return {"error": "image format unsupported"}

    image_id = uuid.uuid4()
    image_ext = {"JPEG": "jpg", "PNG": "png", "WEBP": "webp"}[image.format]
    image_filename = f"{image_id}.{image_ext}"

    (IMAGE_PATH / image_filename).write_bytes(content)


@app.get("/i/v")
def view_image_page(id: str):
    pass


@app.get("/i/r")
def view_raw_image(id: str):
    pass
