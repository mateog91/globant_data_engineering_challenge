from typing import Optional
from sqlalchemy.orm import Session
from crud.base import CRUDBase
from models import Job
from schemas.job import JobCreate


class CRUDJob(CRUDBase[Job, JobCreate]):
    def get_by_name(self, db: Session, name: str):
        return db.query(Job).filter(Job.job == name).first()


job = CRUDJob(Job)
