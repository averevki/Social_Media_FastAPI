"""Social media API

Using: FastAPI framework,
ProgreSQl database, SQLAlchemy ORM

API that allow users to exchange posts on
social media simulation
"""

from fastapi import FastAPI

from .database import Base, engine
from .routers import posts, users, auth, ratings

__author__ = "Aleksandr Verevkin"
__license__ = "GNU GPL v.3"
__status__ = "production"
__maintainer__ = "Aleksandr Verevkin"

# Base.metadata.create_all(bind=engine)     # manual creation of databases

# API instance
app = FastAPI()

# declare routers for queries forwarding
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router,  tags=["Users"])
app.include_router(ratings.router, prefix="/rate", tags=["Ratings"])


@app.get("/")
def home_page():
    """Root page"""
    return {"message": "Hi :)"}
