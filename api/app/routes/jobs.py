#!/usr/bin/python3
""" module of job endpoints """

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
import schemas
import crud

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)


@router.post("/", response_model=schemas.Job)
def create_job(job_in: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = crud.job.get_by_name(db, name=job_in.job)
    if db_job:
        raise HTTPException(
            status_code=400, detail=f"Job name {job_in.job} already registered")
    return crud.job.create(db=db, data_in=job_in)


@router.get("/", response_model=list[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    jobs = crud.job.get_all(db, skip=skip, limit=limit)
    return jobs


@router.get("/hired_employees/{job_id}", response_model=list[schemas.HiredEmployee])
def get_hired_employees_by_job(job_id: int, db: Session = Depends(get_db)):
    db_job = crud.job.get(db, job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    hired_employees_list = db_job.hired_employees
    return hired_employees_list

@router.post("/create_jobs")
def create_jobs(
        list_data_in: list[schemas.JobCreate],
        db: Session = Depends(get_db)
):
    """
    Create jobs from a list of json objects
    """
    # create lists to store valid and invalid data
    valid_data = []
    invalid_data = []

    # validate data
    for data in list_data_in:
        try:
            # check if input data is correct schema/type
            validated_data = schemas.JobCreate(**data.dict())

            # check if job name already exists
            db_job = crud.job.get_by_name(
                db, name=validated_data.job)
            if db_job:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"job {validated_data.job} already registered")

            valid_data.append(validated_data)
        except HTTPException as http_exception:
            # if data is not valid, add it to invalid_data list with respective error
            error_data = {"data": data, "error": str(http_exception.detail)}
            invalid_data.append(error_data)
        except Exception as e:
            # if data is not valid, add it to invalid_data list with respective error
            error_data = {"data": data, "error": str(e)}
            invalid_data.append(error_data)

    # create valid data
    created_data = crud.job.create_many(db=db, data=valid_data)

    return {
        "message": f"success: {len(created_data)}\n faild: {len(invalid_data)}",
        "valid data": created_data,
        "invalid data": invalid_data,
    }