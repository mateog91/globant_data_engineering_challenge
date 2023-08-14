from pydantic import BaseModel
from sqlalchemy.orm import Session
import typing as tp
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
        batches = itertools.
        rows = [self.model(**row.dict()) for row in data]
        db.add_all(rows)
        db.commit()
        for row in rows:
            db.refresh(row)
        return rows
