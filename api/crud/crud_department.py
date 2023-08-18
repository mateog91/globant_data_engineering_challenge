from sqlalchemy.orm import Session
from typing import List
from crud.base import CRUDBase
from schemas.department import DepartmentCreate

from models import Department


class CRUDDepartment(CRUDBase[Department, DepartmentCreate]):
    def get_by_name(self, db: Session, name: str):
        return db.query(Department).filter(Department.department == name).first()


department = CRUDDepartment(Department)
