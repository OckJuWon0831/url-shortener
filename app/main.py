from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models
from app.database import engine
from app.routes import home, url
from app.routes import home

app = FastAPI(
    title="URL Shortener",
    swagger_ui_parameters={"defaultModelsExpandDepth": 0},
)
models.Base.metadata.create_all(bind=engine)

app.include_router(home.router)
# app.include_router(url.router)

app.mount("/static", StaticFiles(directory="static"), name="static")
