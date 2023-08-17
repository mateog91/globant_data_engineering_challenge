from typing import Optional
from pydantic import BaseModel


class HiredEmployeeBase(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None


class HiredEmployeeCreate(HiredEmployeeBase):
    pass


class HiredEmployee(HiredEmployeeBase):
    id: int
    datetime: Optional[str] = None

    class Config:
        orm_mode = True
