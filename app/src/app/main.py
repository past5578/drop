import os

import psycopg
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
DATABASE_PASSWORD = os.environ["DATABASE_PASSWORD"]

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
