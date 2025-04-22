from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database.models import Insurance
from database import get_db
from pydantic import BaseModel
import datetime

insurance_router = APIRouter(prefix='/insurance', tags=['Управление с Страховкой'])


class InsuranceCreate(BaseModel):
    car_id: int
    policy_number: str
    provider: str
    start_date: datetime.date
    end_date: datetime.date
    coverage_amount: float
    status: str


@insurance_router.post("/insurances/")
def create_insurance(insurance: InsuranceCreate, db: Session = Depends(get_db)):
    new_insurance = Insurance(**insurance.dict())
    db.add(new_insurance)
    db.commit()
    db.refresh(new_insurance)
    return new_insurance

@insurance_router.get("/insurances/")
def get_all_insurances(db: Session = Depends(get_db)):
    return db.query(Insurance).all()

@insurance_router.get("/insurances/{insurance_id}")
def get_insurance(insurance_id: int, db: Session = Depends(get_db)):
    insurance = db.query(Insurance).filter(Insurance.insurance_id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    return insurance


@insurance_router.delete("/insurances/{insurance_id}")
def delete_insurance(insurance_id: int, db: Session = Depends(get_db)):
    insurance = db.query(Insurance).filter(Insurance.insurance_id == insurance_id).first()
    if not insurance:
        raise HTTPException(status_code=404, detail="Insurance not found")
    db.delete(insurance)
    db.commit()
    return {"message": "Insurance deleted"}
