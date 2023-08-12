from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String)
    
    hired_employees = relationship("Hired_Employee", back_populates="department")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String)
    
    hired_employee = relationship("Hired_Employee", back_populates="job")


class Hired_Employee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    datetime = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    department = relationship("Department", back_populates="hired_employees")

    job = relationship("Job", back_populates="hired_employees")
