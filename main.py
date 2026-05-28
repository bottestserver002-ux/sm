from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import Base, engine

from routers.auth_router import router as auth_router
from routers.poems_router import router as poems_router
from routers.posts_router import router as posts_router
from routers.ai_router import router as ai_router
from routers.minigame_router import router as minigame_router

import os


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(
    "uploads",
    exist_ok=True
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)

app.include_router(auth_router)
app.include_router(poems_router)
app.include_router(posts_router)
app.include_router(ai_router)
app.include_router(minigame_router)