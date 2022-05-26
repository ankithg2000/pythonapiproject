from sqlalchemy import Column, Integer, String, Date

from database import Base


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    employee_name = Column(String, index=True)


class Timesheet(Base):
    __tablename__ = "timesheet"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, index=True)
    date = Column(Date, index=True)
    amount_of_hours_worked = Column(Integer, index=True)

