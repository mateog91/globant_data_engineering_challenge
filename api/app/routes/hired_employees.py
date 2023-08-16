#!/usr/bin/python3
""" module of department endpoints """

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
def create_hired_employee(department_in: schemas.HiredEmployeeCreate, db: Session = Depends(get_db)):

    return crud.hired_employee.create(db=db, data=department_in)


@router.get("/", response_model=list[schemas.HiredEmployee])
def read_hired_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    hired_employees = crud.hired_employee.get_all(db, skip=skip, limit=limit)
    return hired_employees


@router.post("/add_many", response_model=list[schemas.HiredEmployee])
def create_hired_employees(data: list[schemas.HiredEmployeeCreateList], db: Session = Depends(get_db)):
    return crud.hired_employee.create_many(db=db, data=data)
