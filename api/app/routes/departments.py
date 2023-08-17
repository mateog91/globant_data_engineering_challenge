#!/usr/bin/python3
""" module of department endpoints """

from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix="/departments",
    tags=["departments"]
)


@router.post("/", response_model=schemas.Department)
def create_department(department_in: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    db_department = crud.department.get_by_name(db, name=department_in.department)
    if db_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Department {department_in.department} already registered")
    return crud.department.create(db=db, data_in=department_in)


@router.get("/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.department.get_all(db, skip=skip, limit=limit)
    return departments
