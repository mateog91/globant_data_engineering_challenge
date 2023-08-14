#!/usr/bin/python3
""" module of migration endpoints """

from datetime import datetime
from enum import Enum
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db
import crud
import schemas

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


@router.post("/uploadfile/")
async def create_upload_file(file_type: FileType, file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    out_file_name = f"/file_storage/{file_type}/{datetime.now()}_{file.filename}"
    async with aiofiles.open(out_file_name, mode='wb') as out_f:
        content = await file.read()
        await out_f.write(content)
    return {"filename": file.filename}

# @routing.post("/upload_to_db")




