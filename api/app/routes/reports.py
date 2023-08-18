#!/usr/bin/python3
""" module of department endpoints """

import re
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
import sqlalchemy as sa
from app.dependencies import get_db
import crud
import schemas

router = APIRouter(
    prefix="/reports",
    tags=["reports"]
)

QUERY = """
SELECT 
	d.department,
	j.job,
 	SUM(CASE WHEN EXTRACT(quarter FROM he.datetime) = 1 THEN 1 ELSE 0 END) AS Q1,
    SUM(CASE WHEN EXTRACT(quarter FROM he.datetime) = 2 THEN 1 ELSE 0 END) AS Q2,
    SUM(CASE WHEN EXTRACT(quarter FROM he.datetime) = 3 THEN 1 ELSE 0 END) AS Q3,
    SUM(CASE WHEN EXTRACT(quarter FROM he.datetime) = 4 THEN 1 ELSE 0 END) AS Q4
FROM hired_employees as he
LEFT JOIN departments as d
ON he.department_id = d.id
LEFT JOIN jobs as j
ON he.job_id = j.id
WHERE EXTRACT(year FROM he.datetime) = 2021
GROUP BY d.department, j.job;
"""


@router.get("/")
def hired_employees_by_department_and_job(db: Session = Depends(get_db)
                                          ):
    """
    Get hired employees by department and job
    """
    columns = ["department", "job", "Q1", "Q2", "Q3", "Q4"]
    result = db.execute(sa.text(QUERY))
    
    result2 = [dict(zip(columns, row)) for row in result]

    return result2
