from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
import typing as tp
from more_itertools import ichunked
from models.base import Base

import schemas


## Custom Type Alias ##

ModelType = tp.TypeVar("ModelType", bound=Base)
CreateSchemaType = tp.TypeVar("CreateSchemaType", bound=BaseModel)


class CRUDBase(tp.Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: tp.Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> ModelType:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> list[ModelType]:
        result = db.query(self.model).offset(skip).limit(limit).all()
        return result

    def create(self, db: Session, data_in: CreateSchemaType) -> ModelType:
        db_obj_data = jsonable_encoder(data_in)
        row = self.model(**db_obj_data)
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    def create_many(self, db: Session, data: tp.List[CreateSchemaType]) -> tp.List[ModelType]:
        return_rows = []
        all_chunks = ichunked(data, 2)
        for chunck in all_chunks:
            rows = [self.model(**jsonable_encoder(row)) for row in chunck]
            db.add_all(rows)
            db.flush()
            return_rows.extend(rows)
        db.commit()
        for row in return_rows:
            db.refresh(row)
        return return_rows
