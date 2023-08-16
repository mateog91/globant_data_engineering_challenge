from typing import Optional
from pydantic import BaseModel


class HiredEmployeeBase(BaseModel):
    name: Optional[str] = None
    datetime: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None


class HiredEmployeeCreate(HiredEmployeeBase):
    pass

class HiredEmployeeCreateList(HiredEmployeeCreate):
    id: int


class HiredEmployee(HiredEmployeeBase):
    id: int

    class Config:
        orm_mode = True
