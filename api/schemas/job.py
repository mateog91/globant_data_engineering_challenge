from typing import Union
from pydantic import BaseModel
from .hired_employee import HiredEmployee


class JobBase(BaseModel):
    job: str


class JobCreate(JobBase):
    pass


class Job(JobBase):
    id: int
    hired_employee: list[HiredEmployee] = []

    class Config:
        orm_mode = True
