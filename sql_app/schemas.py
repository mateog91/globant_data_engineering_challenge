from typing import Union
from pydantic import BaseModel

class HiredEmployee(BaseModel):
    id: int
    name = Union[str, None] = None
    datetime = Union[str, None] = None
    department_id: int
    job_id: int

    class Config:
        orm_mode = True


class Department(BaseModel):
    id: int
    department: Union[str, None] = None
    hired_employee: list[HiredEmployee] = []

    class Config:
        orm_mode = True


class Job(BaseModel):
    id: int
    job: Union[str, None] = None
    hired_employee: list[HiredEmployee] = []

    class Config:
        orm_mode = True
