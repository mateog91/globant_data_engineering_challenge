#!/usr/bin/python3
""" module of job endpoints """

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app import crud_old
from app.dependencies import get_db
import schemas

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.post("/", response_model=schemas.Job)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = crud_old.get_job_by_name(db, name=job.job)
    if db_job:
        raise HTTPException(status_code=400, detail="Job already registered")
    return crud_old.create_job(db=db, job=job)

@router.get("/", response_model=list[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud_old.get_jobs(db, skip=skip, limit=limit)
    return jobs