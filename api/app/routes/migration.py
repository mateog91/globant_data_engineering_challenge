#!/usr/bin/python3
""" module of migration endpoints """

from dataclasses import field
from datetime import datetime
from enum import Enum
from typing import Annotated
from sqlalchemy.orm import Session
import csv
import time

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



ft_attributes = {
    "job": {
        "fieldnames": list(models.Job.__table__.columns.keys()),
        "write_function": crud.job.create_many,
        "read_function": crud.job.get_all
    },
    "department": {
        "fieldnames": list(models.Department.__table__.columns.keys()),
        "write_function": crud.department.create_many,
        "read_function": crud.department.get_all
    },
    "hired_employee": {
        "fieldnames": list(models.Hired_Employee.__table__.columns.keys()),
        "write_function": crud.hired_employee.create_many,
        "read_function": crud.hired_employee.get_all
    }
}


@router.post("/uploadfile/")
async def create_upload_file(file_type: FileType, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    out_file_name = f"/file_storage/{file_type}/{file_type}.csv"
    async with aiofiles.open(out_file_name, mode='wb') as out_f:
        content = await file.read()
        await out_f.write(content)
    return {"filename": file.filename}


@router.post("/upload_to_db")
async def upload_to_db(db: Session = Depends(get_db)):
    final_result = {}

    for t in ft_attributes.keys():
        current_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        # variable initialization
        global_path = "file_storage/migration_data/processed_data"
        read_file_path = f"/file_storage/migration_data/input_data/{t}/{t}.csv"
        destination_file_path = f"/file_storage/migration_data/processed_data/{t}/{t}_{current_timestamp}.csv"
        fieldnames = ft_attributes[t]['fieldnames']
        write_all_function = ft_attributes[t]["write_function"]
        read_all_function = ft_attributes[t]["read_function"]

        # Check if file exists
        file_exists = await aiofiles.os.path.isfile(read_file_path)
        if not file_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File not found"
            )

        # check if table is not empty
        if read_all_function(db=db):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Table must be empty"
            )
        # read csv file
        async with aiofiles.open(read_file_path, mode='r') as f:
            content = await f.readlines()
        # reader with rows maped as dict
        csv_reader = csv.DictReader(
            content, fieldnames=fieldnames, delimiter=',')
        # convert to list
        data_list = []

        for row in csv_reader:
            del row['id']
            if t == "hired_employee":
            # if t == FileType.hired_employee:
                if row.get('department_id') == '':
                    row['department_id'] = None
                if row.get("job_id") == '':
                    row['job_id'] = None
            data_list.append(row)
        # [print(i, type(i)) for i in data_list]
        # call write function of particular model
        try:
            result = write_all_function(db=db, data=data_list)
            # move file to processed folder
            await aiofiles.os.replace(read_file_path, destination_file_path)
        except Exception as e:
            # , status_code=status.HTTP_400_BAD_REQUEST}
            return {"message": f"error\n{e}"}

        print(f"wrote {len(result)} rows to {t}")

        final_result[t] = len(result)
        # store result
        print(t, final_result[t])
        # print(final_result)

    return {"message": f"created\n{final_result}"}


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


@router.get("/test")
async def test():
    # file_types_names = 
    for t in FileType:
        print(t)
