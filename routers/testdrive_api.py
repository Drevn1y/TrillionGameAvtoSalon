from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from database.models import TestDrive
from database import get_db
from pydantic import BaseModel
import datetime

testdrive_router = APIRouter(prefix='/testdrive', tags=['Управление с Тест драйвами'])

# Pydantic-схемы
class TestDriveCreate(BaseModel):
    user_id: int
    car_id: int
    scheduled_date: datetime.datetime
    status: str

@testdrive_router.post("/test_drives/")
def create_test_drive(test_drive: TestDriveCreate, db: Session = Depends(get_db)):
    new_test_drive = TestDrive(**test_drive.dict())
    db.add(new_test_drive)
    db.commit()
    db.refresh(new_test_drive)
    return new_test_drive

@testdrive_router.get("/test_drives/")
def get_all_test_drives(db: Session = Depends(get_db)):
    return db.query(TestDrive).all()

@testdrive_router.get("/test_drives/{test_drive_id}")
def get_test_drive(test_drive_id: int, db: Session = Depends(get_db)):
    test_drive = db.query(TestDrive).filter(TestDrive.test_drive_id == test_drive_id).first()
    if not test_drive:
        raise HTTPException(status_code=404, detail="Test drive not found")
    return test_drive

@testdrive_router.delete("/test_drives/{test_drive_id}")
def delete_test_drive(test_drive_id: int, db: Session = Depends(get_db)):
    test_drive = db.query(TestDrive).filter(TestDrive.test_drive_id == test_drive_id).first()
    if not test_drive:
        raise HTTPException(status_code=404, detail="Test drive not found")
    db.delete(test_drive)
    db.commit()
    return {"message": "Test drive deleted"}

