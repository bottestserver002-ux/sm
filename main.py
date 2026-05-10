from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers.auth_router import router as auth_router
from routers.poems_router import router as poems_router
from routers.posts_router import router as posts_router
from routers.ai_router import router as ai_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(poems_router)
app.include_router(posts_router)
app.include_router(ai_router)