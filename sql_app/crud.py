from sqlalchemy.orm import Session

from . import models, schemas

## Departments CRUD ##
def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_department_by_name(db: Session, name: str):
    return db.query(models.Department).filter(models.Department.department == name).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

######################
## Jobs CRUD ##
def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_job_by_name(db: Session, name: str):
    return db.query(models.Job).filter(models.Job.job == name).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()