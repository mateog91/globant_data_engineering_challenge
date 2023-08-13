from sqlalchemy.orm import Session
from typing import List

from app import schemas
from models.departments import Department


## Departments CRUD ##
def get_department(db: Session, department_id: int) -> Department:
    return db.query(Department).filter(Department.id == department_id).first()

def get_department_by_name(db: Session, name: str) -> Department:
    return db.query(Department).filter(Department.department == name).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100) -> List[Department]:
    result = db.query(Department).offset(skip).limit(limit).all()
    for e in result:
        print(e, type(e))
    return result

def create_department(db: Session, department: schemas.DepartmentCreate) -> Department:
    db_department = Department(department=department.department)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

######################
## Jobs CRUD ##
def get_job(db: Session, job_id: int):
    return db.query(Job).filter(Job.id == job_id).first()

def get_job_by_name(db: Session, name: str):
    return db.query(Job).filter(Job.job == name).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Job).offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = Job(job=job.job)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job