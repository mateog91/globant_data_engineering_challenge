from typing import Optional
from pydantic import BaseModel
from datetime import datetime as datetime_


class HiredEmployeeBase(BaseModel):
    name: Optional[str] = None
    department_id: Optional[int] = None
    job_id: Optional[int] = None


class HiredEmployeeCreate(HiredEmployeeBase):
    pass


class HiredEmployee(HiredEmployeeBase):
    id: int
    datetime: Optional[datetime_] = None

    class Config:
        orm_mode = True

class HiredEmployeeImport(HiredEmployeeBase):
    datetime: Optional[datetime_] = None
