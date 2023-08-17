#!/usr/bin/python3
""" module of department endpoints """

from math import e
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.hired_employee import HiredEmployeeCreate

from app.dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix="/hired_employees",
    tags=["hired_employees"]
)


@router.post("/", response_model=schemas.HiredEmployee)
def create_hired_employee(department_in: schemas.HiredEmployeeCreate, db: Session = Depends(get_db)):

    return crud.hired_employee.create(db=db, data_in=department_in)


@router.get("/", response_model=list[schemas.HiredEmployee])
def read_hired_employees(
    skip: int = 0,
    limit: int = 100, db: Session = Depends(get_db)
):
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
    valid_data = []
    invalid_data = []

    for data in list_data_in:
        try:
            validated_data = HiredEmployeeCreate(**data.dict())

            valid_data.append(validated_data)
        except Exception as e:
            error_data = {"data": data, "error": str(e)}
            invalid_data.append(error_data)

    print("it validated schema")
    created_data = crud.hired_employee.create_many(db=db, data=valid_data)

    return {
        "message": f"success: {len(created_data)}\n faild: {len(invalid_data)}",
        "valid data": created_data,
        "invalid data": invalid_data,
    }
