from fastapi import FastAPI
from sqlmodel import SQLModel
from db import engine
from routes.requests import router as requests_router
from routes.codes import router as codes_router
from enums import router as enums_router
#import models 

app = FastAPI()

SQLModel.metadata.create_all(engine)

app.include_router(requests_router)
app.include_router(codes_router)
app.include_router(enums_router)