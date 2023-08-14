from typing import Union
from pydantic import BaseModel
from .hired_employee import HiredEmployee


class DepartementBase(BaseModel):
    department: str


class DepartmentCreate(DepartementBase):
    pass


class Department(DepartementBase):
    id: int
    hired_employees: list[HiredEmployee] = []

    class Config:
        orm_mode = True
