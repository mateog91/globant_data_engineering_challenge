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
    db_department = crud.department.get_by_name(
        db, name=department_in.department)
    if db_department:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Department {department_in.department} already registered")
    return crud.department.create(db=db, data_in=department_in)


@router.get("/", response_model=list[schemas.Department])
def read_departments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    departments = crud.department.get_all(db, skip=skip, limit=limit)
    return departments


@router.post("/create_departments")
def create_departments(
        list_data_in: list[schemas.DepartmentCreate],
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
            validated_data = schemas.DepartmentCreate(**data.dict())

            # check if department name already exists
            db_department = crud.department.get_by_name(
                db, name=validated_data.department)
            if db_department:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=f"Department {validated_data.department} already registered")

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
    created_data = crud.department.create_many(db=db, data=valid_data)

    return {
        "message": f"success: {len(created_data)}\n faild: {len(invalid_data)}",
        "valid data": created_data,
        "invalid data": invalid_data,
    }
