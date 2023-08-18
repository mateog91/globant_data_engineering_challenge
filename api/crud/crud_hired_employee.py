import json
from more_itertools import ichunked
from datetime import datetime, timezone
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from typing import List, Union
from models.hired_employee import Hired_Employee
from schemas.hired_employee import HiredEmployeeCreate, HiredEmployeeImport
from crud.base import CRUDBase
from schemas.hired_employee import HiredEmployeeCreate

import schemas
from models import Hired_Employee


class CRUDHired_Employee(CRUDBase[Hired_Employee, HiredEmployeeCreate]):
    def create(
        self, db: Session, data_in: HiredEmployeeCreate
    ) -> Hired_Employee:
        current_datetime = datetime.now(
            timezone.utc)
        db_obj_data = jsonable_encoder(data_in)
        row = self.model(**db_obj_data, datetime=current_datetime)

        db.add(row)
        db.commit()
        db.refresh(row)

        return row

    def create_many(self, db: Session, data: List[HiredEmployeeCreate]) -> List[Hired_Employee]:
        return_rows = []
        current_datetime = datetime.now(
            timezone.utc)
        all_chunks = ichunked(data, 1000)
        for chunck in all_chunks:
            rows = [self.model(**jsonable_encoder(row),
                               datetime=current_datetime) for row in chunck]
            db.add_all(rows)
            db.flush()
            return_rows.extend(rows)
        db.commit()
        for row in return_rows:
            db.refresh(row)
        return return_rows

    def create_many_import(self, db: Session, data: List[HiredEmployeeImport]) -> List[Hired_Employee]:
        return_rows = []
        all_chunks = ichunked(data, 1000)
        for chunck in all_chunks:
            rows = [self.model(**jsonable_encoder(row)) for row in chunck]
            db.add_all(rows)
            db.flush()
            return_rows.extend(rows)
        db.commit()
        for row in return_rows:
            db.refresh(row)
        return return_rows


hired_employee = CRUDHired_Employee(Hired_Employee)
