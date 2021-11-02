import os

from celery import Celery
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware

from project.channels.router import channel_router
from project.celery_utils import create_celery


def create_app():
    app = FastAPI()

    app.celery_app = create_celery()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    from project.channels import users_router                # new
    app.include_router(users_router)                      # new


    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    app.include_router(channel_router)

    return app



