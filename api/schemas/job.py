from typing import List, Optional, Union
from pydantic import BaseModel
from .hired_employee import HiredEmployee


class JobBase(BaseModel):
    job: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    hired_employees: list[HiredEmployee] = []

    class Config:
        orm_mode = True
