#!/usr/bin/python3
""" module of department endpoints """
from datetime import datetime, timezone
from math import e
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix="/hired_employees",
    tags=["hired_employees"]
)


@router.post("/", response_model=schemas.HiredEmployee)
def create_hired_employee(hired_employee_in: schemas.HiredEmployeeCreate, db: Session = Depends(get_db)):
    """
    Create a hired employee"""

    return crud.hired_employee.create(db=db, data_in=hired_employee_in)


@router.get("/", response_model=list[schemas.HiredEmployee])
def read_hired_employees(
    skip: int = 0,
    limit: int = 100, db: Session = Depends(get_db)
):
    """
    Get all hired employees"""
    hired_employees = crud.hired_employee.get_all(db, skip=skip, limit=limit)
    return hired_employees


@router.post("/create_employees")
def create_hired_employees(
        list_data_in: list[schemas.HiredEmployeeCreate],
        db: Session = Depends(get_db)
):
    """
    Create hired employees from a list of json objects
    """
    # create lists to store valid and invalid data
    valid_data = []
    invalid_data = []

    # validate data
    for data in list_data_in:
        try:
            # check if input data is correct schema/type
            validated_data = schemas.HiredEmployeeCreate(**data.dict())
        except Exception as e:
            invalid_data.append({"data": data, "error": str(e)})
            continue
        # check if department exists
        if validated_data.department_id is not None:

            department_db = crud.department.get(
                db, id=validated_data.department_id)

            # check if job's and department's id's exist
            if not department_db:
                invalid_data.append(
                    {"data": data, "error": f"Department {validated_data.department_id} does not exist"})
                continue

        if validated_data.job_id is not None:
            job_db = crud.job.get(db, id=validated_data.job_id)
            if not job_db:
                invalid_data.append(
                    {"data": data, "error": f"Job {validated_data.job_id} does not exist"})
                continue

        valid_data.append(validated_data)

    # create valid data
    created_data = crud.hired_employee.create_many(db=db, data=valid_data)

    return {
        "message": f"success: {len(created_data)}, faild: {len(invalid_data)}",
        "valid data": created_data,
        "invalid data": invalid_data,
    }
