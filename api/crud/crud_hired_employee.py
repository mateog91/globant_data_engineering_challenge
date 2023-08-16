from sqlalchemy.orm import Session
from typing import List
from crud.base import CRUDBase
from schemas.hired_employee import HiredEmployeeCreate, HiredEmployeeCreateList

import schemas
from models import Hired_Employee

class CRUDHired_Employee(CRUDBase[Hired_Employee, HiredEmployeeCreate]):
    pass

hired_employee = CRUDHired_Employee(Hired_Employee)