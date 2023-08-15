#!/usr/bin/python3
""" module of migration endpoints """

from datetime import datetime
from enum import Enum
from typing import Annotated
from sqlalchemy.orm import Session
import csv

from app.dependencies import get_db
import crud
import schemas
import models

from fastapi import APIRouter, routing, status, HTTPException, Depends
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

import aiofiles

router = APIRouter(
    prefix="/migrate",
    tags=["migration"]
)



class FileType(str, Enum):
    job = "job"
    department = "department"
    hired_employee = "hired_employee"
    
csv_schema = {
    "job": list(models.Job.__table__.columns.keys()),
    "department": list(models.Department.__table__.columns.keys()),
    "hired_employee": list(models.Hired_Employee.__table__.columns.keys())
}

class CsvSchema:
    job: list(models.Job.__table__.columns.keys())
    department: list(models.Department.__table__.columns.keys())
    hired_employee: list(models.Hired_Employee.__table__.columns.keys())
    
csv_schema = CsvSchema()


@router.post("/uploadfile/")
async def create_upload_file(file_type: FileType, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    # out_file_name = f"/file_storage/{file_type}/{datetime.now()}_{file.filename}"
    out_file_name = f"/file_storage/{file_type}/{file_type}.csv"
    async with aiofiles.open(out_file_name, mode='wb') as out_f:
        content = await file.read()
        await out_f.write(content)
    return {"filename": file.filename}


@router.post("/upload_to_db")
async def upload_to_db(db: Session = Depends(get_db)):
    from models.job import Job as modeljob
    # for t in FileType:
    #     read_file_path = f"/file_storage/{t}/{t}.csv"
    lst = modeljob.__table__.columns.keys()
    # print(lst)

    t = "job"
    read_file_path = f"/file_storage/{t}/{t}.csv"
    async with aiofiles.open(read_file_path, mode='r') as f:
        content = await f.readlines()
    csv_reader = csv.DictReader(content, fieldnames=lst, delimiter=',')
    data_list = list(csv_reader)
    
    result = crud.job.create_many(db=db, data=data_list)
    # for e in csv_reader:
    #     print(e)

    return {"message": f"{len(result)} created"}

    # if file_type == FileType.job:
    #     crud.job.create_many() (db, file_type)
    # elif file_type == FileType.department:
    #     crud.create_departments_from_csv(db, file_type)
    # elif file_type == FileType.hired_employee:
    #     crud.create_hired_employees_from_csv(db, file_type)
    # else:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="File type not recognized"
    #     )
    # return {"status": "success"}


async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Read the uploaded CSV file
    content = await file.read()

    # Decode the content and split lines
    decoded_content = content.decode("utf-8")
    csv_reader = csv.DictReader(decoded_content.splitlines(), delimiter=',')

    employees_to_create = []

    # Convert CSV data to HiredEmployeeCreate instances
    for row in csv_reader:
        employee_data = {
            "name": row.get("name"),
            "datetime": row.get("datetime"),
            "department_id": int(row.get("department_id")),
            "job_id": int(row.get("job_id"))
        }
        employees_to_create.append(employee_data)

    # Create instances of HiredEmployeeCreate
    hired_employees = [schemas.HiredEmployeeCreate(
        **data) for data in employees_to_create]

    # Insert the data into the database
    created_employees = crud.hired_employee.create_many(
        db=db, data=hired_employees)

    return {"message": f"{len(created_employees)} employees created"}

# Other routes and app configurations
