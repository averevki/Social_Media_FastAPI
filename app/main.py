"""Social media API

API that allow users to exchange posts on
social media simulation

Using: FastAPI framework,
PostgreSQl database, SQLAlchemy ORM, alembic as database migration tool,
OAuth2 and JWN tokens for users authentication.

Application is dockerized and deployed on heroku
link: social-media-api-verevkin.herokuapp.com/

Each query provided with pytest tests

Application is automized for CI/CD workflow with GitHub actions
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import posts, users, auth, ratings

__author__ = "Aleksandr Verevkin"
__license__ = "GNU GPL v.3"
__status__ = "maintenance"
__maintainer__ = "Aleksandr Verevkin"

# Base.metadata.create_all(bind=engine)     # manual creation of databases

# API instance
app = FastAPI()
# CORS setup
origins = ["*"]     # list of allowed origins (["*"] - all)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# declare routers for queries forwarding
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router,  tags=["Users"])
app.include_router(ratings.router, prefix="/rate", tags=["Ratings"])


@app.get("/", tags=["General"])
def home_page() -> dict:
    """Root page"""
    return {"message": "Hello there :) Available queries -> /posts /users /rate"}
