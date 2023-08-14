from typing import Union
from pydantic import BaseModel


class HiredEmployeeBase(BaseModel):
    name: Union[str, None] = None
    datetime: Union[str, None] = None
    department_id: Union[int, None] = None
    job_id: Union[int, None] = None


class HiredEmployeeCreate(HiredEmployeeBase):
    pass


class HiredEmployee(HiredEmployeeBase):
    id: int


    class Config:
        orm_mode = True
