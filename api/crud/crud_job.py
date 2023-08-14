from sqlalchemy.orm import Session
from typing import List
from crud.base import CRUDBase
from schemas.job import JobCreate

import schemas
from models import Job

class CRUDJob(CRUDBase[Job, JobCreate]):
    pass

job = CRUDJob(Job)