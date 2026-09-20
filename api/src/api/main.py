import uuid
import warnings
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from PIL import Image

from api import config
from api.postgres import database

warnings.simplefilter("error", Image.DecompressionBombWarning)

IMAGE_PATH = config.IMAGE_PATH
THUMB_PATH = config.THUMB_PATH


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    async with database.pool.acquire() as connection, connection.transaction():
        # Make this imported instead of hardcoded
        await connection.execute(
            """
            CREATE TABLE
                IF NOT EXISTS image_metadata (
                    id uuid PRIMARY KEY,
                    extension text NOT NULL,
                    file_path text NOT NULL,
                    width integer NOT NULL,
                    height integer NOT NULL,
                    created_at timestamptz NOT NULL
                )"""
        )

    yield

    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/api/img/upload")
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

    image_filepath = IMAGE_PATH / image_filename

    image_filepath.write_bytes(content)

    async with database.pool.acquire() as connection, connection.transaction():
        await connection.execute(
            "INSERT INTO image_metadata (id, extension, file_path, width, height, created_at) VALUES ($1, $2, $3, $4, $5, $6)",
            image_id,
            image_ext,
            image_filepath.as_posix(),
            image.width,
            image.height,
            datetime.now(timezone.utc),
        )

    return {"id": image_id}


@app.get("/api/image/raw")
async def view_raw_image(id: str):
    async with database.pool.acquire() as connection, connection.transaction():
        row = await connection.fetchrow(
            "SELECT * FROM image_metadata WHERE id = $1", id
        )

    image_filepath = row["file_path"]

    if not image_filepath:
        return {"error": "image not found"}

    return FileResponse(image_filepath)
