from fastapi import Depends, FastAPI, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session

from models.base import engine
from app.routes import jobs, departments, migration, hired_employees
import models
print("here")

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jobs.router)
app.include_router(departments.router)
app.include_router(hired_employees.router)
app.include_router(migration.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
