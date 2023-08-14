#!/usr/bin/python3
""" module of migration endpoints """

from datetime import datetime
from typing import Annotated
from sqlalchemy.orm import Session

from app.dependencies import get_db
import crud
import schemas

from fastapi import APIRouter, status, HTTPException, Depends
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

import aiofiles

router = APIRouter(
    prefix="/migrate",
    tags=["migration"]
)


@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be a CSV file"
        )
    out_file_name = f"/file_storage/{datetime.now()}_{file.filename}"
    async with aiofiles.open(out_file_name, mode='wb') as out_f:
        content = await file.read()
        await out_f.write(content)
    return {"filename": file.filename}



