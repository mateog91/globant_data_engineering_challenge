from fastapi import Depends, FastAPI, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine
from app.routes import jobs, departments

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jobs.router)
app.include_router(departments.router)



@app.get("/")
async def root():
    return {"message": "Hello World"}


