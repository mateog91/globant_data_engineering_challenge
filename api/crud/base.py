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

    def create(self, db: Session, data: CreateSchemaType) -> ModelType:
        row = self.model(**data.dict())
        db.add(row)
        db.commit()
        db.refresh(row)
        return row

    def create_many(self, db: Session, data: tp.List[CreateSchemaType]) -> tp.List[ModelType]:
        all_chunks = ichunked(data, 1000)
        return_rows = []
        for chunck in all_chunks:
            print("inside create many")
            # print(type(chunck[0]))
            # rows = [print(row, type(row)) for row in chunck]
            rows = [self.model(**row) for row in chunck]
            db.add_all(rows)
            db.commit()
            for row in rows:
                db.refresh(row)
            return_rows.extend(rows)
            # print(rows)
        return return_rows
