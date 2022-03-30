"""Social media API

Using: FastAPI, Progresql database

API that allow users to exchange posts on
social media simulation
"""
# TODO documentation

from time import sleep

from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor

from .database import Base, engine, load_dotenv, getenv
from .routers import posts, users, auth

load_dotenv()

__author__ = "Aleksandr Verevkin"
__license__ = "GNU GPL v.3"
__status__ = "production"
__maintainer__ = "Aleksandr Verevkin"

Base.metadata.create_all(bind=engine)
# API instance
app = FastAPI()

# connection to database
while True:
    try:
        conn = psycopg2.connect(host=getenv("HOST"),
                                database=getenv("DB_USER"),
                                user=getenv("DB_USER"), password=getenv("DB_PASSWORD"),
                                cursor_factory=RealDictCursor)
        cur = conn.cursor()
        print("Successful database connection")
        break
    except Exception as e:
        print(f"Database connection failed.\nError: {e}")
        sleep(2)
        print("Trying again...")

# declare routers for queries forwarding
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router,  tags=["Users"])


@app.get("/")
def home_page():
    return {"message": "Hi :)"}
