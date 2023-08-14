from sqlalchemy.orm import Session
from typing import List
from crud.base import CRUDBase
from schemas.department import DepartmentCreate

import schemas
from models import Department

class CRUDDepartment(CRUDBase[Department, DepartmentCreate]):
    pass

department = CRUDDepartment(Department)