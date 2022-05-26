import models
from fastapi import FastAPI, Request, Depends 
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from pydantic import BaseModel
from models import Employee, Timesheet
from datetime import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class RegisterEmployee(BaseModel):
    employee_id: int
    employee_name: str


class RegisterTimesheet(BaseModel):
    employee_id: int
    date: str
    amount_of_hours_worked: int


def fetch_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/employees_page")
async def employees_page(request: Request, employee_id=None, db: Session = Depends(fetch_db)):
    """
    Processes GET request to display all the employees record and also filter by employee_id
    """

    employees = db.query(Employee)

    if employee_id:
        employees = employees.filter(Employee.employee_id == employee_id)

    return templates.TemplateResponse("employee.html", {
        "request": request,
        "employees": employees
    })


@app.get("/timesheet_page")
async def timesheet_page(request: Request, employee_id=None, date=None, db: Session = Depends(fetch_db)):
    """
    Processes GET request to display all the timesheets record and also filter by employee_id and date
    """

    timesheets = db.query(Timesheet)

    if employee_id:
        timesheets = timesheets.filter(Timesheet.employee_id == employee_id)
    
    if date:
        timesheets = timesheets.filter(Timesheet.date == date)

    return templates.TemplateResponse("timesheet.html", {
        "request": request,
        "timesheets": timesheets
    })


@app.post("/employee")
async def register_employee(create_employee: RegisterEmployee, db: Session = Depends(fetch_db)):
    """
    Processes POST request to register new employees
    """

    employee = Employee()

    employee.employee_id = create_employee.employee_id
    employee.employee_name = create_employee.employee_name

    db.add(employee)
    db.commit()

    return {"Employee": "Registered"}


@app.post("/timesheet")
async def register_timesheet(create_timesheet: RegisterTimesheet, db: Session = Depends(fetch_db)):
    """
    Processes POST request to register employee timesheets
    """
    
    timesheet = Timesheet()
    
    timesheet.employee_id = create_timesheet.employee_id
    timesheet.date = datetime.strptime(create_timesheet.date, '%Y-%m-%d')
    timesheet.amount_of_hours_worked = create_timesheet.amount_of_hours_worked
    
    db.add(timesheet)
    db.commit()

    return {"Timesheet": "Registered"}
