from sqlalchemy.orm import Session

from . import models, schemas

## Departments CRUD ##
def get_department(db: Session, department_id: int):
    return db.query(models.Department).filter(models.Department.id == department_id).first()

def get_department_by_name(db: Session, name: str):
    return db.query(models.Department).filter(models.Department.department == name).first()


def get_departments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Department).offset(skip).limit(limit).all()

def create_department(db: Session, department: schemas.DepartmentCreate):
    db_department = models.Department(department=department.department)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department

######################
## Jobs CRUD ##
def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_job_by_name(db: Session, name: str):
    return db.query(models.Job).filter(models.Job.job == name).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(job=job.job)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job