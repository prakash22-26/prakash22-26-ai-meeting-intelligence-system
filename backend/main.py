from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

from routers.meetings import router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(
    router,
    prefix="/api"
)

@app.get("/")
def home():
    return {
        "message": "API Running"
    }
