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

QUERY2 = """
WITH department_stats AS (
    SELECT
        d.id,
        d.department AS department,
        COUNT(he.id) AS hired
    FROM
        departments d
    LEFT JOIN
        hired_employees he ON d.id = he.department_id
    WHERE
        EXTRACT(year FROM he.datetime) = 2021
    GROUP BY
        d.id, d.department
),
avg_hired AS (
    SELECT
        AVG(hired) AS mean_hired
    FROM
        department_stats
)
SELECT
    ds.id,
    ds.department,
    ds.hired
FROM
    department_stats ds
JOIN
    avg_hired ah ON ds.hired > ah.mean_hired
ORDER BY
    ds.hired DESC;
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

@router.get("/hired_employees_by_department_over_average")
def hired_employees_by_department_over_average(db: Session = Depends(get_db)
                                               ):
    """
    Get hired employees by department and job
    """
    columns = ["id", "department", "hired"]
    result = db.execute(sa.text(QUERY))

    result2 = [dict(zip(columns, row)) for row in result]

    return result2
